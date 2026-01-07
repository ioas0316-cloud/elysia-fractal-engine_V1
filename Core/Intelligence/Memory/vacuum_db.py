
import sqlite3
import os

db_path = "data/Memory/memory.db"
if os.path.exists(db_path):
    print(f"Original size: {os.path.getsize(db_path)} bytes")
    conn = sqlite3.connect(db_path)
    conn.execute("VACUUM")
    conn.close()
    print(f"Vacuumed size: {os.path.getsize(db_path)} bytes")
else:
    print("memory.db not found.")
