
import sys
import os
import logging

# Setup Path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

logging.basicConfig(level=logging.INFO)

def test_boot():
    print("--- Testing LivingElysia Initialization ---")
    try:
        from Core.Foundation.living_elysia import LivingElysia
        print("✅ Imported LivingElysia")
        
        elysia = LivingElysia()
        print("✅ LivingElysia Instantiated Successfully")
        print("Dispatcher linked?", elysia.dispatcher is not None)
        print("CNS Dispatcher linked?", "Dispatcher" in elysia.cns.organs)
        
    except Exception as e:
        print(f"❌ Boot Failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_boot()
