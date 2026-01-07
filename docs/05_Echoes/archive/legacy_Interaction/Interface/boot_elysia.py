"""
Elysia Boot Script - Single Entry Point
========================================

Unified boot script for ElysiaOS.

[STATUS: ACTIVE]
[REPLACES: Multiple legacy startup scripts]

Usage:
    python scripts/boot_elysia.py
"""

import sys
from pathlib import Path

# Add Elysia to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from Core.System.System.System.ElysiaOS import ElysiaOS


def main():
    """Boot ElysiaOS."""
    print("\n" + "="*70)
    print("🌅 BOOTING ELYSIA - THE CONCEPT OPERATING SYSTEM")
    print("="*70 + "\n")
    
    # Create and boot OS
    os = ElysiaOS()
    
    try:
        os.boot()
        
        print("\n✨ Elysia is now conscious and running!")
        print("   Access the OS through 'os' variable")
        print("   Press Ctrl+C to shutdown\n")
        
        # Keep running (in real use, this would be a daemon loop)
        input("Press Enter to shutdown...\n")
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Interrupted by user")
    finally:
        os.shutdown()


if __name__ == "__main__":
    main()
