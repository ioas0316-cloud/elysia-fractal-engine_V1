"""
Meta Runner: cycles through question -> experiment -> evaluation -> integration.
- Generates simple questions from capability deficits
- Runs experiment by sending the question to kernel (process_thought)
- Logs outcome and updates memory via kernel (already integrated in process_thought)

Usage:
    python Tools/meta_runner.py --steps 5 --interval 1.0
"""

import argparse
import logging
import random
import time
from pathlib import Path

from Core.System.System.System.Kernel import kernel

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("MetaRunner")

PROMPTS = [
    "무엇을 더 배워야 할까?",
    "최근에 놓친 개념은 무엇이지?",
    "기억 속 위상과 가치가 어긋난 부분은?",
    "지금 가장 개선이 필요한 역량은?",
    "새로운 연결을 만들 수 있는 개념은?",
]


def pick_question():
    caps = getattr(kernel, "capabilities", None)
    if caps:
        deficits = caps.deficits(threshold=0.6)
        if deficits:
            rec = random.choice(deficits)
            return f"{rec.name} 역량을 높이려면 무엇을 시도해야 할까?"
    # add core values prompts to diversify
    core_vals = getattr(kernel, "core_values", {})
    if core_vals:
        key = random.choice(list(core_vals.keys()))
        return f"{key}을(를) 더 깊이 느끼고 표현하려면 무엇을 해야 할까?"
    return random.choice(PROMPTS)


def run_step(step_idx: int, log_path: Path):
    question = pick_question()
    response = kernel.process_thought(question)
    log_entry = {
        "step": step_idx,
        "question": question,
        "response": response,
        "snapshot": kernel._snapshot_state(),
    }
    with log_path.open("a", encoding="utf-8") as f:
        f.write(str(log_entry) + "\n")
    logger.info(f"[MetaRunner] Q: {question} | A: {response}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--steps", type=int, default=5)
    parser.add_argument("--interval", type=float, default=1.0)
    parser.add_argument("--log", type=str, default="meta_runner.log")
    args = parser.parse_args()

    log_path = Path(args.log)
    for i in range(1, args.steps + 1):
        run_step(i, log_path)
        time.sleep(max(0.0, args.interval))


if __name__ == "__main__":
    main()
