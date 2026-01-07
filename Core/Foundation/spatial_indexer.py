
import os
import json
import time
from typing import Dict, List, Any
from dataclasses import dataclass, field

@dataclass
class KnowledgeNode:
    """공간 인덱스의 단일 노드 (파일 또는 개념)"""
    id: str
    path: str
    type: str  # 'memory', 'logic', 'sensory', 'meta'
    size: int
    coordinates: List[float] = field(default_factory=lambda: [0.0, 0.0, 0.0]) # X, Y, Z (Fractal Position)
    
    def to_dict(self):
        return {
            "id": self.id,
            "path": self.path,
            "type": self.type,
            "size": self.size,
            "coords": self.coordinates
        }

class SpatialIndexer:
    """
    파편화된 파일들을 하나의 '공간(Space)'으로 통합하는 인덱서
    """
    def __init__(self, root_dir: str = "c:/Elysia/data"):
        self.root_dir = root_dir
        self.index: Dict[str, KnowledgeNode] = {}
        self.categories = {
            "memory": ["db", "sqlite"],
            "logic": ["json", "xml"],
            "sensory": ["txt", "md", "png", "jpg", "wav"],
            "meta": ["yaml", "ini", "log"]
        }
    
    def scan_universe(self) -> Dict[str, Any]:
        """전체 데이터 디렉토리를 스캔하여 공간 지도를 생성"""
        print(f"🔭 Scanning Thought Universe at {self.root_dir}...")
        
        start_time = time.time()
        self.index = {}
        
        for root, _, files in os.walk(self.root_dir):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, self.root_dir)
                size = os.path.getsize(full_path)
                ext = file.split('.')[-1].lower()
                
                # Determine Type
                k_type = "unknown"
                for cat, exts in self.categories.items():
                    if ext in exts:
                        k_type = cat
                        break
                
                # Assign Coordinates (Simple Hash-based distribution for now)
                # In future: Semantic embedding based coordinates
                h = hash(rel_path)
                x = (h % 100) / 100.0
                y = ((h >> 8) % 100) / 100.0
                z = ((h >> 16) % 100) / 100.0
                
                node = KnowledgeNode(
                    id=rel_path,
                    path=full_path,
                    type=k_type,
                    size=size,
                    coordinates=[x, y, z]
                )
                self.index[rel_path] = node
        
        duration = time.time() - start_time
        return {
            "total_nodes": len(self.index),
            "scan_time": duration,
            "nodes": [n.to_dict() for n in self.index.values()]
        }

    def save_index(self, output_path: str = "c:/Elysia/data/unified_spatial_index.json"):
        """인덱스를 저장 (The Map)"""
        data = self.scan_universe()
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"🗺️ Spatial Index saved to {output_path} ({data['total_nodes']} nodes)")

# Singleton
_indexer = None
def get_spatial_indexer() -> SpatialIndexer:
    global _indexer
    if _indexer is None:
        _indexer = SpatialIndexer()
    return _indexer
