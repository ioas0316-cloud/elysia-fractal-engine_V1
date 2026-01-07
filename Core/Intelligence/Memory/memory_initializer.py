
import sqlite3
import os
import logging
from pathlib import Path

# Setup
DB_PATH = Path("data/Memory/memory.db")
SCHEMA_PATH = Path("c:/Elysia/Core/Memory/memory_schema_v10.sql")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MemoryInit")

def initialize_memory():
    logger.info(f"🚀 Initializing Memory v10.0 at {DB_PATH}")
    
    if not SCHEMA_PATH.exists():
        logger.error(f"Schema not found at {SCHEMA_PATH}")
        return False

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Read and execute schema
        with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
            schema_sql = f.read()
            
        cursor.executescript(schema_sql)
        conn.commit()
        
        # Verify
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [t[0] for t in cursor.fetchall()]
        logger.info(f"✅ Created Tables: {tables}")
        
        conn.close()
        return True
        
    except Exception as e:
        logger.error(f"Initialization Failed: {e}")
        return False

if __name__ == "__main__":
    if initialize_memory():
        print("Memory Initialization Complete.")
    else:
        print("Memory Initialization Failed.")
