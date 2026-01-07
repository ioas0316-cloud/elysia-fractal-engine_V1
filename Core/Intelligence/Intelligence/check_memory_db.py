"""메모리 DB 한국어/영어 개념 분포 확인"""
import sqlite3

conn = sqlite3.connect('data/Memory/memory.db')
cursor = conn.cursor()

print('=' * 60)
print('🔍 Memory Database 분석')
print('=' * 60)

# 테이블 구조 확인
print('\n📊 테이블 구조:')
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print(f'테이블 목록: {[t[0] for t in tables]}')

for table_name in [t[0] for t in tables]:
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()
    print(f'\n{table_name} 컬럼:')
    for col in columns:
        print(f'  - {col[1]} ({col[2]})')

# 전체 개념 수
cursor.execute('SELECT COUNT(*) FROM concepts')
total = cursor.fetchone()[0]
print(f'\n총 개념 수: {total:,}')

# 한국어 개념 검색
print('\n📋 한국어 개념 샘플:')
korean_words = ['사랑', '정체성', '의식', '꿈', '진실', '아버지']
for word in korean_words:
    cursor.execute(f"SELECT COUNT(*) FROM concepts WHERE id LIKE '%{word}%'")
    count = cursor.fetchone()[0]
    print(f'  "{word}": {count}개')
    
    if count > 0:
        cursor.execute(f"SELECT id FROM concepts WHERE id LIKE '%{word}%' LIMIT 3")
        samples = cursor.fetchall()
        for (concept_id,) in samples:
            print(f'    → {concept_id}')

# 영어 개념 검색
print('\n📋 영어 개념 샘플:')
english_words = ['love', 'identity', 'consciousness', 'dream', 'truth', 'father']
for word in english_words:
    cursor.execute(f"SELECT COUNT(*) FROM concepts WHERE id LIKE '%{word}%'")
    count = cursor.fetchone()[0]
    print(f'  "{word}": {count}개')
    
    if count > 0:
        cursor.execute(f"SELECT id FROM concepts WHERE id LIKE '%{word}%' LIMIT 3")
        samples = cursor.fetchall()
        for (concept_id,) in samples:
            print(f'    → {concept_id}')

# 상위 빈도 개념 - 최근 액세스 기준
print('\n🔥 최근 액세스 개념 TOP 20:')
cursor.execute('SELECT id, last_accessed FROM concepts ORDER BY last_accessed DESC LIMIT 20')
top_concepts = cursor.fetchall()
for i, (concept_id, last_access) in enumerate(top_concepts, 1):
    print(f'  {i:2d}. {concept_id}')

conn.close()
