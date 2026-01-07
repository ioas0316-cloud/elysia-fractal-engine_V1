-- Elysia v10.0 Memory Schema
-- Logic: Wave-based storage + P4 Sensory Cache

-- 1. EXPERIENCES: The stream of consciousness
CREATE TABLE IF NOT EXISTS experiences (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    type TEXT NOT NULL, -- 'chat', 'thought', 'sensory_input'
    content TEXT,
    emotion_vector TEXT, -- JSON serialization of emotional state
    source TEXT, -- 'user', 'p4_system', 'internal'
    embedding BLOB -- For future vector search
);

-- 2. KNOWLEDGE GRAPH: The "Spiderweb" concept map
CREATE TABLE IF NOT EXISTS knowledge_graph (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    concept_a TEXT NOT NULL,
    relation TEXT NOT NULL,
    concept_b TEXT NOT NULL,
    weight REAL DEFAULT 1.0,
    last_accessed DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(concept_a, relation, concept_b)
);

-- 3. SENSORY CACHE (P4): Caching expensive web fetches
CREATE TABLE IF NOT EXISTS sensory_cache (
    url_hash TEXT PRIMARY KEY,
    url TEXT NOT NULL,
    content TEXT,
    fetched_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_accessed DATETIME DEFAULT CURRENT_TIMESTAMP,
    access_count INTEGER DEFAULT 1
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_exp_timestamp ON experiences(timestamp);
CREATE INDEX IF NOT EXISTS idx_kg_concept_a ON knowledge_graph(concept_a);
CREATE INDEX IF NOT EXISTS idx_sensory_url ON sensory_cache(url);
