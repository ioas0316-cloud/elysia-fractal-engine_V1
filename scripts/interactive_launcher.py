import sys
import time
import os
from typing import Dict, Any
import math

# Ensure the package is in the path
# Ensure the package is in the path (parent directory of scripts/)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from elysia_engine import World, Entity
from elysia_engine.physics import PhysicsWorld, Attractor
from elysia_engine.tensor import SoulTensor
from elysia_engine.math_utils import Vector3
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

def run_divine_intervention():
    print("\n=== [시나리오 3] 공허의 속삭임 (Divine Intervention) ===")
    print("당신의 의지(Text)가 디지털 세계의 물리 법칙(Physics)을 변화시킵니다.")
    print("무엇을 하고 싶으신가요? (예: 'I want to fight', 'Protect my friends')")

    intent_text = input("\n당신의 의지를 입력하세요: ")
    forces = StoryTeller.parse_intent(intent_text)

    print(f"\n[해석된 의지] Body: {forces['body']:.2f}, Soul: {forces['soul']:.2f}, Spirit: {forces['spirit']:.2f}")
    print("세계에 의지가 주입됩니다...\n")
    time.sleep(1)

    world = World()
    # Create a generic avatar to receive the user's intent
    avatar = Entity(id="UserAvatar", role="Traveler")
    # Initialize with base values so changes are visible
    avatar.f_body = 0.1
    avatar.f_soul = 0.1
    avatar.f_spirit = 0.1

    # We override the update function to ADD the user's forces continuously or one-shot?
    # For this demo, let's just set them as a bias.
    # Since Entity doesn't have a 'bias' field by default, we'll manually set them
    # and let them decay or persist depending on the simulation logic.
    # However, standard Entity.update_force_components might overwrite them if it was a subclass.
    # The base Entity class doesn't overwrite force components in update_force_components (it's empty).

    avatar.f_body += forces['body']
    avatar.f_soul += forces['soul']
    avatar.f_spirit += forces['spirit']

    world.add_entity(avatar)

    print("--- 시뮬레이션 시작 (5초간 진행) ---")
    try:
        for _ in range(10): # 10 steps * 0.5s = 5 seconds
            world.step(dt=0.5)
            snap = world.export_persona_snapshot()
            story = StoryTeller.narrate_frame(snap)
            print(story)
            time.sleep(0.5)
    except KeyboardInterrupt:
        pass

    print("\n의지가 세계에 흔적을 남겼습니다.")
    time.sleep(1)

def run_quantum_logic_demo():
    print("\n=== [시나리오 4] 양자 논리 토폴로지 (Quantum Logic Topology) ===")
    print("입력된 텍스트가 '물리적 실체'가 되어, 의미의 중력장으로 낙하합니다.")
    print("가능한 결말(Attractor): [전투(War, Left)], [평화(Peace, Right)], [마법(Magic, Up)]")

    text = input("\n의도를 입력하세요 (예: 'I want to kill', 'love and peace', 'cast fireball'): ")
    if not text: text = "void"
    entity = StoryTeller.create_intent_entity(text)

    print(f"\n[생성된 텐서] Freq: {entity.soul.frequency:.1f}Hz, Amp: {entity.soul.amplitude:.1f}")

    # Setup Physics World
    p_world = PhysicsWorld()

    # 1. War Attractor (Red/High Freq, Position -10)
    war = Attractor(id="War", position=Vector3(-10, 0, 0), mass=500.0,
                    soul=SoulTensor(amplitude=500, frequency=150, phase=0))
    p_world.add_attractor(war)

    # 2. Peace Attractor (Green/Low Freq, Position +10)
    peace = Attractor(id="Peace", position=Vector3(10, 0, 0), mass=500.0,
                      soul=SoulTensor(amplitude=500, frequency=40, phase=0))
    p_world.add_attractor(peace)

    # 3. Magic Attractor (Violet/Ultra Freq, Position 0, +10)
    magic = Attractor(id="Magic", position=Vector3(0, 10, 0), mass=500.0,
                      soul=SoulTensor(amplitude=500, frequency=350, phase=math.pi))
    p_world.add_attractor(magic)

    # Register Entity
    p_world.register_entity(entity)

    print("--- 시뮬레이션 시작 (결정이 내려질 때까지) ---")

    step = 0
    final_decision = None

    try:
        while step < 100:
            step += 1
            # Apply Physics
            # Note: Entity.apply_physics updates velocity and position
            entity.apply_physics(coil=None, world_physics=p_world, dt=0.1)

            pos = entity.physics.position
            # Simple visualization
            # War <--- (-10) --- (0) --- (+10) ---> Peace
            #                    |
            #                  Magic

            print(f"Tick {step}: Pos({pos.x:.2f}, {pos.y:.2f})", end="")

            # Check for Collapse/Capture
            captured = False
            for att in [war, peace, magic]:
                dist = (att.position - pos).magnitude
                if dist < 2.0: # Event Horizon
                    print(f" -> Captured by [{att.id}]!")
                    entity.soul.collapse()
                    final_decision = att.id
                    captured = True
                    break

            if captured:
                break

            print(" -> Drifting...")
            time.sleep(0.1)

    except KeyboardInterrupt:
        pass

    if final_decision:
        print(f"\n결과: 당신의 의도는 [{final_decision}]으로 확정되었습니다.")
        print(f"최종 상태: {entity.soul.decode_emotion()}")
    else:
        print(f"\n결과: 의도가 갈 곳을 잃고 공허로 흩어졌습니다.")

    time.sleep(2)

def main():
    while True:
        try:
            print("\n" + "="*40)
            print("   🌌 엘리시아 엔진 인터랙티브 런처 🌌")
            print("="*40)
            print("1. 세 영웅의 이야기 (Story Mode)")
            print("2. 단순한 호흡 (Visual Mode)")
            print("3. 공허의 속삭임 (Divine Intervention)")
            print("4. 양자 논리 토폴로지 (Quantum Logic)")
            print("5. 종료 (Exit)")
            print("-" * 40)

            choice = input("선택을 입력하세요 (1-5): ").strip()

            if choice == "1":
                run_three_heroes()
            elif choice == "2":
                run_simple_pulse()
            elif choice == "3":
                run_divine_intervention()
            elif choice == "4":
                run_quantum_logic_demo()
            elif choice == "5":
                print("엘리시아 엔진을 종료합니다. 안녕히 가세요!")
                break
            else:
                print("잘못된 입력입니다. 다시 선택해주세요.")
        except KeyboardInterrupt:
            # Handle Ctrl+C at menu level gracefully
            print("\n종료하려면 3번을 선택하세요.")

if __name__ == "__main__":
    main()
