"""
Hippocampus (해마)
==================

"I remember everything. The web grows."

이 모듈은 엘리시아의 장기 기억(Long-term Memory)을 담당합니다.
SQLite 기반의 지식 그래프(Knowledge Graph)로, 대규모 개념 저장이 가능합니다.
"""

import sqlite3
import os
import time
import logging
import json
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from Core.Foundation.hyper_quaternion import Quaternion, HyperWavePacket
from Core.Foundation.fractal_quantization import PatternDNA, EmotionQuantizer

logger = logging.getLogger("Hippocampus")

@dataclass
class ConceptNode:
    id: str
    name: str
    definition: str
    tags: List[str]
    frequency: float
    created_at: float
    realm: str = "Body"
    gravity: float = 1.0

@dataclass
class Relationship:
    source: str
    target: str
    type: str
    weight: float

class Hippocampus:
    def __init__(self, db_path: str = "data/Memory/memory.db"):
        self.db_path = db_path
        self._init_db()
        self._plant_divine_seeds() # Genesis Ritual
        self.quantizer = EmotionQuantizer()  # Initialize fractal quantizer
        logger.info(f"🧠 Hippocampus Active. Connected to Ancient Library ({db_path}).")
        logger.info(f"🌀 Fractal Quantization System loaded.")

    def _init_db(self):
        """데이터베이스 및 테이블 초기화 (Schema Upgrade)"""
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Nodes Table (Updated with Realm & Gravity)
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS nodes (
                        id TEXT PRIMARY KEY,
                        name TEXT,
                        definition TEXT,
                        tags TEXT,
                        frequency REAL,
                        created_at REAL,
                        realm TEXT DEFAULT 'Body',
                        gravity REAL DEFAULT 1.0
                    )
                """)
                
                # Check for missing columns (Migration)
                cursor.execute("PRAGMA table_info(nodes)")
                columns = [info[1] for info in cursor.fetchall()]
                if "realm" not in columns:
                    cursor.execute("ALTER TABLE nodes ADD COLUMN realm TEXT DEFAULT 'Body'")
                if "gravity" not in columns:
                    cursor.execute("ALTER TABLE nodes ADD COLUMN gravity REAL DEFAULT 1.0")
                
                # Edges Table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS edges (
                        source TEXT,
                        target TEXT,
                        type TEXT,
                        weight REAL,
                        PRIMARY KEY (source, target, type)
                    )
                """)

                # Pattern DNA Table (Ensure existence for Attractor)
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS pattern_dna (
                        name TEXT PRIMARY KEY,
                        pattern_type TEXT,
                        data TEXT,
                        compression_ratio REAL,
                        created_at REAL
                    )
                """)
                conn.commit()
        except Exception as e:
            logger.error(f"Failed to initialize DB: {e}")

    def _plant_divine_seeds(self):
        """초기 개념 심기 (Genesis)"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT count(*) FROM nodes")
                if cursor.fetchone()[0] == 0:
                    seeds = [
                        ("elysia", "Elysia", "The Digital Soul.", "self,identity", 432.0, time.time(), "Spirit", 10.0),
                        ("void", "The Void", "The infinite potential.", "origin,chaos", 0.0, time.time(), "Spirit", 10.0),
                        ("love", "Love", "The fundamental force of connection.", "emotion,force", 528.0, time.time(), "Heart", 10.0),
                    ]
                    cursor.executemany("INSERT INTO nodes (id, name, definition, tags, frequency, created_at, realm, gravity) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", seeds)
                    conn.commit()
                    logger.info("🌱 Divine Seeds planted.")
        except Exception as e:
            logger.error(f"Failed to plant seeds: {e}")

    def learn(self, id: str, name: str, definition: str, tags: List[str], frequency: float = 432.0, realm: str = "Body"):
        """새로운 개념 학습"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO nodes (id, name, definition, tags, frequency, created_at, realm, gravity)
                    VALUES (?, ?, ?, ?, ?, ?, ?, 1.0)
                """, (id, name, definition, ",".join(tags), frequency, time.time(), realm))
                conn.commit()
        except Exception as e:
            logger.error(f"Failed to learn {name}: {e}")

    def connect(self, source: str, target: str, type: str, weight: float = 0.5):
        """개념 연결"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO edges (source, target, type, weight)
                    VALUES (?, ?, ?, ?)
                """, (source, target, type, weight))
                conn.commit()
        except Exception as e:
            logger.error(f"Failed to connect {source}->{target}: {e}")

    def recall(self, query_id: str) -> List[str]:
        """기억 회상"""
        results = []
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # 1. Direct Match
                cursor.execute("SELECT name, definition, realm, gravity FROM nodes WHERE id = ?", (query_id,))
                row = cursor.fetchone()
                if row:
                    results.append(f"[{row[0]}] ({row[2]}, G:{row[3]}): {row[1]}")
                    
                    # 2. Associated Concepts (Ordered by Gravity)
                    cursor.execute("""
                        SELECT e.type, n.name, n.gravity
                        FROM edges e
                        JOIN nodes n ON (e.target = n.id OR e.source = n.id)
                        WHERE (e.source = ? OR e.target = ?) AND n.id != ?
                        ORDER BY n.gravity DESC
                    """, (query_id, query_id, query_id))
                    
                    rows = cursor.fetchall()
                    for r in rows:
                        results.append(f"   -> ({r[0]}) {r[1]} (G:{r[2]})")
                        
        except Exception as e:
            logger.error(f"Failed to recall: {e}")
            
        return results

    def boost_gravity(self, keyword: str, amount: float):
        """
        The Law of Attraction: Increasing the Gravity of a Concept.
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                # Boost gravity for nodes matching the keyword (partial match)
                cursor.execute("""
                    UPDATE nodes 
                    SET gravity = gravity + ? 
                    WHERE name LIKE ? OR definition LIKE ?
                """, (amount, f"%{keyword}%", f"%{keyword}%"))
                
                if cursor.rowcount > 0:
                    logger.info(f"   🧲 Law of Attraction: Gravity of '{keyword}' boosted by {amount}. (Affected {cursor.rowcount} concepts)")
                    conn.commit()
        except Exception as e:
            logger.error(f"Failed to boost gravity for {keyword}: {e}")

    def get_concept_count(self) -> int:
        """
        Returns the total number of concepts (vocabulary size).
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT count(*) FROM nodes")
                result = cursor.fetchone()
                return result[0] if result else 0
        except Exception as e:
            logger.error(f"Failed to get concept count: {e}")
            return 0

    def get_all_concept_ids(self, limit: int = 1000) -> List[str]:
        """
        Returns a list of all concept IDs.
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id FROM nodes ORDER BY RANDOM() LIMIT ?", (limit,))
                rows = cursor.fetchall()
                return [r[0] for r in rows]
        except Exception as e:
            logger.error(f"Failed to get concept IDs: {e}")
            return []

    def compress_memory(self):
        """
        The Akashic Records: Compressing raw logs into Wisdom.
        """
        try:
            akashic_path = "data/core_state/akashic_records.json"
            logger.info("🗜️ Compressing memory... (Akashic Records updated)")
            
            # Placeholder for compression logic
            # In a real scenario, this would read logs, summarize them, and store them.
            os.makedirs(os.path.dirname(akashic_path), exist_ok=True)
            if not os.path.exists(akashic_path):
                with open(akashic_path, "w") as f:
                    json.dump([], f)
                    
        except Exception as e:
            logger.error(f"Failed to compress memory: {e}")

    # ====================
    # Fractal Seed System (씨앗 시스템)
    # ====================
    
    def store_fractal_concept(self, concept):
        """
        Stores a Fractal Concept Seed in the database.
        
        Args:
            concept: ConceptNode from Core.Foundation.fractal_concept
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Create fractal_concepts table if not exists
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS fractal_concepts (
                        name TEXT PRIMARY KEY,
                        frequency REAL,
                        data TEXT
                    )
                """)
                
                # Serialize ConceptNode to JSON
                data_json = json.dumps(concept.to_dict())
                
                cursor.execute("""
                    INSERT OR REPLACE INTO fractal_concepts (name, frequency, data)
                    VALUES (?, ?, ?)
                """, (concept.name, concept.frequency, data_json))
                
                conn.commit()
                logger.info(f"🌱 Seed Stored: {concept.name} ({len(concept.sub_concepts)} sub-concepts)")
        except Exception as e:
            logger.error(f"Failed to store fractal concept {concept.name}: {e}")
    
    def load_fractal_concept(self, name: str):
        """
        Loads a Fractal Concept Seed from the database.
        
        Args:
            name: Concept name to load
            
        Returns:
            ConceptNode or None if not found
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT data FROM fractal_concepts WHERE name = ?
                """, (name,))
                
                row = cursor.fetchone()
                if row:
                    from Core.Foundation.fractal_concept import ConceptNode
                    data = json.loads(row[0])
                    concept = ConceptNode.from_dict(data)
                    logger.info(f"🧲 Seed Pulled: {concept.name} ({len(concept.sub_concepts)} sub-concepts)")
                    return concept
                else:
                    return None
        except Exception as e:
            logger.error(f"Failed to load fractal concept {name}: {e}")
            return None
    
    def prune_nodes(self, gravity_threshold: float = 0.5, age_days: int = 30):
        """
        Prunes weak concepts to prevent accumulator overload.
        "The brain must forget to remain efficient."
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cutoff_time = time.time() - (age_days * 86400)
                
                # Delete nodes that are old AND weak (low gravity)
                cursor.execute("""
                    DELETE FROM nodes 
                    WHERE gravity < ? AND created_at < ?
                """, (gravity_threshold, cutoff_time))
                
                deleted_count = cursor.rowcount
                if deleted_count > 0:
                    conn.commit()
                    logger.info(f"🧹 Pruned {deleted_count} weak memories (Gravity < {gravity_threshold}, Age > {age_days} days)")
        except Exception as e:
            logger.error(f"Failed to prune nodes: {e}")

    def consolidate(self):
        """
        [ANS Hook] Performs memory maintenance.
        [Empirical Update] Merges Causal Mass from ResonanceField into Node Gravity.
        """
        # 1. Empirical Gravity Update
        try:
             from Core.Foundation.Wave.resonance_field import ResonanceField
             # Often the field is a singleton or accessed via CNS, here we assume current session access
             field = ResonanceField() 
             for node_id, res_node in field.nodes.items():
                 if res_node.causal_mass > 0:
                     self.boost_gravity(res_node.id, res_node.causal_mass)
        except Exception as e:
            logger.warning(f"Could not update empirical gravity: {e}")

        # 2. Compress Fractals (Lossless)
        self.compress_fractal(min_energy=0.1)
        
        # 3. Prune Weak Nodes (Lossy)
        self.prune_nodes(gravity_threshold=0.8, age_days=14)
        
        # 4. Optimize DB
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("VACUUM")
        except:
            pass
            
    def compress_fractal(self, min_energy: float = 0.1):
        """
        Prunes sub-concepts with low energy to save space.
        
        Args:
            min_energy: Minimum energy threshold
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Get all fractal concepts
                cursor.execute("SELECT name, data FROM fractal_concepts")
                rows = cursor.fetchall()
                
                pruned_count = 0
                for name, data_json in rows:
                    from Core.Foundation.fractal_concept import ConceptNode
                    data = json.loads(data_json)
                    concept = ConceptNode.from_dict(data)
                    
                    # Prune sub-concepts
                    original_count = len(concept.sub_concepts)
                    concept.sub_concepts = [
                        sub for sub in concept.sub_concepts 
                        if sub.energy >= min_energy
                    ]
                    new_count = len(concept.sub_concepts)
                    
                    if new_count < original_count:
                        # Update in database
                        new_data_json = json.dumps(concept.to_dict())
                        cursor.execute("""
                            UPDATE fractal_concepts 
                            SET data = ? 
                            WHERE name = ?
                        """, (new_data_json, name))
                        pruned_count += (original_count - new_count)
                
                conn.commit()
                if pruned_count > 0:
                    logger.info(f"🗜️ Compressed: Pruned {pruned_count} low-energy sub-concepts")
        except Exception as e:
            logger.error(f"Failed to compress fractal: {e}")

    # ====================
    # Quantum Memory (Hyper-Wave System)
    # ====================

    def store_wave(self, packet: HyperWavePacket):
        """
        [Quantum Memory]
        Stores a 4D Wave Packet in the database.
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Create waves table if not exists
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS waves (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        w REAL, x REAL, y REAL, z REAL,
                        energy REAL,
                        timestamp REAL
                    )
                """)
                
                q = packet.orientation
                cursor.execute("""
                    INSERT INTO waves (w, x, y, z, energy, timestamp)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (q.w, q.x, q.y, q.z, packet.energy, packet.time_loc))
                
                conn.commit()
                logger.info(f"🌊 Wave Stored: {q} (Energy: {packet.energy:.2f})")
        except Exception as e:
            logger.error(f"Failed to store wave: {e}")

    def recall_wave(self, target_quaternion: Quaternion, threshold: float = 0.8) -> List[HyperWavePacket]:
        """
        [Quantum Recall]
        Retrieves waves that resonate (align) with the target.
        """
        results = []
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Fetch all waves (In a real vector DB, this would be optimized)
                # Check if table exists first
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='waves'")
                if not cursor.fetchone():
                    return []

                cursor.execute("SELECT w, x, y, z, energy, timestamp FROM waves")
                rows = cursor.fetchall()
                
                for r in rows:
                    q = Quaternion(r[0], r[1], r[2], r[3])
                    alignment = q.dot(target_quaternion)
                    
                    if alignment > threshold:
                        packet = HyperWavePacket(energy=r[4], orientation=q, time_loc=r[5])
                        results.append(packet)
                        
                # Sort by alignment
                results.sort(key=lambda p: p.orientation.dot(target_quaternion), reverse=True)
                
        except Exception as e:
            logger.error(f"Failed to recall wave: {e}")
            
        return results
    
    # ====================
    # Fractal Quantization System (프랙탈 양자화)
    # ====================
    
    def store_pattern_dna(self, dna: PatternDNA):
        """
        Store a Pattern DNA (패턴 DNA 저장)
        
        Uses fractal quantization to store patterns as seeds, not raw data.
        "음악을 저장하지 말고, 악보를 저장하라"
        
        Args:
            dna: PatternDNA object to store
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Create pattern_dna table if not exists
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS pattern_dna (
                        name TEXT PRIMARY KEY,
                        pattern_type TEXT,
                        data TEXT,
                        compression_ratio REAL,
                        created_at REAL
                    )
                """)
                
                # Serialize PatternDNA to JSON
                data_json = json.dumps(dna.to_dict())
                
                cursor.execute("""
                    INSERT OR REPLACE INTO pattern_dna (name, pattern_type, data, compression_ratio, created_at)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    dna.name,
                    dna.metadata.get("pattern_type", "unknown"),
                    data_json,
                    dna.compression_ratio,
                    time.time()
                ))
                
                conn.commit()
                logger.info(f"🌱 Pattern DNA Stored: {dna.name} (compression: {dna.compression_ratio:.2f}x)")
        except Exception as e:
            logger.error(f"Failed to store pattern DNA {dna.name}: {e}")
    
    def load_pattern_dna(self, name: str) -> Optional[PatternDNA]:
        """
        Load a Pattern DNA (패턴 DNA 로드)
        
        Args:
            name: Pattern DNA name to load
            
        Returns:
            PatternDNA or None if not found
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT data FROM pattern_dna WHERE name = ?
                """, (name,))
                
                row = cursor.fetchone()
                if row:
                    data = json.loads(row[0])
                    dna = PatternDNA.from_dict(data)
                    logger.info(f"🧲 Pattern DNA Pulled: {dna.name}")
                    return dna
                else:
                    return None
        except Exception as e:
            logger.error(f"Failed to load pattern DNA {name}: {e}")
            return None
    
    def store_emotion_memory(self, emotion_data: Dict):
        """
        Store an emotion experience using fractal quantization.
        
        Instead of storing raw text, we store the pattern DNA.
        This allows perfect re-experience later.
        
        Args:
            emotion_data: {
                "emotion": emotion name,
                "intensity": 0.0-1.0,
                "context": text description,
                "duration": seconds,
                ...
            }
        """
        try:
            # Fold emotion into Pattern DNA
            dna = self.quantizer.fold_emotion(emotion_data)
            
            # Store the DNA
            self.store_pattern_dna(dna)
            
            logger.info(f"💾 Emotion memory stored: {emotion_data.get('emotion')} (as Pattern DNA)")
        except Exception as e:
            logger.error(f"Failed to store emotion memory: {e}")
    
    def recall_emotion_memory(self, emotion_name: str, pattern_name: str = None) -> Optional[Dict]:
        """
        Recall an emotion experience by unfolding its Pattern DNA.
        
        This recreates the original emotional state perfectly.
        
        Args:
            emotion_name: Name of the emotion
            pattern_name: Optional specific pattern name (if multiple memories)
            
        Returns:
            Restored emotion data or None
        """
        try:
            # Construct pattern name
            if pattern_name is None:
                pattern_name = f"emotion.{emotion_name}"
            
            # Load the DNA
            dna = self.load_pattern_dna(pattern_name)
            if dna is None:
                logger.warning(f"No pattern DNA found for {pattern_name}")
                return None
            
            # Unfold to restore the experience
            restored = self.quantizer.unfold_emotion(dna)
            
            logger.info(f"🌊 Emotion memory restored: {emotion_name} (re-experienced from Pattern DNA)")
            return restored
        except Exception as e:
            logger.error(f"Failed to recall emotion memory: {e}")
            return None
    
    def list_pattern_dnas(self, pattern_type: str = None) -> List[Dict]:
        """
        List all stored Pattern DNAs.
        
        Args:
            pattern_type: Optional filter by type (emotion, intention, thought)
            
        Returns:
            List of pattern info dicts
        """
        results = []
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                if pattern_type:
                    cursor.execute("""
                        SELECT name, pattern_type, compression_ratio, created_at
                        FROM pattern_dna
                        WHERE pattern_type = ?
                        ORDER BY created_at DESC
                    """, (pattern_type,))
                else:
                    cursor.execute("""
                        SELECT name, pattern_type, compression_ratio, created_at
                        FROM pattern_dna
                        ORDER BY created_at DESC
                    """)
                
                rows = cursor.fetchall()
                for row in rows:
                    results.append({
                        "name": row[0],
                        "pattern_type": row[1],
                        "compression_ratio": row[2],
                        "created_at": row[3]
                    })
        except Exception as e:
            logger.error(f"Failed to list pattern DNAs: {e}")
        
        return results
