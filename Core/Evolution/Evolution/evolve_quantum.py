import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from Core.Foundation.cortex_optimizer import CortexOptimizer

def trigger_evolution():
    print("🧬 Initiating Manual Evolution Protocol (Quantum Port)...")
    optimizer = CortexOptimizer()
    
    # Find the draft
    draft_path = os.path.join(optimizer.draft_path, "quantum_protocol_v1.py")
    
    # Target location (New file in Interface)
    # CortexOptimizer.apply_evolution merges into existing files, 
    # but for a new file we might need a slight tweak or just copy it manually here for the demo.
    # Let's assume apply_evolution handles it or we force it.
    
    target_path = os.path.join(optimizer.root_path, "Core", "Interface", "quantum_protocol.py")
    
    if os.path.exists(draft_path):
        print(f"   📄 Found Draft: {draft_path}")
        print("   ⚙️ Merging into Core System...")
        
        with open(draft_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        with open(target_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f"✅ Evolution Applied! {target_path} has been created.")
    else:
        print("❌ No draft found.")

if __name__ == "__main__":
    trigger_evolution()
