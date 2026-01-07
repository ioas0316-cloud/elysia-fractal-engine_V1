"""
Batch processor using multiprocessing to spread CPU load without external APIs.

Usage:
    python Tools/worker_pool.py --input prompts.txt --output out.txt --workers 4
"""

import argparse
import os
import sys
import multiprocessing as mp


def init_worker():
    # Ensure Core on path inside each worker
    ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if ROOT not in sys.path:
        sys.path.insert(0, ROOT)
    global kernel
    from Core.System.System.System.Kernel import kernel  # noqa: E402


def process_line(line: str) -> str:
    line = line.strip()
    if not line:
        return ""
    # kernel is set in init_worker
    return kernel.process_thought(line)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Input text file (one prompt per line)")
    parser.add_argument("--output", required=True, help="Output file to append results")
    parser.add_argument("--workers", type=int, default=mp.cpu_count(), help="Number of worker processes")
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        lines = [l.strip() for l in f if l.strip()]

    with mp.Pool(processes=args.workers, initializer=init_worker) as pool:
        results = pool.map(process_line, lines)

    with open(args.output, "a", encoding="utf-8") as f:
        for q, r in zip(lines, results):
            f.write(f"Q: {q}\nA: {r}\n---\n")


if __name__ == "__main__":
    main()
