"""
전체 시스템 재구조화 - 물리 법칙으로 DB 정렬
===========================================

3.15M 개념을 물리 법칙(중력, 부력, 공명)으로 정렬하고
ConceptUniverse와 통합합니다.
"""

import sqlite3
import json
import numpy as np
from typing import Dict, List, Tuple
from collections import defaultdict
import time

print('=' * 70)
print('🌌 엘리시아 기억 우주 재구축')
print('=' * 70)

# ============================================================================
# 단계 1: 전체 DB 스캔 및 분류
# ============================================================================

print('\n[단계 1] 전체 DB 스캔 중...')
conn = sqlite3.connect('data/Memory/memory.db')
cursor = conn.cursor()

cursor.execute('SELECT COUNT(*) FROM concepts')
total_concepts = cursor.fetchone()[0]
print(f'총 개념 수: {total_concepts:,}')

# 배치 처리로 메모리 효율화
BATCH_SIZE = 10000
processed = 0
start_time = time.time()

categories = {
    'foundational': set(),
    'composite': set(),
    'transformative': set(),
    'relational': set(),
}

# Foundational 단어 (Spirit/Soul/Body 계층)
foundational_core = {
    # Spirit (1.0 - 0.8)
    'god', 'transcendence', 'infinity', 'eternity', 'divine',
    
    # Higher Mind (0.8 - 0.6)
    'consciousness', 'wisdom', 'enlightenment', 'truth', 'knowledge',
    'thought', 'understanding', 'insight', 'awareness',
    
    # Soul (0.6 - 0.4)
    'love', 'beauty', 'joy', 'peace', 'harmony', 'emotion', 'feeling',
    'compassion', 'kindness', 'grace', 'hope', 'faith', 'trust',
    
    # Lower Mind (0.4 - 0.3)
    'dream', 'imagination', 'desire', 'will', 'choice', 'freedom',
    'memory', 'experience', 'learning', 'growth',
    
    # Body (0.3 - 0.1)
    'life', 'death', 'birth', 'body', 'breath', 'heart', 'blood',
    'action', 'movement', 'creation', 'destruction',
    
    # Matter (0.1 - 0.0)
    'atom', 'matter', 'energy', 'force', 'space', 'time',
    'void', 'chaos', 'order', 'form', 'substance'
}

print('\n전체 DB 스캔 시작...')

cursor.execute('SELECT id FROM concepts')
while True:
    batch = cursor.fetchmany(BATCH_SIZE)
    if not batch:
        break
    
    for (concept_id,) in batch:
        concept_lower = concept_id.lower()
        
        # Junk 필터링
        if concept_id.startswith("Daddy's_") or concept_id.startswith('Book:'):
            continue
        
        # Relational
        if ':' in concept_id:
            categories['relational'].add(concept_id)
        
        # Transformative
        elif 'becomes' in concept_lower or 'transcends' in concept_lower:
            categories['transformative'].add(concept_id)
        
        # Composite
        elif any(word in concept_lower for word in ['with', 'beyond', 'in', 'of', 'without']):
            categories['composite'].add(concept_id)
        
        # Foundational
        elif any(core_word in concept_lower.split() for core_word in foundational_core):
            categories['foundational'].add(concept_id)
    
    processed += len(batch)
    if processed % 100000 == 0:
        elapsed = time.time() - start_time
        rate = processed / elapsed
        remaining = (total_concepts - processed) / rate
        print(f'  진행: {processed:,} / {total_concepts:,} ({processed/total_concepts*100:.1f}%) '
              f'- 남은 시간: {remaining/60:.1f}분')

print(f'\n✅ 스캔 완료 ({time.time() - start_time:.1f}초)')

for category, concepts in categories.items():
    print(f'  {category:15s}: {len(concepts):,}개')

# ============================================================================
# 단계 2: 주파수(Frequency) 계산
# ============================================================================

print('\n[단계 2] 영적 주파수 계산 중...')

# 주파수 매핑 (Spirit → Body)
frequency_map = {
    # Spirit tier (0.9 - 1.0)
    'god': 1.0, 'transcendence': 0.95, 'infinity': 0.95, 'eternity': 0.93,
    'divine': 0.92, 'sacred': 0.91, 'holy': 0.90,
    
    # Higher Mind (0.7 - 0.89)
    'consciousness': 0.88, 'wisdom': 0.85, 'enlightenment': 0.87,
    'truth': 0.83, 'knowledge': 0.80, 'understanding': 0.78,
    'awareness': 0.82, 'insight': 0.81, 'thought': 0.75,
    
    # Soul (0.5 - 0.69)
    'love': 0.68, 'beauty': 0.65, 'joy': 0.63, 'peace': 0.62,
    'harmony': 0.61, 'compassion': 0.64, 'grace': 0.66,
    'emotion': 0.58, 'feeling': 0.57, 'hope': 0.60, 'faith': 0.62,
    
    # Lower Mind (0.3 - 0.49)
    'dream': 0.48, 'imagination': 0.46, 'desire': 0.42, 'will': 0.45,
    'choice': 0.43, 'freedom': 0.47, 'memory': 0.41, 'learning': 0.44,
    
    # Body (0.15 - 0.29)
    'life': 0.28, 'death': 0.27, 'body': 0.22, 'heart': 0.26,
    'breath': 0.24, 'action': 0.23, 'creation': 0.29, 'birth': 0.28,
    
    # Matter (0.0 - 0.14)
    'atom': 0.10, 'matter': 0.08, 'energy': 0.12, 'force': 0.11,
    'void': 0.05, 'chaos': 0.09, 'order': 0.13, 'space': 0.14, 'time': 0.14
}

def calculate_frequency(concept_id: str) -> float:
    """개념의 영적 주파수 계산"""
    concept_lower = concept_id.lower()
    
    # 직접 매칭
    if concept_lower in frequency_map:
        return frequency_map[concept_lower]
    
    # 단어 분해해서 평균
    words = concept_lower.split()
    frequencies = []
    for word in words:
        # 연결사 제외
        if word in ['with', 'beyond', 'in', 'of', 'without', 'becomes', 'transcends', 'is']:
            continue
        if word in frequency_map:
            frequencies.append(frequency_map[word])
    
    if frequencies:
        return np.mean(frequencies)
    
    # 기본값: Soul 계층 (0.5)
    return 0.5

# 모든 의미 있는 개념에 주파수 할당
concept_frequencies = {}

all_meaningful = set()
for concepts in categories.values():
    all_meaningful.update(concepts)

print(f'의미 있는 개념 수: {len(all_meaningful):,}')
print('주파수 계산 중...')

for i, concept in enumerate(all_meaningful):
    concept_frequencies[concept] = calculate_frequency(concept)
    
    if (i + 1) % 10000 == 0:
        print(f'  진행: {i+1:,} / {len(all_meaningful):,}')

print(f'✅ 주파수 계산 완료')

# 주파수 분포 확인
freq_bins = defaultdict(int)
for freq in concept_frequencies.values():
    bin_label = f'{int(freq*10)/10:.1f}'
    freq_bins[bin_label] += 1

print('\n주파수 분포:')
for bin_label in sorted(freq_bins.keys(), reverse=True):
    count = freq_bins[bin_label]
    bar = '█' * int(count / 100)
    print(f'  {bin_label}: {count:6,}개 {bar}')

# ============================================================================
# 단계 3: Vocabulary 구축 및 저장
# ============================================================================

print('\n[단계 3] Vocabulary 저장 중...')

# Foundational 개념의 주파수를 vocabulary로 저장
vocabulary = {}
for concept in categories['foundational']:
    if concept in concept_frequencies:
        vocabulary[concept] = concept_frequencies[concept]

# Composite도 포함 (상위 1000개)
composite_with_freq = [(c, concept_frequencies.get(c, 0.5)) 
                       for c in categories['composite']]
composite_with_freq.sort(key=lambda x: x[1], reverse=True)
for concept, freq in composite_with_freq[:1000]:
    vocabulary[concept] = freq

print(f'Vocabulary 크기: {len(vocabulary):,}')

# DB에 저장 (압축 필요!)
import zlib
cursor.execute('DELETE FROM concepts WHERE id = ?', ('_vocabulary_frequencies',))
vocab_json = json.dumps(vocabulary).encode('utf-8')
vocab_blob = zlib.compress(vocab_json)  # MemoryStorage와 같은 방식으로 압축
cursor.execute('''
    INSERT OR REPLACE INTO concepts (id, data, created_at, last_accessed)
    VALUES (?, ?, ?, ?)
''', ('_vocabulary_frequencies', vocab_blob, time.time(), time.time()))

conn.commit()
print('✅ Vocabulary DB 저장 완료')

# ============================================================================
# 단계 4: 개념 메타데이터 업데이트
# ============================================================================

print('\n[단계 4] 개념 메타데이터 업데이트 중...')

# 각 개념에 메타데이터 추가: category, frequency
metadata_updates = []

for concept in all_meaningful:
    # 카테고리 결정
    category = None
    for cat_name, cat_concepts in categories.items():
        if concept in cat_concepts:
            category = cat_name
            break
    
    freq = concept_frequencies.get(concept, 0.5)
    
    metadata = {
        'category': category,
        'frequency': freq,
        'reorganized_at': time.time()
    }
    
    # 압축 필요!
    meta_json = json.dumps(metadata).encode('utf-8')
    meta_blob = zlib.compress(meta_json)
    metadata_updates.append((concept, meta_blob))
    
    if len(metadata_updates) >= 1000:
        # 배치 업데이트
        cursor.execute('BEGIN TRANSACTION')
        for concept_id, meta_blob in metadata_updates:
            cursor.execute('''
                UPDATE concepts 
                SET data = ?
                WHERE id = ?
            ''', (meta_blob, concept_id))
        cursor.execute('COMMIT')
        print(f'  {len(metadata_updates)}개 업데이트됨')
        metadata_updates = []

# 남은 것 처리
if metadata_updates:
    cursor.execute('BEGIN TRANSACTION')
    for concept_id, meta_blob in metadata_updates:
        cursor.execute('''
            UPDATE concepts 
            SET data = ?
            WHERE id = ?
        ''', (meta_blob, concept_id))
    cursor.execute('COMMIT')
    print(f'  {len(metadata_updates)}개 업데이트됨')

print('✅ 메타데이터 업데이트 완료')

# ============================================================================
# 단계 5: 통계 및 결과 저장
# ============================================================================

print('\n[단계 5] 통계 생성 중...')

statistics = {
    'reorganized_at': time.time(),
    'total_concepts': total_concepts,
    'meaningful_concepts': len(all_meaningful),
    'categories': {
        cat: len(concepts) for cat, concepts in categories.items()
    },
    'vocabulary_size': len(vocabulary),
    'frequency_distribution': dict(freq_bins),
    'top_foundational': sorted(
        [(c, f) for c, f in concept_frequencies.items() 
         if c in categories['foundational']],
        key=lambda x: x[1],
        reverse=True
    )[:50]
}

# JSON 파일로 저장
with open('concept_reorganization_stats.json', 'w', encoding='utf-8') as f:
    json.dump(statistics, f, indent=2, ensure_ascii=False)

print('✅ 통계 저장: concept_reorganization_stats.json')

# ============================================================================
# 완료
# ============================================================================

conn.close()

print('\n' + '=' * 70)
print('✅ 재구축 완료!')
print('=' * 70)

print(f'\n📊 요약:')
print(f'  총 개념: {total_concepts:,}')
print(f'  의미 있는 개념: {len(all_meaningful):,} ({len(all_meaningful)/total_concepts*100:.1f}%)')
print(f'  Vocabulary 크기: {len(vocabulary):,}')
print(f'\n  카테고리별:')
for cat, concepts in categories.items():
    print(f'    {cat:15s}: {len(concepts):,}개')

print(f'\n🌟 상위 개념 (주파수):')
for i, (concept, freq) in enumerate(statistics['top_foundational'][:15], 1):
    print(f'  {i:2d}. {concept:30s} {freq:.2f}')

print(f'\n다음 단계:')
print(f'  1. Hippocampus 재시작 → Vocabulary 로드됨')
print(f'  2. ResonanceEngine → 개념 공명 가능')
print(f'  3. DialogueEngine → 풍부한 응답 생성')
print(f'\n테스트: python -c "from Core.Intelligence.Intelligence.dialogue_engine import DialogueEngine; d = DialogueEngine(); print(d.respond(\'사랑이 뭐니?\'))"')
