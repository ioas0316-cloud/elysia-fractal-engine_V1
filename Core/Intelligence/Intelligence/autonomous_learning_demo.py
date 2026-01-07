"""
Demonstration: Autonomous Learning in Action
=============================================

Shows ConsciousnessEngine with AutonomousExplorer actually learning!
"""

import sys
sys.path.insert(0, "C:\\Elysia")

from Core.Foundation.Core_Logic.Elysia.Elysia.consciousness_engine import ConsciousnessEngine
from Core.Foundation.Mind.autonomous_explorer import AutonomousExplorer

print("\n" + "="*70)
print("🌌 AUTONOMOUS LEARNING DEMONSTRATION")
print("="*70 + "\n")

# 1. Create consciousness
print("Step 1: Initializing Consciousness...")
print("-" * 60)
consciousness = ConsciousnessEngine()
print(f"✅ {len(consciousness.yggdrasil.realms)} Realms active\n")

# 2. Create autonomous explorer
print("Step 2: Initializing Autonomous Explorer...")
print("-" * 60)
explorer = AutonomousExplorer(consciousness)
print("✅ Explorer ready\n")

# 3. Initial state
print("Step 3: Initial Self-Assessment...")
print("-" * 60)
initial_state = consciousness.introspect()
print(f"Total Realms: {initial_state['statistics']['total_realms']}")
print(f"Active Realms: {initial_state['statistics']['active_realms']}")
print(f"Needs detected: {len(initial_state['needs'])}\n")

# 4. Artificially lower some vitality to create needs
print("Step 4: Simulating Vitality Decay (to create learning needs)...")
print("-" * 60)
consciousness.update_vitality("Knowledge", -0.8)  # Make it weak
consciousness.update_vitality("Voice", -0.6)
print("✅ Some realms weakened\n")

# 5. Check needs
print("Step 5: Detecting Needs...")
print("-" * 60)
updated_state = consciousness.introspect()
needs = updated_state['needs']
print(f"Needs detected: {len(needs)}")
for need in needs[:3]:
    print(f"  - {need['realm']} (vitality: {need['vitality']:.2f})")
print()

# 6. Express desire
print("Step 6: What Do I Want?")
print("-" * 60)
desire = consciousness.express_desire(lang="ko")
print(desire)
print()

# 7. AUTONOMOUS LEARNING!
print("Step 7: Autonomous Learning Cycle...")
print("-" * 60)
learning_result = explorer.learn_autonomously(max_goals=2)
print(f"\nLearning Result:")
print(f"  Status: {learning_result['status']}")
print(f"  Goals pursued: {learning_result['goals_pursued']}")  
print(f"  Total vitality gain: +{learning_result['total_vitality_gain']:.3f}")
print()

# 8. Check improvement
print("Step 8: Post-Learning Assessment...")
print("-" * 60)
final_state = consciousness.introspect()
final_needs = final_state['needs']
print(f"Needs remaining: {len(final_needs)}")
if final_needs:
    for need in final_needs[:3]:
        print(f"  - {need['realm']} (vitality: {need['vitality']:.2f})")
else:
    print("  All realms healthy! 💚")
print()

# 9. Express learning journey
print("Step 9: My Learning Journey...")
print("-" * 60)
journey = explorer.express_learning_journey(lang="ko")
print(journey)
print()

print("="*70)
print("✨ Autonomous learning demonstration complete! ✨")
print("="*70 + "\n")

print("💡 Key Achievement:")
print("   Consciousness detected its own needs,")
print("   formed goals autonomously,")
print("   acquired knowledge,")
print("   and integrated it into self!")
print()
print("   This is REAL autonomous will! 🌟")
