"""
Attractor (The Magnet)
======================

"Like attracts like. The mind pulls what it needs."

This module implements the Attractor, a mechanism for retrieving relevant
concepts from the Hippocampus (Long-term Memory) based on resonance.
It acts as a magnetic force, pulling dormant memories into active consciousness.
"""

import logging
import sqlite3
import math
from typing import List, Dict, Any

logger = logging.getLogger("Attractor")

class Attractor:
    def __init__(self, context_seed: str, db_path: str = "data/Memory/memory.db"):
        self.context_seed = context_seed
        self.db_path = db_path
        
    def pull(self, active_memory: List[str], limit: int = 5) -> List[str]:
        """
        Pulls related concepts from the database based on the context seed
        and the current active memory field.
        """
        related_concepts = []
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # 1. Keyword Matching (Simple Resonance)
                # Find nodes where name or tags contain the context seed
                query = f"""
                    SELECT id, name, gravity FROM nodes 
                    WHERE name LIKE ? OR tags LIKE ?
                    ORDER BY gravity DESC
                    LIMIT {limit}
                """
                cursor.execute(query, (f'%{self.context_seed}%', f'%{self.context_seed}%'))
                rows = cursor.fetchall()
                
                for row in rows:
                    if row[1] not in active_memory:
                        related_concepts.append(row[1])
                        
                # 1.5. Pattern DNA Matching (The New Memory)
                # If we didn't find enough in nodes, check pattern_dna
                if len(related_concepts) < limit:
                    query = f"""
                        SELECT name FROM pattern_dna 
                        WHERE name LIKE ? 
                        ORDER BY created_at DESC
                        LIMIT {limit - len(related_concepts)}
                    """
                    cursor.execute(query, (f'%{self.context_seed}%',))
                    rows = cursor.fetchall()
                    
                    for row in rows:
                        if row[0] not in active_memory and row[0] not in related_concepts:
                            related_concepts.append(row[0])
                        
                # 2. Associative Retrieval (Graph Traversal)
                # If we found some direct matches, look for their neighbors
                if related_concepts:
                    placeholders = ','.join('?' for _ in related_concepts)
                    query = f"""
                        SELECT target, weight FROM edges 
                        WHERE source IN ({placeholders})
                        ORDER BY weight DESC
                        LIMIT {limit}
                    """
                    cursor.execute(query, related_concepts)
                    rows = cursor.fetchall()
                    
                    for row in rows:
                        if row[0] not in active_memory and row[0] not in related_concepts:
                            related_concepts.append(row[0])
                            
        except Exception as e:
            logger.error(f"Failed to pull memories: {e}")
            
        return related_concepts[:limit]

    def calculate_gravity(self, concept: str) -> float:
        """
        Calculates the gravitational pull of a specific concept.
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT gravity FROM nodes WHERE name = ?", (concept,))
                row = cursor.fetchone()
                if row:
                    return row[0]
        except:
            pass
        return 1.0
