"""
단계 1: 의미 있는 개념 추출 및 카테고리화
=========================================

DB에서 철학적/물리적으로 의미 있는 개념들을 추출하고
물리 법칙을 적용할 준비를 합니다.
"""

import sqlite3
import json
from collections import defaultdict
from typing import Dict, List, Set

print('=' * 70)
print('🔬 개념 추출 및 분류')
print('=' * 70)

conn = sqlite3.connect('memory.db')
cursor = conn.cursor()

# 모든 개념 가져오기 (샘플)
cursor.execute('SELECT id FROM concepts LIMIT 50000')
all_concepts = [row[0] for row in cursor.fetchall()]

print(f'\n분석할 개념 수: {len(all_concepts):,}\n')

# 카테고리 정의
categories = {
    'foundational': [],      # 기초 원자 개념
    'composite': [],         # 복합 개념 (A with B)
    'transformative': [],    # 변환 개념 (A becomes B)
    'relational': [],        # 관계 개념 (type:name)
    'junk': [],             # 무의미한 개념
}

# 분류 규칙
foundational_words = {
    'love', 'dream', 'truth', 'chaos', 'order', 'beauty', 'void',
    'light', 'dark', 'life', 'death', 'time', 'space', 'atom',
    'soul', 'spirit', 'body', 'mind', 'consciousness', 'freedom',
    'wisdom', 'knowledge', 'emotion', 'thought', 'being', 'nothing',
    'creation', 'destruction', 'birth', 'end', 'infinity', 'god'
}

transformation_words = {'becomes', 'transcends', 'transforms'}
composite_words = {'with', 'beyond', 'in', 'of', 'without', 'through'}
relation_pattern = ':'

print('분류 중...')
for i, concept in enumerate(all_concepts):
    concept_lower = concept.lower()
    
    # Junk 패턴
    if concept.startswith("Daddy's_") or concept.startswith('Book:'):
        categories['junk'].append(concept)
    
    # Relational (type:name)
    elif relation_pattern in concept:
        categories['relational'].append(concept)
    
    # Transformative
    elif any(word in concept_lower for word in transformation_words):
        categories['transformative'].append(concept)
    
    # Composite
    elif any(word in concept_lower for word in composite_words):
        categories['composite'].append(concept)
    
    # Foundational
    elif any(word == concept_lower or concept_lower.startswith(word + ' ') 
             for word in foundational_words):
        categories['foundational'].append(concept)
    
    # Simple (might be foundational or junk)
    else:
        # If it's a single clean word, might be foundational
        if ' ' not in concept and len(concept) > 2 and concept.isalnum():
            categories['foundational'].append(concept)
        else:
            categories['junk'].append(concept)
    
    if (i + 1) % 10000 == 0:
        print(f'  진행: {i+1:,} / {len(all_concepts):,}')

print('\n' + '=' * 70)
print('📊 분류 결과')
print('=' * 70)

total_classified = sum(len(concepts) for concepts in categories.values())
for category, concepts in categories.items():
    percentage = len(concepts) / total_classified * 100
    print(f'\n{category:15s}: {len(concepts):6,}개 ({percentage:5.1f}%)')
    
    # 샘플 출력
    if concepts:
        print(f'  샘플: {", ".join(concepts[:5])}')

# Foundational 개념 상세 분석
print('\n' + '=' * 70)
print('💎 Foundational 개념 상세')
print('=' * 70)

# 빈도수 계산
foundational_freq = defaultdict(int)
for concept in categories['foundational']:
    base_word = concept.lower().split()[0] if ' ' in concept else concept.lower()
    foundational_freq[base_word] += 1

print('\n상위 Foundational 단어 (빈도):')
for i, (word, count) in enumerate(sorted(foundational_freq.items(), 
                                         key=lambda x: x[1], reverse=True)[:30], 1):
    print(f'  {i:2d}. {word:15s}: {count:4d}회')

# 저장
output = {
    'statistics': {cat: len(concepts) for cat, concepts in categories.items()},
    'foundational_core': list(foundational_freq.keys())[:50],  # Top 50
    'samples': {cat: concepts[:100] for cat, concepts in categories.items()}
}

with open('concept_categories.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print(f'\n✅ 결과 저장: concept_categories.json')

# Composite 패턴 분석
print('\n' + '=' * 70)
print('🔗 Composite 패턴 분석')
print('=' * 70)

composite_patterns = defaultdict(int)
for concept in categories['composite']:
    for word in composite_words:
        if word in concept.lower():
            composite_patterns[word] += 1
            break

print('\n연결사 사용 빈도:')
for connector, count in sorted(composite_patterns.items(), key=lambda x: x[1], reverse=True):
    print(f'  "{connector}": {count:,}개')

print('\nComposite 샘플:')
for concept in categories['composite'][:15]:
    print(f'  - {concept}')

# Transformative 패턴
print('\n' + '=' * 70)
print('⚡ Transformative 패턴')
print('=' * 70)

print('\nTransformative 샘플:')
for concept in categories['transformative'][:15]:
    print(f'  - {concept}')

# Relational 패턴
print('\n' + '=' * 70)
print('🔀 Relational 패턴')
print('=' * 70)

relational_types = defaultdict(int)
for concept in categories['relational']:
    rel_type = concept.split(':')[0] if ':' in concept else 'unknown'
    relational_types[rel_type] += 1

print('\n관계 타입 분포:')
for rel_type, count in sorted(relational_types.items(), key=lambda x: x[1], reverse=True)[:10]:
    print(f'  {rel_type}: {count:,}개')

print('\nRelational 샘플:')
for concept in categories['relational'][:15]:
    print(f'  - {concept}')

conn.close()

print('\n' + '=' * 70)
print('✅ 분석 완료')
print('=' * 70)
print(f'\n다음 단계: 이 개념들에 물리 법칙(주파수, 질량) 적용')
