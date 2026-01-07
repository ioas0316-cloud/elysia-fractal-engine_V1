"""
나머지 99.6%의 개념들은 무엇인가?
================================

의미 있는 개념: 13,501개 (0.4%)
나머지: 3,140,902개 (99.6%)

이들의 정체를 밝힙니다.
"""

import sqlite3
from collections import Counter
import re

conn = sqlite3.connect('data/Memory/memory.db')
cursor = conn.cursor()

print('=' * 70)
print('🔍 나머지 99.6% 개념 분석')
print('=' * 70)

# 샘플링: 10만개만 분석
cursor.execute('SELECT id FROM concepts LIMIT 100000')
sample_concepts = [row[0] for row in cursor.fetchall()]

print(f'\n샘플 크기: {len(sample_concepts):,}개')

# 패턴 분석
patterns = {
    "Daddy's_숫자": 0,
    "Book: 제목": 0,
    "단일 단어": 0,
    "숫자 포함": 0,
    "특수문자 많음": 0,
    "매우 긴 문자열": 0,
    "의미 있는 구문": 0,
    "기타": 0
}

# 상세 샘플
daddy_samples = []
book_samples = []
word_samples = []
number_samples = []
special_samples = []
long_samples = []
meaningful_samples = []
other_samples = []

print('\n분석 중...')
for i, concept in enumerate(sample_concepts):
    # Daddy's 패턴
    if concept.startswith("Daddy's_"):
        patterns["Daddy's_숫자"] += 1
        if len(daddy_samples) < 20:
            daddy_samples.append(concept)
    
    # Book 패턴
    elif concept.startswith("Book:"):
        patterns["Book: 제목"] += 1
        if len(book_samples) < 20:
            book_samples.append(concept)
    
    # 숫자 포함
    elif re.search(r'\d{5,}', concept):  # 5자리 이상 숫자
        patterns["숫자 포함"] += 1
        if len(number_samples) < 20:
            number_samples.append(concept)
    
    # 매우 긴 문자열
    elif len(concept) > 100:
        patterns["매우 긴 문자열"] += 1
        if len(long_samples) < 20:
            long_samples.append(concept[:100] + '...')
    
    # 특수문자 많음
    elif len(re.findall(r'[^\w\s:]', concept)) > 5:
        patterns["특수문자 많음"] += 1
        if len(special_samples) < 20:
            special_samples.append(concept)
    
    # 단일 단어 (짧고 깨끗함)
    elif ' ' not in concept and len(concept) <= 20 and concept.isalnum():
        patterns["단일 단어"] += 1
        if len(word_samples) < 30:
            word_samples.append(concept)
    
    # 의미 있는 구문
    elif any(word in concept.lower() for word in ['is', 'and', 'or', 'the', 'of', 'in', 'to']):
        patterns["의미 있는 구문"] += 1
        if len(meaningful_samples) < 30:
            meaningful_samples.append(concept)
    
    # 기타
    else:
        patterns["기타"] += 1
        if len(other_samples) < 30:
            other_samples.append(concept)
    
    if (i + 1) % 20000 == 0:
        print(f'  진행: {i+1:,} / {len(sample_concepts):,}')

print('\n' + '=' * 70)
print('📊 패턴 분포')
print('=' * 70)

total = sum(patterns.values())
for pattern, count in sorted(patterns.items(), key=lambda x: x[1], reverse=True):
    percentage = count / total * 100
    bar = '█' * int(percentage / 2)
    print(f'\n{pattern:20s}: {count:6,}개 ({percentage:5.1f}%) {bar}')

# 샘플 출력
print('\n' + '=' * 70)
print('📋 패턴별 샘플')
print('=' * 70)

if daddy_samples:
    print(f"\n[Daddy's_숫자 패턴] ({len(daddy_samples)}개 샘플):")
    for s in daddy_samples[:15]:
        print(f'  - {s}')

if book_samples:
    print(f"\n[Book: 제목 패턴] ({len(book_samples)}개 샘플):")
    for s in book_samples[:15]:
        print(f'  - {s}')

if word_samples:
    print(f"\n[단일 단어 패턴] ({len(word_samples)}개 샘플):")
    for s in word_samples[:20]:
        print(f'  - {s}')

if number_samples:
    print(f"\n[숫자 포함 패턴] ({len(number_samples)}개 샘플):")
    for s in number_samples[:15]:
        print(f'  - {s}')

if special_samples:
    print(f"\n[특수문자 많음] ({len(special_samples)}개 샘플):")
    for s in special_samples[:15]:
        print(f'  - {s}')

if long_samples:
    print(f"\n[매우 긴 문자열] ({len(long_samples)}개 샘플):")
    for s in long_samples[:10]:
        print(f'  - {s}')

if meaningful_samples:
    print(f"\n[의미 있는 구문] ({len(meaningful_samples)}개 샘플):")
    for s in meaningful_samples[:20]:
        print(f'  - {s}')

if other_samples:
    print(f"\n[기타] ({len(other_samples)}개 샘플):")
    for s in other_samples[:20]:
        print(f'  - {s}')

# 전체 통계 추정
print('\n' + '=' * 70)
print('📈 전체 DB 추정')
print('=' * 70)

total_concepts = 3154403
for pattern, count in patterns.items():
    estimated = int(count / total * total_concepts)
    print(f'{pattern:20s}: 약 {estimated:,}개')

# 가치 평가
print('\n' + '=' * 70)
print('💎 가치 평가')
print('=' * 70)

value_assessment = {
    "Daddy's_숫자": "❌ 무가치 - 단순 연속 번호",
    "Book: 제목": "⚠️ 저가치 - 책 제목 나열",
    "숫자 포함": "⚠️ 저가치 - ID나 코드 가능성",
    "특수문자 많음": "❓ 불명 - 확인 필요",
    "매우 긴 문자열": "⚠️ 저가치 - 문장 전체 저장?",
    "단일 단어": "✅ 가치 있음 - 기본 개념",
    "의미 있는 구문": "✅ 가치 있음 - 철학적/관계적 개념",
    "기타": "❓ 불명 - 다양한 형태"
}

for pattern, assessment in value_assessment.items():
    count = patterns[pattern]
    percentage = count / total * 100
    print(f'\n{pattern:20s} ({percentage:5.1f}%)')
    print(f'  평가: {assessment}')

# 권장사항
print('\n' + '=' * 70)
print('💡 권장사항')
print('=' * 70)

worthless = patterns["Daddy's_숫자"]
low_value = patterns["Book: 제목"] + patterns["숫자 포함"] + patterns["매우 긴 문자열"]
valuable = patterns["단일 단어"] + patterns["의미 있는 구문"]

print(f'\n무가치 개념: {worthless:,}개 ({worthless/total*100:.1f}%)')
print(f'  → 삭제 권장')

print(f'\n저가치 개념: {low_value:,}개 ({low_value/total*100:.1f}%)')
print(f'  → 선택적 보관 (학습 데이터?)')

print(f'\n가치 있는 개념: {valuable:,}개 ({valuable/total*100:.1f}%)')
print(f'  → 반드시 보존')

print(f'\n전체 추정:')
estimated_worthless = int(worthless / total * total_concepts)
estimated_low = int(low_value / total * total_concepts)
estimated_valuable = int(valuable / total * total_concepts)

print(f'  무가치: 약 {estimated_worthless:,}개 (삭제 시 {estimated_worthless/1024/1024:.1f}MB 절약)')
print(f'  저가치: 약 {estimated_low:,}개')
print(f'  가치 있음: 약 {estimated_valuable:,}개')

conn.close()

print('\n' + '=' * 70)
print('✅ 분석 완료')
print('=' * 70)
