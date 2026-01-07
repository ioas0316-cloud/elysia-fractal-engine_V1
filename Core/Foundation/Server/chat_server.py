"""
Simple HTTP chat server for talking with Elysia in real time.

Usage (from project root):
    python Tools/chat_server.py --port 8765

Then open http://127.0.0.1:8765 in a browser.
"""


import argparse
import json
import logging
import os
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer


ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)


# Define logger early
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("ElysiaChat")

from Core.Intelligence.Intelligence.Reasoning import ReasoningEngine


# Initialize the engine once
logger.info("Initializing ReasoningEngine v10.0...")
try:
    engine = ReasoningEngine()
except Exception as e:
    logger.error(f"Failed to initialize engine: {e}")
    sys.exit(1)

CHAT_HTML = """<!DOCTYPE html>
<html lang="ko">
<head>

  <meta charset="utf-8">
  <title>Elysia Chat</title>
  <style>
    body { font-family: system-ui, -apple-system, BlinkMacSystemFont, sans-serif; margin: 0; padding: 0; background: #0b1020; color: #f2f2f2; }
    #wrap { max-width: 800px; margin: 0 auto; padding: 16px; }
    #log { height: 480px; overflow-y: auto; border: 1px solid #333; padding: 8px; background: #050814; }
    .msg { margin: 4px 0; }
    .who { font-weight: bold; margin-right: 4px; }
    .you { color: #9cdcfe; }
    .elysia { color: #c586c0; }
    #input-row { display: flex; margin-top: 8px; }
    #msg { flex: 1; padding: 6px 8px; border-radius: 4px; border: 1px solid #333; background: #0f1628; color: #f2f2f2; }
    #send { margin-left: 8px; padding: 6px 12px; border-radius: 4px; border: none; background: #3b82f6; color: #fff; cursor: pointer; }
    #send:disabled { background: #555; cursor: default; }
  </style>
</head>
<body>
  <div id="wrap">
    <h2>Elysia Chat</h2>
    <div id="log"></div>
    <form id="chat-form">
      <div id="input-row">
        <input id="msg" autocomplete="off" placeholder="메시지를 입력하세요..." />
        <button id="send" type="submit">Send</button>
      </div>
    </form>
  </div>
  <script>
    const log = document.getElementById('log');
    const form = document.getElementById('chat-form');
    const input = document.getElementById('msg');
    const sendBtn = document.getElementById('send');

    function append(who, text) {
      const div = document.createElement('div');
      div.className = 'msg';
      const spanWho = document.createElement('span');
      spanWho.className = 'who ' + (who === 'you' ? 'you' : 'elysia');
      spanWho.textContent = who === 'you' ? 'You:' : 'Elysia:';
      const spanText = document.createElement('span');
      spanText.textContent = ' ' + text;
      div.appendChild(spanWho);
      div.appendChild(spanText);
      log.appendChild(div);
      log.scrollTop = log.scrollHeight;
    }

    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const text = input.value.trim();
      if (!text) return;
      append('you', text);
      input.value = '';
      sendBtn.disabled = true;
      try {
        const res = await fetch('/api/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message: text })
        });
        if (!res.ok) {
          append('elysia', '(error: ' + res.status + ')');
        } else {
          const data = await res.json();
          append('elysia', data.response || '(empty response)');
        }
      } catch (err) {
        append('elysia', '(network error)');
      } finally {
        sendBtn.disabled = false;
        input.focus();
      }
    });

    input.focus();
  </script>
</body>
</html>
"""



class ChatHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        if self.path in ("/", "/index.html"):
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(CHAT_HTML.encode("utf-8"))

        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self) -> None:
        if self.path != "/api/chat":
            self.send_response(404)
            self.end_headers()
            return
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length) if length > 0 else b""
        try:
            payload = json.loads(raw.decode("utf-8") or "{}")
        except json.JSONDecodeError:
            payload = {}
        message = str(payload.get("message", "")).strip()
        if not message:
            self.send_response(400)
            self.end_headers()
            return
        try:
            # v10.0 Logic: Use engine.communicate(message)
            reply = engine.communicate(message)
        except Exception as e:
            logger.error("Error during chat processing: %s", e)
            self.send_response(500)
            self.end_headers()
            return
        body = json.dumps({"response": reply}, ensure_ascii=False).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args) -> None:
        # Suppress default noisy HTTP logs; rely on our logger instead.
        return


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()

    server = HTTPServer((args.host, args.port), ChatHandler)
    logger.info("Elysia chat server listening on http://%s:%d", args.host, args.port)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logger.info("Shutting down chat server.")
        server.server_close()


if __name__ == "__main__":
    main()

