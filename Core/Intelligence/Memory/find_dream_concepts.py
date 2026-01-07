"""dream 개념 찾기"""
import sqlite3

conn = sqlite3.connect('data/Memory/memory.db')
cursor = conn.cursor()

print('dream 관련 개념 검색:')
cursor.execute("SELECT id FROM concepts WHERE id LIKE '%dream%' LIMIT 30")
results = cursor.fetchall()

print(f'\n총 {len(results)}개 발견:\n')
for r in results:
    print(f'  - {r[0]}')

print('\n\nlove 관련 개념 검색:')
cursor.execute("SELECT id FROM concepts WHERE id LIKE '%love%' LIMIT 30")
results = cursor.fetchall()

print(f'\n총 {len(results)}개 발견:\n')
for r in results:
    print(f'  - {r[0]}')

conn.close()
