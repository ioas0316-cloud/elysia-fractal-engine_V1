import sys
import os
import logging

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Core.Foundation.language_center import LanguageCenter

# Configure Logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("OsmosisTest")

def test_cultural_osmosis():
    print("\n🎭 Testing Cultural Osmosis (Mode Switching)...")
    
    lc = LanguageCenter()
    
    # 1. Test Epic Mode (Fantasy)
    print("\n  ⚔️  Testing 'Epic' Mode...")
    # Use raw text for testing
    epic_text = "The ancient dragon slumbered beneath the mountain, its scales shimmering like obsidian in the gloom. A thousand years had passed since the last age of heroes."
    result_epic = lc.hyper_evolve(years=1, data_source=epic_text, mode="epic")
    print(f"  Result: {result_epic}")
    
    if "optimized for 'epic'" in result_epic:
        print("  ✅ SUCCESS: Epic Mode activated.")
        # Verify Physics Constants (Simulated check)
        if lc.magnetic_engine.gravity_constant == 2.0:
            print("  ✅ Physics: High Gravity confirmed.")
        else:
            print(f"  ❌ Physics Mismatch: Gravity is {lc.magnetic_engine.gravity_constant}")
    else:
        print("  ❌ FAILURE: Epic Mode activation failed.")

    # 2. Test Drama Mode (K-Drama)
    print("\n  🎭 Testing 'Drama' Mode...")
    drama_text = "Oppa, why didn't you call me? I waited all night! You always do this. It's not about the time, it's about your heart."
    result_drama = lc.hyper_evolve(years=1, data_source=drama_text, mode="drama")
    print(f"  Result: {result_drama}")
    
    if "optimized for 'drama'" in result_drama:
        print("  ✅ SUCCESS: Drama Mode activated.")
        # Verify Physics Constants
        if lc.magnetic_engine.dark_matter_density == 2.0:
            print("  ✅ Physics: High Dark Matter (Context) confirmed.")
        else:
            print(f"  ❌ Physics Mismatch: Dark Matter is {lc.magnetic_engine.dark_matter_density}")
    else:
        print("  ❌ FAILURE: Drama Mode activation failed.")

if __name__ == "__main__":
    test_cultural_osmosis()
