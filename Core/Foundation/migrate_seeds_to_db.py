import sys
import os
import json
import logging

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Core.Foundation.hippocampus import Hippocampus
from Core.Foundation.fractal_quantization import PatternDNA

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SeedMigration")

def migrate():
    print("🚀 Starting Seed Migration to Memory DB...")
    
    # 1. Initialize Hippocampus (creates tables in memory.db)
    hippocampus = Hippocampus()
    
    # 2. Load Internet Seeds
    json_path = "data/internet_pattern_dna.json"
    if not os.path.exists(json_path):
        print(f"❌ Error: {json_path} not found!")
        return
        
    with open(json_path, 'r') as f:
        data = json.load(f)
        
    seeds = data.get("seeds", {})
    print(f"📦 Found {len(seeds)} seeds in JSON.")
    
    # 3. Store in Memory DB
    for key, seed_data in seeds.items():
        # Create PatternDNA object
        # Create PatternDNA object
        from Core.Foundation.hyper_quaternion import Quaternion
        
        dna = PatternDNA(
            name=key,
            seed_formula={"formula": "Z = Z^2 + C", "constants": {"C": 0.5}},
            frequency_signature=[seed_data.get("frequency", 432.0)],
            phase_pattern=[0.0],
            amplitude_envelope=[1.0],
            resonance_fingerprint=Quaternion(1, 0, 0, 0),
            metadata={
                "source": "internet_sync",
                "essence": seed_data.get("essence"),
                "harmonics": seed_data.get("harmonics", [])
            },
            compression_ratio=1000.0
        )
        
        # Store
        hippocampus.store_pattern_dna(dna)
        print(f"   ✅ Migrated: {key}")
        
    print("\n🎉 Migration Complete!")
    print("Memory DB is now the active Pattern DNA Bank.")

if __name__ == "__main__":
    migrate()
