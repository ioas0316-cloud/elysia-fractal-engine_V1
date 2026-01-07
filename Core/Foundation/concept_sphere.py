"""
Concept Sphere - Fractal Node Structure
=========================================

Based on SELF_FRACTAL_MODEL.md:
Node = Fractal Sphere with nested layers

Structure:
- Core: Will (의지)
- Inner: Emotions/Values (감정/가치)
- Middle: Concepts/Language (개념/언어)
- Outer: Mirror/Phenomena (세상의 투영)
"""

import numpy as np
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import time

from Core.Foundation.Wave.hyper_qubit import HyperQubit


@dataclass
class WillVector:
    """Core Layer: 의지의 방향"""
    x: float = 0.0  # Internal/Dream
    y: float = 0.0  # External/Action
    z: float = 0.0  # Law/Intent
    
    def magnitude(self) -> float:
        return np.sqrt(self.x**2 + self.y**2 + self.z**2)


class MirrorLayer:
    """
    Outer Layer: 외부 세계의 내부 표현
    세상의 현상을 마음으로 반영
    """
    def __init__(self):
        self.phenomena: List[Dict[str, Any]] = []
        self.intensity: float = 0.0
        self.last_reflection: float = 0.0
    
    def reflect(self, world_event: Dict[str, Any]):
        """세상의 현상을 내부로 반영"""
        self.phenomena.append({
            **world_event,
            'reflected_at': time.time()
        })
        # Keep only recent phenomena (last 100)
        if len(self.phenomena) > 100:
            self.phenomena = self.phenomena[-100:]
        self.last_reflection = time.time()
        self._calculate_intensity()
    
    def _calculate_intensity(self):
        """현상의 강도 계산"""
        if not self.phenomena:
            self.intensity = 0.0
            return
        
        # Recent phenomena have more intensity
        now = time.time()
        intensity = 0.0
        for p in self.phenomena:
            age = now - p.get('reflected_at', now)
            decay = np.exp(-age / 10.0)  # 10초 반감기
            intensity += decay
        
        self.intensity = intensity / len(self.phenomena)
    
    def project(self) -> List[Dict[str, Any]]:
        """내부 상태를 외부로 투영"""
        return self.phenomena


class ConceptSphere:
    """
    개념노드 = 프랙탈 구체
    
    Each concept is a spherical universe with:
    - Core: Will (central intention)
    - Inner: Emotions & Values
    - Middle: Sub-concepts & Language
    - Outer: Mirror (world reflections)
    """
    
    def __init__(self, concept_id: str, parent: Optional['ConceptSphere'] = None):
        self.id = concept_id
        self.parent = parent
        
        # === Core Layer (중심: 의지) ===
        self.will = WillVector()
        
        # === Inner Layer (내부: 감정/가치) ===
        self.emotions: Dict[str, float] = {}
        self.values: Dict[str, float] = {}
        
        # === Middle Layer (중간: 개념/언어) ===
        self.sub_concepts: Dict[str, 'ConceptSphere'] = {}  # Fractal recursion!
        self.language_tokens: List[str] = []
        
        # === Outer Layer (외부: Mirror) ===
        self.mirror = MirrorLayer()
        
        # === Dimensional State (HyperQubit) ===
        self.qubit = HyperQubit(concept_id)
        
        # === Synesthetic Layer (공감각) ===
        self.sensory_signature: Dict[str, Any] = {}  # {color, pitch, texture, etc.}
        
        # === Metadata ===
        self.created_at = time.time()
        self.last_activated = time.time()
        self.activation_count = 0
    
    def activate(self, intensity: float = 1.0):
        """Activate this concept sphere"""
        self.activation_count += 1
        self.last_activated = time.time()
        
        # Propagate to sub-concepts (fractal cascade)
        for sub in self.sub_concepts.values():
            sub.activate(intensity * 0.5)
    
    def add_sub_concept(self, concept_id: str) -> 'ConceptSphere':
        """
        프랙탈 재귀: Node 안에 Node
        """
        if concept_id not in self.sub_concepts:
            self.sub_concepts[concept_id] = ConceptSphere(concept_id, parent=self)
        return self.sub_concepts[concept_id]
    
    def set_emotion(self, emotion_type: str, intensity: float):
        """Set emotional state (Inner Layer)"""
        self.emotions[emotion_type] = max(0.0, min(1.0, intensity))
    
    def set_value(self, value_type: str, strength: float):
        """Set value (Inner Layer)"""
        self.values[value_type] = max(0.0, min(1.0, strength))
    
    def set_will(self, x: float, y: float, z: float):
        """Set will direction (Core Layer)"""
        self.will.x = x
        self.will.y = y
        self.will.z = z
    
    def get_slice(self) -> Dict[str, Any]:
        """
        구체의 단면 추출 (Dimensional Point)
        현재 상태 전체를 압축
        """
        return {
            'id': self.id,
            'will_magnitude': self.will.magnitude(),
            'will_vector': (self.will.x, self.will.y, self.will.z),
            'emotion_avg': np.mean(list(self.emotions.values())) if self.emotions else 0.0,
            'value_avg': np.mean(list(self.values.values())) if self.values else 0.0,
            'concept_density': len(self.sub_concepts),
            'mirror_intensity': self.mirror.intensity,
            'activation_count': self.activation_count,
            'qubit_state': self.qubit.get_observation(),
            'sensory_signature': self.sensory_signature
        }
    
    def to_compact(self) -> List[Any]:
        """
        Serialize to compact list for maximum compression.
        [id, [wx,wy,wz], emotions, values, subs, tokens, m_count, m_int, cat, lat, ac, q, sensory]
        """
        def q_int8(val):
            if isinstance(val, float):
                return int((max(-1.0, min(1.0, val)) + 1.0) * 127.5)
            if isinstance(val, dict):
                return {k: q_int8(v) for k, v in val.items()}
            if isinstance(val, list):
                return [q_int8(v) for v in val]
            return val

        return [
            self.id,
            [q_int8(self.will.x), q_int8(self.will.y), q_int8(self.will.z)],
            q_int8(self.emotions),
            q_int8(self.values),
            list(self.sub_concepts.keys()),
            self.language_tokens,
            len(self.mirror.phenomena),
            q_int8(self.mirror.intensity),
            int(self.created_at),
            int(self.last_activated),
            self.activation_count,
            q_int8(self.qubit.get_observation()) if self.qubit else None,
            self.sensory_signature
        ]

    @staticmethod
    def from_compact(data: List[Any]) -> 'ConceptSphere':
        """Deserialize from compact list."""
        def dq_int8(val):
            if isinstance(val, int) and 0 <= val <= 255:
                return (val / 127.5) - 1.0
            if isinstance(val, dict):
                return {k: dq_int8(v) for k, v in val.items()}
            if isinstance(val, list):
                return [dq_int8(v) for v in val]
            return val

        # Unpack list
        # [id, will, emo, val, subs, tok, m_cnt, m_int, cat, lat, ac, q, sensory]
        sphere = ConceptSphere(data[0])
        
        # Will
        w = data[1]
        sphere.will = WillVector(x=dq_int8(w[0]), y=dq_int8(w[1]), z=dq_int8(w[2]))
        
        # Emotions & Values
        sphere.emotions = dq_int8(data[2])
        sphere.values = dq_int8(data[3])
        
        # Others
        # sub_concepts keys are loaded, but objects are lazy loaded
        sphere.language_tokens = data[5]
        sphere.mirror.intensity = dq_int8(data[7])
        
        sphere.created_at = float(data[8])
        sphere.last_activated = float(data[9])
        sphere.activation_count = data[10]
        
        # Qubit (if exists)
        if data[11] is not None:
            # We can't easily restore full qubit state from one observation, 
            # but we can init it.
            pass 
            
        # Sensory Signature (New in v2)
        if len(data) > 12:
            sphere.sensory_signature = data[12]
            
        return sphere
    
    def __repr__(self) -> str:
        return (f"<ConceptSphere '{self.id}': "
                f"Will={self.will.magnitude():.2f}, "
                f"Emotions={len(self.emotions)}, "
                f"Sensory={bool(self.sensory_signature)}, "
                f"Mirror={self.mirror.intensity:.2f}>")
