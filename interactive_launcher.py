import sys
import time
import os
from typing import Dict, Any
import math

# Ensure the package is in the path
sys.path.append(os.getcwd())

from elysia_engine import World, Entity
from elysia_engine.storyteller import StoryTeller
from elysia_engine.persona import build_persona_frame

# --- Define Examples Classes Here (Self-contained) ---

class Warrior(Entity):
    def __init__(self, id: str):
        super().__init__(id=id, role="warrior")
    def update_force_components(self, world: World) -> None:
        # Body cycles strongly, others low
        self.f_body = (math.sin(world.time / 2.0) + 1.2) * 0.8
        self.f_soul = 0.2
        self.f_spirit = 0.1

class Mage(Entity):
    def __init__(self, id: str):
        super().__init__(id=id, role="mage")
    def update_force_components(self, world: World) -> None:
        # Soul cycles
        self.f_soul = (math.sin(world.time / 3.0) + 1.2) * 0.8
        self.f_body = 0.1
        self.f_spirit = 0.3

class Priest(Entity):
    def __init__(self, id: str):
        super().__init__(id=id, role="priest")
    def update_force_components(self, world: World) -> None:
        # Spirit cycles
        self.f_spirit = (math.sin(world.time / 4.0) + 1.2) * 0.8
        self.f_body = 0.1
        self.f_soul = 0.4

class Pulse(Entity):
    def update_force_components(self, world: World) -> None:
        # Simple rhythmic breathing
        self.f_body = (math.sin(world.time / 2.0) + 1.0) * 0.5
        self.f_soul = 0.0
        self.f_spirit = 0.0

# --- Runners ---

def run_three_heroes():
    print("\n=== [시나리오 1] 세 영웅의 이야기 ===")
    print("전사(Warrior), 마법사(Mage), 사제(Priest)가 모험을 떠납니다.")
    print("엔진이 각 캐릭터의 내면(Body/Soul/Spirit)을 시뮬레이션하고,")
    print("StoryTeller가 이를 문장으로 변환합니다.")
    print("\n[Ctrl+C]를 누르면 언제든지 메뉴로 돌아갑니다.\n")
    time.sleep(2)

    world = World()
    world.add_entity(Warrior("Aragorn"))
    world.add_entity(Mage("Gandalf"))
    world.add_entity(Priest("Mercy"))

    try:
        while True:
            world.step(dt=0.5)
            snap = world.export_persona_snapshot()

            # Use StoryTeller to print text
            story = StoryTeller.narrate_frame(snap)
            print(story)

            time.sleep(1.0) # Read speed
    except KeyboardInterrupt:
        print("\n모험이 종료되었습니다.")

def run_simple_pulse():
    print("\n=== [시나리오 2] 단순한 호흡 ===")
    print("하나의 의식이 숨을 쉽니다. 에너지의 파동을 시각적으로 느껴보세요.")
    print("\n[Ctrl+C]를 누르면 언제든지 메뉴로 돌아갑니다.\n")
    time.sleep(2)

    world = World()
    world.add_entity(Pulse("Breath"))

    try:
        while True:
            world.step(dt=0.2)
            snap = world.export_persona_snapshot()

            entities = snap.get("entities", [])
            if entities:
                # Access force components directly from the new payload structure
                forces = entities[0].get("force_components", {})
                e_val = forces.get("body", 0.0) # Pulse uses body for breathing

                # Visual Bar
                bar_len = int(e_val * 40)
                bar = "#" * bar_len
                print(f"[호흡] {bar:<40} ({e_val:.2f})")

            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\n명상이 종료되었습니다.")

def main():
    while True:
        try:
            print("\n" + "="*40)
            print("   🌌 엘리시아 엔진 인터랙티브 런처 🌌")
            print("="*40)
            print("1. 세 영웅의 이야기 (Story Mode)")
            print("2. 단순한 호흡 (Visual Mode)")
            print("3. 종료 (Exit)")
            print("-" * 40)

            choice = input("선택을 입력하세요 (1-3): ").strip()

            if choice == "1":
                run_three_heroes()
            elif choice == "2":
                run_simple_pulse()
            elif choice == "3":
                print("엘리시아 엔진을 종료합니다. 안녕히 가세요!")
                break
            else:
                print("잘못된 입력입니다. 다시 선택해주세요.")
        except KeyboardInterrupt:
            # Handle Ctrl+C at menu level gracefully
            print("\n종료하려면 3번을 선택하세요.")

if __name__ == "__main__":
    main()
