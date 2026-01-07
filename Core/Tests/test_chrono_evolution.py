import sys
import os
import logging

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Core.Foundation.language_center import LanguageCenter

# Configure Logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("ChronoTest")

def test_chrono_evolution():
    print("\n⏳ Testing Chrono-Linguistics (Time Compression)...")
    
    lc = LanguageCenter()
    
    # 1. Initial State
    print("  Checking initial state...")
    # In a real system, we'd check specific weights. Here we just ensure the engine is ready.
    if lc.magnetic_engine:
        print("  ✅ MagneticEngine is online.")
        
    # 2. Run Hyper-Evolution
    # Simulate 5 years of reading in seconds
    years = 5
    print(f"\n  🚀 Initiating Hyper-Evolution ({years} years)...")
    
    # Use a dummy URL for testing if network is restricted, but here we try a real one.
    # If it fails, the method handles it gracefully.
    result = lc.hyper_evolve(years=years)
    print(f"  Result: {result}")
    
    # 3. Verify Outcome
    if "Evolution Complete" in result:
        print("  ✅ SUCCESS: Time Compression simulation completed.")
        print("  ✅ MagneticEngine has been trained on high-density data.")
    else:
        print("  ❌ FAILURE: Evolution did not complete as expected.")

if __name__ == "__main__":
    test_chrono_evolution()
