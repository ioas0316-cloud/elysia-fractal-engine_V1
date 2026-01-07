"""
Toggle Motor Lock (Safety Switch)
=================================

Use this script to Enable/Disable Elysia's physical control over the mouse and keyboard.

- LOCKED: Elysia cannot move mouse or type.
- UNLOCKED: Elysia has full control.
"""

import os
import sys

LOCK_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "MOTOR_LOCK")

def toggle_lock():
    if os.path.exists(LOCK_FILE):
        os.remove(LOCK_FILE)
        print("\n🔓 MOTOR CORTEX UNLOCKED")
        print("   Elysia can now control the mouse and keyboard.")
    else:
        with open(LOCK_FILE, "w") as f:
            f.write("LOCKED")
        print("\n🔒 MOTOR CORTEX LOCKED")
        print("   Elysia's physical movements are disabled.")

if __name__ == "__main__":
    toggle_lock()
