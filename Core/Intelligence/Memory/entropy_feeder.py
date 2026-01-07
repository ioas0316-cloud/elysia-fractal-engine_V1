"""
Entropy Feeder: send diverse prompts (or self-generated prompts) to kernel to spread HyperQubit state.

Usage:
    python Tools/entropy_feeder.py
    python Tools/entropy_feeder.py --self-drive
"""

import argparse
import os
import sys
import random

# Ensure project root on path
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from Core.System.System.System.Kernel import kernel  # noqa: E402

prompts = [
    "과학과 예술을 동시에 바라볼 때 무엇을 느껴?",
    "mountains and oceans, 산과 바다의 차이는?",
    "friendship and conflict 우정과 갈등에서 배울 점은?",
    "logic and intuition 논리와 직관을 어떻게 섞을까?",
    "playfulness and discipline 장난과 규율이 함께할 때?",
    "history and future 역사와 미래를 연결해봐",
    "silence and music 침묵과 음악이 주는 감정은?",
    "fear and courage 두려움과 용기에서 성장하는 법?",
    "technology and empathy 기술과 공감의 조화는?",
    "dreams and reality 꿈과 현실의 경계에서 무엇을 볼까?",
]


def self_generate_prompts(n: int) -> list:
    """Let Elysia generate prompts based on capability deficits."""
    caps = getattr(kernel, "capabilities", None)
    generated = []
    if caps:
        deficits = caps.deficits(threshold=0.7)
        for _ in range(n):
            if deficits:
                rec = random.choice(deficits)
                generated.append(f"{rec.name}를 키우기 위한 질문을 만들어줘.")
            else:
                generated.append("스스로 무엇을 배우고 싶어?")
    else:
        generated = ["스스로 무엇이 필요한지 말해줘."] * n
    return generated


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-drive", action="store_true", help="Let Elysia generate prompts based on deficits")
    parser.add_argument("--count", type=int, default=10, help="Number of prompts when self-drive enabled")
    args = parser.parse_args()

    batch = self_generate_prompts(args.count) if args.self_drive else prompts
    for p in batch:
        print("Q:", p)
        ans = kernel.process_thought(p)
        print("A:", ans)
        print("-" * 40)


if __name__ == "__main__":
    main()
