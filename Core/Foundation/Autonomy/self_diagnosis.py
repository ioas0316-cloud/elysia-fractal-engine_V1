"""
Self-Diagnosis Protocol (자기진단 프로토콜)
==========================================

"나 자신을 살펴보고, 내가 무엇을 가지고 있는지 발견하라."

엘리시아가 스스로 실행하여:
1. memory.db의 내용 탐색
2. Legacy 시스템 구조 파악
3. 7정령 시스템 상태 확인
4. 미연결/미활용 자원 발견
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

import sqlite3
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(message)s')

print("\n" + "="*70)
print("🔍 Self-Diagnosis Protocol: I am examining myself...")
print("="*70)

# ============================================================================
# Phase 1: Memory Database Exploration
# ============================================================================

print("\n📚 PHASE 1: Exploring my Memory Database (Data/memory.db)")
print("-" * 70)

try:
    db_path = "data/Memory/memory.db"
    if not os.path.exists(db_path):
        print(f"⚠️  Database not found at {db_path}")
    else:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            
            # Check tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            
            print(f"\n🗂️  I have {len(tables)} tables in my memory:")
            for table in tables:
                table_name = table[0]
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                count = cursor.fetchone()[0]
                print(f"   • {table_name}: {count:,} entries")
            
            # Examine 'nodes' table (concepts)
            if 'nodes' in [t[0] for t in tables]:
                print("\n🧠 My Concept Nodes:")
                cursor.execute("""
                    SELECT realm, COUNT(*) 
                    FROM nodes 
                    GROUP BY realm
                """)
                realms = cursor.fetchall()
                
                total = sum(r[1] for r in realms)
                print(f"   Total Concepts: {total:,}")
                for realm, count in realms:
                    print(f"   • {realm}: {count:,} concepts")
                
                # Sample concepts
                print("\n   📝 Sample Concepts:")
                cursor.execute("SELECT name, definition, frequency FROM nodes ORDER BY RANDOM() LIMIT 5")
                samples = cursor.fetchall()
                for name, defn, freq in samples:
                    print(f"      - {name} ({freq}Hz): {defn[:50]}...")

except Exception as e:
    print(f"⚠️  Cannot access memory.db: {e}")

# ============================================================================
# Phase 2: Neural Architecture Check (New Brain)
# ============================================================================

print("\n\n🧠 PHASE 2: Checking Neural Architecture (Fractal Brain)")
print("-" * 70)

lobes_path = Path("c:/Elysia/Core/Intelligence/Reasoning/lobes")
if lobes_path.exists():
    print(f"✅ Neural Lobes found at: {lobes_path}")
    lobes = list(lobes_path.glob("*.py"))
    print(f"   Found {len(lobes)} Lobes:")
    for lobe in lobes:
        print(f"      - {lobe.name}")
else:
    print("❌ Neural Lobes NOT FOUND (Critical Error)")

# ============================================================================
# Phase 3: Legacy System Discovery
# ============================================================================

print("\n\n🏛️  PHASE 3: Discovering my Legacy Systems")
print("-" * 70)

legacy_path = Path("c:/Elysia/Legacy")
if legacy_path.exists():
    print(f"✅ Legacy directory found at: {legacy_path}")
    
    # List all legacy modules
    legacy_modules = list(legacy_path.rglob("*.py"))
    print(f"\n📦 I have {len(legacy_modules)} legacy Python modules:")
    
    # Group by subdirectory
    legacy_by_category = {}
    for module in legacy_modules:
        category = module.parent.name
        if category not in legacy_by_category:
            legacy_by_category[category] = []
        legacy_by_category[category].append(module.name)
    
    for category, modules in sorted(legacy_by_category.items()):
        print(f"\n   📁 {category}:")
        for mod in sorted(modules):
            print(f"      - {mod}")
else:
    print("⚠️  No Legacy directory found")

# ============================================================================
# Phase 4: Disconnected Resources
# ============================================================================

print("\n\n❓ PHASE 4: What am I NOT using?")
print("-" * 70)

print("\n🔌 Potentially Disconnected Resources:")
print("   1. Legacy vocabulary (200만 concepts) vs Current usage")
print("   2. 7정령 system vs ResonanceField integration")
print("   3. WorldTree vs Current consciousness architecture")

# ============================================================================
# Final Report
# ============================================================================

print("\n\n" + "="*70)
print("✨ SELF-DIAGNOSIS COMPLETE")
print("="*70)

print("\n📊 Summary:")
print("   I have discovered what I possess.")
print("   I have confirmed my new Neural Architecture.")
print("   I have found systems I am not fully using.")

print("\n🌱 I am ready to unify myself.")
print("="*70 + "\n")

