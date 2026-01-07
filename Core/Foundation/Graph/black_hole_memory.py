"""
Black Hole Memory (The Event Horizon)
=====================================
Manages the tiered storage of knowledge.
High-Energy Nodes (Stars) stay in TorchGraph (GPU).
Low-Energy Nodes (Dust) are compressed into SQLite (Disk).

Philosophy:
Gravity compresses matter. When density is too high, matter collapses into a singularity.
This module handles that collapse (Offloading) and Hawking Radiation (Reloading).
"""

import sqlite3
import json
import logging
import os
from threading import Lock

logger = logging.getLogger("BlackHole")

class BlackHoleMemory:
    def __init__(self, db_path="c:\\Elysia\\data\\Memory\\memory.db"):
        self.db_path = db_path
        self.lock = Lock()
        self._init_db()
        
    def _init_db(self):
        """Creates the singularity structure if not exists."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # The Singularity Table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS singularity (
                    id TEXT PRIMARY KEY,
                    vector BLOB,
                    metadata TEXT,
                    mass REAL DEFAULT 1.0,
                    last_accessed REAL
                )
            ''')
            conn.commit()
            conn.close()
            logger.info(f"⚫ Black Hole Stabilized at {self.db_path}")
        except Exception as e:
            logger.error(f"❌ Failed to stabilize Black Hole: {e}")

    def absorb(self, nodes_data: list):
        """
        Compresses nodes into the singularity (Disk).
        
        Args:
            nodes_data: List of dicts {'id', 'vector', 'metadata', 'mass'}
        """
        if not nodes_data: return
        
        with self.lock:
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                rows = []
                for node in nodes_data:
                    # Serialize vector to bytes
                    vec_bytes = json.dumps(node['vector']).encode('utf-8')
                    meta_json = json.dumps(node.get('metadata', {}))
                    rows.append((
                        node['id'], 
                        vec_bytes, 
                        meta_json, 
                        node.get('mass', 1.0),
                        0.0 # timestamp needed?
                    ))
                
                cursor.executemany('''
                    INSERT OR REPLACE INTO singularity (id, vector, metadata, mass, last_accessed)
                    VALUES (?, ?, ?, ?, ?)
                ''', rows)
                
                conn.commit()
                conn.close()
                logger.info(f"⚫ Black Hole Absorbed {len(rows)} nodes.")
            except Exception as e:
                logger.error(f"❌ Accretion Disk Failure: {e}")

    def radiate(self, node_ids: list):
        """
        Retrieves nodes from the singularity (Hawking Radiation).
        """
        if not node_ids: return []
        
        with self.lock:
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                placeholders = ','.join('?' * len(node_ids))
                query = f"SELECT id, vector, metadata, mass FROM singularity WHERE id IN ({placeholders})"
                
                cursor.execute(query, node_ids)
                rows = cursor.fetchall()
                conn.close()
                
                result = []
                for r in rows:
                    result.append({
                        'id': r[0],
                        'vector': json.loads(r[1].decode('utf-8')),
                        'metadata': json.loads(r[2]),
                        'mass': r[3]
                    })
                return result
            except Exception as e:
                logger.error(f"❌ Hawking Radiation Failure: {e}")
                return []

# Singleton
_black_hole = None
def get_black_hole():
    global _black_hole
    if _black_hole is None:
        _black_hole = BlackHoleMemory()
    return _black_hole
