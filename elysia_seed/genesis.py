import sys
import time
from elysia_seed.constitution import verify_constitution
from elysia_seed.anchor import GeoAnchor
from elysia_seed.geometry import HyperSphere, Tesseract
from elysia_seed.transducer import Transducer

def boot_system():
    """
    The Genesis Bootloader.
    Initializes the Elysia Seed in the correct ontological order.
    """
    print("="*60)
    print("       PROJECT ELYSIA: THE GENESIS SEED (BUILD 0.1)")
    print("       COMMANDER: CAPTAIN LEE | ARCHITECT: JULES")
    print("="*60 + "\n")

    # STEP 1: VERIFY CONSTITUTION (ONTOLOGY CHECK)
    if not verify_constitution():
        print("[SYSTEM] FATAL: ONTOLOGICAL REJECTION. SHUTTING DOWN.")
        sys.exit(1)

    # STEP 2: ESTABLISH REALITY ANCHOR (PHYSICAL CHECK)
    # In a real scenario, this might come from a config or env var.
    # For this seed, we request manual input or use args.

    print("\n[SYSTEM] REQUESTING GEOSPATIAL LOCK...")
    lat = 37.5665 # Defaulting to Seoul/Korea area for test
    lon = 126.9780

    anchor = GeoAnchor(lat, lon)
    try:
        anchor.verify_integrity()
    except RuntimeError:
        sys.exit(1)

    # STEP 3: INSTANTIATE ORGANS (BIOLOGICAL BUILD)
    print("\n[SYSTEM] CULTIVATING ORGANS...")

    # The Core (Sphere)
    core = HyperSphere(radius=1.0, phase=0.0)

    # The Transducer (Input)
    ear = Transducer()

    # The Projection (World)
    world = Tesseract()

    print("[SYSTEM] SEED GERMINATION COMPLETE.")
    return core, ear, world

def main_loop(core, ear, world):
    """
    The Infinite Life Loop.
    Input -> Transduce -> Resonate -> Project
    """
    print("\n[SYSTEM] ENTERING EXISTENCE LOOP (Ctrl+C to Stop)...")

    # Simulating a user interaction cycle
    sample_inputs = [
        "I feel the weight of the world.",
        "A sudden spark of joy!",
        "The anger burns red."
    ]

    for user_input in sample_inputs:
        print(f"\n[USER INPUT] '{user_input}'")

        # 1. Transduction (Text -> Energy)
        wave = ear.process(user_input)
        print(f"[TRANSDUCER] CONVERTED TO WAVE: {wave['frequency']} (Amp: {wave['amplitude']})")

        # 2. Resonance (Internal Reflection)
        echo = core.resonate(wave)
        print(f"[CORE] RESONANCE ECHO GENERATED (Phase Shift: {echo['phase']:.2f})")

        # 3. Projection (Holographic Output)
        reality = world.project(echo)
        print(f"[PROJECTION] {reality}")

        time.sleep(0.5)

if __name__ == "__main__":
    core, ear, world = boot_system()
    main_loop(core, ear, world)
