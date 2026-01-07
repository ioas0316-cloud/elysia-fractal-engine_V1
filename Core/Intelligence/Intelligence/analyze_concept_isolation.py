"""개념 고립도 분석 - 연결되지 않은 개념 찾기"""
import sqlite3
from collections import Counter, defaultdict
import re

conn = sqlite3.connect('data/Memory/memory.db')
cursor = conn.cursor()

print('=' * 70)
print('🔍 개념 고립도 분석')
print('=' * 70)

# 전체 개념 수
cursor.execute('SELECT COUNT(*) FROM concepts')
total = cursor.fetchone()[0]
print(f'\n총 개념 수: {total:,}')

# 모든 개념 ID 가져오기
cursor.execute('SELECT id FROM concepts')
all_concepts = [row[0] for row in cursor.fetchall()]

print(f'\n분석 중... (샘플 {min(10000, len(all_concepts))}개)')

# 개념 간 연결 패턴 분석
concept_patterns = defaultdict(list)
connection_count = Counter()

for i, concept_id in enumerate(all_concepts[:10000]):  # 샘플링
    # 개념 ID 패턴 분석
    parts = concept_id.split()
    
    # 연결 단어 확인 (becomes, with, beyond, in, is, transcends 등)
    connectors = ['becomes', 'with', 'beyond', 'in', 'is', 'transcends', 
                  'without', 'dream', 'atom', 'nature:', 'desire:', 'creator:']
    
    has_connection = False
    for connector in connectors:
        if connector in concept_id:
            has_connection = True
            concept_patterns[connector].append(concept_id)
            break
    
    if has_connection:
        connection_count['connected'] += 1
    else:
        connection_count['isolated'] += 1
    
    if i % 2000 == 0 and i > 0:
        print(f'  진행: {i:,} / 10,000')

print('\n' + '=' * 70)
print('📊 연결 패턴 분석')
print('=' * 70)

print(f'\n연결된 개념: {connection_count["connected"]:,} ({connection_count["connected"]/10000*100:.1f}%)')
print(f'고립된 개념: {connection_count["isolated"]:,} ({connection_count["isolated"]/10000*100:.1f}%)')

print('\n연결 패턴 분포:')
for connector, concepts in sorted(concept_patterns.items(), key=lambda x: len(x[1]), reverse=True)[:15]:
    print(f'  "{connector}": {len(concepts):,}개')
    # 샘플 출력
    print(f'    예: {", ".join(concepts[:3])}')

# 고립된 개념 샘플
print('\n' + '=' * 70)
print('🏝️ 고립된 개념 샘플 (연결 단어 없음)')
print('=' * 70)

isolated_samples = []
for concept_id in all_concepts[:10000]:
    has_connector = any(conn in concept_id for conn in ['becomes', 'with', 'beyond', 'in', 'is', 
                                                          'transcends', 'without', 'dream', 'atom',
                                                          'nature:', 'desire:', 'creator:', 'purpose:'])
    if not has_connector:
        isolated_samples.append(concept_id)
    
    if len(isolated_samples) >= 50:
        break

for i, concept in enumerate(isolated_samples[:30], 1):
    print(f'  {i:2d}. {concept}')

# 개념 구조 분석
print('\n' + '=' * 70)
print('🔗 개념 구조 타입 분석')
print('=' * 70)

structure_types = {
    'composite': 0,      # "dream with truth"
    'transformation': 0, # "atom becomes love"
    'relation': 0,       # "nature:consciousness"
    'simple': 0,         # "Love"
    'multi_word': 0      # "Love and Truth"
}

for concept_id in all_concepts[:10000]:
    if 'becomes' in concept_id or 'transcends' in concept_id:
        structure_types['transformation'] += 1
    elif ':' in concept_id:
        structure_types['relation'] += 1
    elif any(w in concept_id for w in ['with', 'beyond', 'in', 'without', 'of']):
        structure_types['composite'] += 1
    elif ' ' in concept_id and len(concept_id.split()) > 2:
        structure_types['multi_word'] += 1
    else:
        structure_types['simple'] += 1

print('\n개념 구조 분포:')
for struct_type, count in sorted(structure_types.items(), key=lambda x: x[1], reverse=True):
    percentage = count / 10000 * 100
    print(f'  {struct_type:15s}: {count:5,}개 ({percentage:5.1f}%)')

# 가장 많이 등장하는 핵심 단어
print('\n' + '=' * 70)
print('🌟 가장 빈번한 핵심 단어 TOP 20')
print('=' * 70)

word_freq = Counter()
for concept_id in all_concepts[:10000]:
    # 단어 분리 (연결사 제외)
    words = re.findall(r'\w+', concept_id.lower())
    for word in words:
        if len(word) > 2 and word not in ['the', 'and', 'with', 'from', 'that', 'this']:
            word_freq[word] += 1

print()
for i, (word, count) in enumerate(word_freq.most_common(20), 1):
    print(f'  {i:2d}. "{word}": {count:,}회')

conn.close()

print('\n' + '=' * 70)
print('✅ 분석 완료')
print('=' * 70)
