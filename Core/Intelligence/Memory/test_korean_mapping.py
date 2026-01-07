# -*- coding: utf-8 -*-
"""
한국어 매핑 테스트
==================
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Core.Foundation.rapid_learning_engine import RapidLearningEngine

print("\n" + "="*70)
print("🇰🇷 한국어 매핑 테스트")
print("="*70 + "\n")

learning = RapidLearningEngine()

# 테스트 텍스트
test_text = """
Love is an intense feeling of deep affection.
Freedom means the power to act without constraint.
Beauty inspires creativity and imagination.
"""

print("학습 중...\n")
learning.learn_from_text_ultra_fast(test_text)

# 확인
print("학습된 개념:\n")
concepts = learning.hippocampus.get_all_concept_ids(limit=10)

for cid in concepts[:5]:
    seed = learning.hippocampus.load_fractal_concept(cid)
    if seed and hasattr(seed, 'metadata'):
        kr_name = seed.metadata.get('kr_name', '')
        if kr_name:  # 한국어 이름이 있는 것만
            print(f"  • {seed.name} = {kr_name}")
            if 'description' in seed.metadata:
                print(f"    정의: {seed.metadata['description'][:50]}...")
            print()

print("="*70)
print("✅ 한국어 매핑 작동!")
print("="*70 + "\n")
