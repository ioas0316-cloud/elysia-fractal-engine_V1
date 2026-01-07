"""
ConsciousnessConsole - Talk to UnifiedConsciousness with temporal modes.

Features:
- Switch temporal mode: past_heavy / present_heavy / future_heavy / balanced
- Send a line of text and watch:
  - Perception + Emotion
  - Fractal Time Engine (Past/Present/Future phase)
  - Self-model snapshot (Yggdrasil)

This is a lightweight CLI wrapper around `unified_consciousness_prototype.UnifiedConsciousness`.
"""

import os
import sys
from typing import Optional

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from unified_consciousness_prototype import UnifiedConsciousness  # type: ignore


MODES = ["balanced", "past_heavy", "present_heavy", "future_heavy"]


def _print_help() -> None:
    print("\nCommands:")
    print("  /mode <name>    - set temporal mode "
          f"({', '.join(MODES)})")
    print("  /whoami         - print current self-model snapshot")
    print("  /w <value>      - dummy zoom hint (macro/meso/micro label only)")
    print("  /quit           - exit console")
    print("  /help           - show this help\n")


def _label_zoom(w: float) -> str:
    if w >= 2.0:
        return "MACRO (cells / past / body)"
    if w >= 1.0:
        return "MESO (molecules / present / mind)"
    return "MICRO (atoms+photons / future / spirit)"


def run_console() -> None:
    print("=== Elysia Consciousness Console ===")
    print("Initializing UnifiedConsciousness...\n")

    consciousness = UnifiedConsciousness()
    current_w: float = 2.0  # zoom hint only (not yet wired to render_level)

    print(f"Current temporal mode: {consciousness.temporal_mode}")
    print(f"Current zoom (w): {current_w:.1f} -> {_label_zoom(current_w)}")
    _print_help()

    while True:
        try:
            line = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            break

        if not line:
            continue

        if line.startswith("/"):
            parts = line.split()
            cmd = parts[0].lower()

            if cmd == "/quit":
                print("Goodbye.")
                break

            if cmd == "/help":
                _print_help()
                continue

            if cmd == "/mode":
                if len(parts) < 2:
                    print(f"Usage: /mode <{'|'.join(MODES)}>")
                    continue
                mode = parts[1]
                if mode not in MODES:
                    print(f"Unknown mode '{mode}'. Available: {', '.join(MODES)}")
                    continue
                try:
                    consciousness.set_temporal_mode(mode)
                    print(f"Temporal mode set to: {mode}")
                except Exception as e:
                    print(f"Failed to set mode: {e}")
                continue

            if cmd == "/whoami":
                print("\n--- SELF-MODEL SNAPSHOT ---")
                print(consciousness.introspect())
                print("--- END ---\n")
                continue

            if cmd == "/w":
                if len(parts) < 2:
                    print("Usage: /w <float>")
                    continue
                try:
                    current_w = float(parts[1])
                except ValueError:
                    print("w must be a number (e.g., 0.0, 1.0, 2.0)")
                    continue
                print(f"Zoom set to w={current_w:.2f} -> {_label_zoom(current_w)}")
                # Future: hook this into FractalUniverse.render_level(w)
                continue

            print("Unknown command. Type /help for options.")
            continue

        # Regular text -> consciousness cycle
        consciousness.listen_and_respond(line)


if __name__ == "__main__":
    run_console()

