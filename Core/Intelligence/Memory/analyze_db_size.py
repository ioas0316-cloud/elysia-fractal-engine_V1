
import sys
import os
import sqlite3
import json

sys.path.append(os.getcwd())

conn = sqlite3.connect("data/Memory/memory.db")
cursor = conn.cursor()

cursor.execute("SELECT id, length(data) as size, data FROM concepts LIMIT 5")
rows = cursor.fetchall()

print("--- Sample Data Sizes ---")
total_size = 0
for row in rows:
    print(f"ID: {row[0]}, Size: {row[1]} bytes")
    total_size += row[1]
    # print(f"Content: {row[2][:100]}...")

cursor.execute("SELECT avg(length(data)) FROM concepts")
avg_size = cursor.fetchone()[0]
print(f"\nAverage JSON Data Size: {avg_size:.2f} bytes")

conn.close()
