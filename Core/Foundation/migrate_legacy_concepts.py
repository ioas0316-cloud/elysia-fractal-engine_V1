import sqlite3
import zlib
import json
import time
import sys
import os
import logging
from typing import List, Dict, Any

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Core.Foundation.hyper_quaternion import Quaternion

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("migration.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("Migration")

DB_PATH = "data/Memory/memory.db"
BATCH_SIZE = 10000

def get_legacy_count(cursor):
    cursor.execute("SELECT count(*) FROM concepts")
    return cursor.fetchone()[0]

def create_pattern_dna_table(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pattern_dna (
            name TEXT PRIMARY KEY,
            pattern_type TEXT,
            data TEXT,
            compression_ratio REAL,
            created_at REAL
        )
    """)

def map_legacy_to_dna(legacy_id: str, legacy_data: Any) -> Dict[str, Any]:
    """
    Map legacy format to PatternDNA dict format.
    Handles both List (oldest) and Dict (newer) formats.
    """
    try:
        name = legacy_id # ALWAYS use legacy_id as the unique name
        internal_name = legacy_id
        color = [127, 127, 127]
        base_freq = 432.0
        quat_dict = {"w": 1, "x": 0, "y": 0, "z": 0}
        
        if isinstance(legacy_data, list):
            # Format: [name, color, ..., quaternion]
            if len(legacy_data) > 0:
                internal_name = legacy_data[0] # Store internal name in metadata
            if len(legacy_data) > 1:
                color = legacy_data[1]
            if len(legacy_data) > 11 and isinstance(legacy_data[11], dict):
                quat_dict = legacy_data[11]
            
            # Map Color to Frequency
            avg_color = sum(color) / 3.0 if color else 127
            base_freq = 200 + (avg_color * 2)
            
        elif isinstance(legacy_data, dict):
            # Format: {"category": ..., "frequency": ...}
            base_freq = legacy_data.get("frequency", 432.0)
            if base_freq < 20.0:
                base_freq = base_freq * 1000.0
            
        # Construct PatternDNA dict
        dna_dict = {
            "name": name, # Unique ID
            "seed_formula": {
                "formula": "Z = Z^2 + C_legacy",
                "constants": {"color": color}
            },
            "frequency_signature": [base_freq, base_freq * 1.5, base_freq * 2.0],
            "phase_pattern": [0.0, 1.57, 3.14],
            "amplitude_envelope": [1.0, 0.8, 0.6, 0.4, 0.2],
            "resonance_fingerprint": [
                quat_dict.get("w", 1),
                quat_dict.get("x", 0),
                quat_dict.get("y", 0),
                quat_dict.get("z", 0)
            ],
            "metadata": {
                "source": "legacy_migration",
                "original_id": legacy_id,
                "internal_name": internal_name,
                "legacy_data_type": type(legacy_data).__name__
            },
            "compression_ratio": 10.0
        }
        return dna_dict
        
    except Exception as e:
        return None

def migrate():
    if not os.path.exists(DB_PATH):
        logger.error(f"Database not found: {DB_PATH}")
        return

    logger.info(f"🚀 Starting Massive Migration from {DB_PATH}")
    
    try:
        # Connection 1: Reader (Read-only)
        conn_read = sqlite3.connect(DB_PATH)
        cursor_read = conn_read.cursor()
        
        # Connection 2: Writer
        conn_write = sqlite3.connect(DB_PATH)
        conn_write.execute("PRAGMA journal_mode=WAL;") # Enable WAL mode for better I/O
        cursor_write = conn_write.cursor()
        
        # 1. Setup
        create_pattern_dna_table(cursor_write)
        total_count = get_legacy_count(cursor_read)
        logger.info(f"📦 Total Legacy Concepts to Migrate: {total_count:,}")
        
        # 2. Check existing
        cursor_read.execute("SELECT count(*) FROM pattern_dna WHERE data LIKE '%legacy_migration%'")
        already_migrated = cursor_read.fetchone()[0]
        logger.info(f"⏭️  Already Migrated: {already_migrated:,}")
        
        if already_migrated >= total_count:
            logger.info("✅ Migration already complete!")
            conn_read.close()
            conn_write.close()
            return

        # 3. Batch Process
        logger.info("Processing in batches...")
        start_time = time.time()
        processed = 0
        
        # Optimization: Use LIMIT/OFFSET to skip already processed rows
        # This is much faster than iterating and ignoring
        offset = already_migrated
        logger.info(f"Resuming from offset: {offset:,}")
        
        while True:
            # Fetch batch with offset
            cursor_read.execute(f"SELECT id, data FROM concepts LIMIT {BATCH_SIZE} OFFSET {offset}")
            rows = cursor_read.fetchall()
            
            if not rows:
                break
                
            batch_data = []
            for row in rows:
                legacy_id = row[0]
                blob = row[1]
                
                try:
                    # Decompress & Parse
                    json_str = zlib.decompress(blob).decode('utf-8')
                    legacy_list = json.loads(json_str)
                    
                    # Map
                    dna_dict = map_legacy_to_dna(legacy_id, legacy_list)
                    
                    if dna_dict:
                        batch_data.append((
                            dna_dict["name"],
                            "legacy_concept",
                            json.dumps(dna_dict),
                            dna_dict["compression_ratio"],
                            time.time()
                        ))
                        
                except Exception as e:
                    continue
            
            # Bulk Insert using writer
            if batch_data:
                cursor_write.executemany("""
                    INSERT OR IGNORE INTO pattern_dna (name, pattern_type, data, compression_ratio, created_at)
                    VALUES (?, ?, ?, ?, ?)
                """, batch_data)
                conn_write.commit()
                
                processed += len(batch_data)
                offset += len(rows) # Increment offset
                
                # Progress Log
                elapsed = time.time() - start_time
                rate = processed / elapsed if elapsed > 0 else 0
                percent = (offset) / total_count * 100
                logger.info(f"   Progress: {offset:,}/{total_count:,} ({percent:.2f}%) - {rate:.0f} items/sec")
            else:
                offset += len(rows) # Skip if no valid data in batch

        logger.info("Migration Complete!")
        conn_read.close()
        conn_write.close()

    except Exception as e:
        logger.error(f"Fatal Error: {e}")

if __name__ == "__main__":
    migrate()
