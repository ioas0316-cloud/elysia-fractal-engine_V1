"""
Headless live loop for Elysia on Windows.
- Runs kernel.tick() periodically
- Reads stdin (and optional TCP socket) into a queue and feeds kernel.voice
- Writes heartbeat to a file for liveness monitoring

Usage:
    python Tools/live_loop.py [--tcp 8765] [--heartbeat elysia_heartbeat.txt]
"""

import argparse
import threading
import queue
import time
import sys
import os
import logging
from pathlib import Path
import socketserver
from typing import Set
from http.server import BaseHTTPRequestHandler, HTTPServer
import random

# Ensure project root on path
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from Core.System.System.System.Kernel import kernel  # noqa: E402

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("LiveLoop")

INPUT_QUEUE = queue.Queue()


class TCPHandler(socketserver.StreamRequestHandler):
    def handle(self):
        for line in self.rfile:
            text = line.decode("utf-8", errors="ignore").strip()
            if text:
                INPUT_QUEUE.put(text)
            if text.lower() in {"quit", "exit"}:
                break


class HTTPHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode("utf-8", errors="ignore").strip()
        if body:
            for line in body.splitlines():
                line = line.strip()
                if line:
                    INPUT_QUEUE.put(line)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"ok")

    def log_message(self, format, *args):
        return  # suppress default logging


def stdin_reader():
    for line in sys.stdin:
        text = line.strip()
        if text:
            INPUT_QUEUE.put(text)
        if text.lower() in {"quit", "exit"}:
            break


def write_heartbeat(path: Path):
    path.write_text(str(time.time()), encoding="utf-8")


def poll_watch_dir(watch_dir: Path, seen: Set[Path]):
    """Poll a directory for new text files and enqueue their content as inputs."""
    if not watch_dir.exists() or not watch_dir.is_dir():
        return
    for path in watch_dir.glob("*.txt"):
        if path in seen:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore").strip()
            if text:
                for line in text.splitlines():
                    line = line.strip()
                    if line:
                        INPUT_QUEUE.put(line)
            seen.add(path)
            logger.info(f"Ingested file from watch dir: {path}")
        except Exception as e:
            logger.error(f"Failed to read {path}: {e}")


def generate_question():
    caps = getattr(kernel, "capabilities", None)
    prompts = [
        "무엇을 더 배우고 싶나요?",
        "지금 가장 필요한 것은 무엇일까요?",
        "어떤 역량을 먼저 키워야 할까요?",
        "축(사랑/성장/조화/아름다움)에 맞춰 목표를 정해볼까요?",
    ]
    if caps:
        deficits = caps.deficits(threshold=0.6)
        if deficits:
            rec = random.choice(deficits)
            return f"{rec.name} 역량을 높이려면 무엇을 시도할까요?"
    return random.choice(prompts)


def run_self_eval():
    caps = getattr(kernel, "capabilities", None)
    if not caps:
        return
    snap = kernel._snapshot_state()
    momentum_active = int(snap.get("momentum_active", 0))
    chaos_raw = abs(float(snap.get("chaos_raw", 0.0)))

    # If the mind is already very busy or unstable, skip self-critique.
    if momentum_active > 3 or chaos_raw > 50.0:
        logger.info("[SelfEval] Skipping self-evaluation (mind too busy / unstable).")
        return

    # Occasionally choose pure rest over evaluation, even if called.
    if random.random() < 0.3:
        logger.info("[SelfEval] Choosing rest instead of creating new improvement tickets this cycle.")
        return

    tickets = []
    deficits = caps.deficits(threshold=0.7)
    for rec in deficits:
        # Allow Elysia to sometimes live with a known weakness for now.
        if random.random() < 0.5:
            logger.info(f"[SelfEval] Accepting current limitation for now: {rec.name} (no ticket opened).")
            continue
        tickets.append(caps.add_ticket(rec.name, "deficit", "self-eval"))
    # Entropy check
    phase = snap.get("phase", {})
    qubit = phase.get("qubit", {})
    entropy = 0.0
    if qubit:
        total = sum(qubit.values())
        if total > 0:
            import math
            norm = [p / total for p in qubit.values() if p > 0]
            entropy = -sum(p * math.log(p, 2) for p in norm)
    if entropy < 0.2:
        tickets.append(caps.add_ticket("phase", "low entropy", "diversify concepts"))
    if tickets:
        for t in tickets:
            logger.info(f"[SelfEval] Ticket {t.ticket_id}: {t.target} | {t.issue}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--tcp", type=int, default=None, help="Listen on TCP port for input (optional)")
    parser.add_argument("--http", type=int, default=None, help="Listen on HTTP port for POST input (optional)")
    parser.add_argument("--heartbeat", type=str, default="elysia_logs/elysia_heartbeat.txt")
    parser.add_argument("--tick-interval", type=float, default=0.1)
    parser.add_argument("--state-file", type=str, default="saves/elysia_state.json")
    parser.add_argument("--load-state", action="store_true", help="Load state at startup if file exists")
    parser.add_argument("--save-interval", type=float, default=30.0, help="Seconds between state saves")
    parser.add_argument("--watch-dir", type=str, default=None, help="Directory to poll for .txt inputs")
    parser.add_argument("--ask-interval", type=float, default=0.0, help="If >0, Elysia proactively asks when idle (seconds)")
    parser.add_argument("--self-eval-interval", type=float, default=0.0, help="If >0, periodically create self-eval tickets (seconds)")
    args = parser.parse_args()

    heartbeat_path = Path(args.heartbeat)
    watch_dir = Path(args.watch_dir) if args.watch_dir else None
    seen_files: Set[Path] = set()

    heartbeat_path.parent.mkdir(parents=True, exist_ok=True)

    reader_thread = threading.Thread(target=stdin_reader, daemon=True)
    reader_thread.start()

    if args.load_state:
        try:
            kernel.load_state(args.state_file)
            logger.info(f"Loaded state from {args.state_file}")
        except Exception as e:
            logger.error(f"State load failed: {e}")

    server = None
    if args.tcp:
        server = socketserver.ThreadingTCPServer(("127.0.0.1", args.tcp), TCPHandler)
        server.daemon_threads = True
        threading.Thread(target=server.serve_forever, daemon=True).start()
        logger.info(f"TCP input listening on 127.0.0.1:{args.tcp}")
    http_server = None
    if args.http:
        http_server = HTTPServer(("127.0.0.1", args.http), HTTPHandler)
        threading.Thread(target=http_server.serve_forever, daemon=True).start()
        logger.info(f"HTTP input listening on 127.0.0.1:{args.http}")

    logger.info("Live loop started. Type messages (stdin/TCP/HTTP); 'quit' to exit.")
    last_save = time.time()
    last_input = time.time()
    last_eval = time.time()
    try:
        while True:
            now = time.time()
            kernel.tick()
            # Run action agent (Elysia acting) each loop with throttle
            if hasattr(kernel, "action_agent"):
                kernel.action_agent.run(now)

            while not INPUT_QUEUE.empty():
                user_text = INPUT_QUEUE.get()
                if user_text.lower() in {"quit", "exit"}:
                    logger.info("Received exit command. Shutting down.")
                    if server:
                        server.shutdown()
                    if http_server:
                        http_server.shutdown()
                    return
                response = kernel.process_thought(user_text)
                print(response, flush=True)
                last_input = time.time()

            if watch_dir:
                poll_watch_dir(watch_dir, seen_files)

            # Proactive question when idle
            if args.ask_interval > 0 and (now - last_input) >= args.ask_interval:
                question = generate_question()
                print(f"[Elysia asks] {question}", flush=True)
                ans = kernel.process_thought(question)
                print(f"[Elysia answers] {ans}", flush=True)
                last_input = now

            write_heartbeat(heartbeat_path)
            if args.save_interval > 0 and (now - last_save) >= args.save_interval:
                try:
                    kernel.save_state(args.state_file)
                    last_save = now
                except Exception as e:
                    logger.error(f"State save failed: {e}")
            if args.self_eval_interval > 0 and (now - last_eval) >= args.self_eval_interval:
                run_self_eval()
                last_eval = now
            time.sleep(max(0.01, args.tick_interval))
    except KeyboardInterrupt:
        logger.info("Interrupted; exiting.")
        if server:
            server.shutdown()
        if http_server:
            http_server.shutdown()


if __name__ == "__main__":
    main()
