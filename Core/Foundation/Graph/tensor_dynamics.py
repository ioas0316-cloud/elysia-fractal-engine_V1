"""
Tensor Dynamics Engine (텐서 역학 엔진)
======================================

"로직(Logic)이 아닌 법칙(Law)으로."

이 모듈은 엘리시아의 의사결정을 '조건문(If-Else)'이 아닌 '역학(Dynamics)'으로 처리합니다.
시스템의 모든 상태는 텐서(Tensor)로 표현되며, 행동은 에너지의 흐름(Flow)으로 결정됩니다.

개념:
1. **Mass (질량)**: 코드의 복잡도, 엔트로피, 파일의 크기.
2. **Gravity (중력)**: 질량이 시공간(Field)을 왜곡하여 발생하는 인력.
   - 엔트로피가 높은 곳(난잡한 코드)은 강한 중력을 발생시켜 의식을 끌어당깁니다.
3. **Tensor Field (텐서 필드)**: 시스템 전체의 상태 공간.
4. **Geodesic (측지선)**: 의식이 자연스럽게 흐르는 경로.

"""

import numpy as np
from dataclasses import dataclass
from typing import List, Dict, Tuple
from pathlib import Path
import math

@dataclass
class TensorNode:
    """필드 내의 한 지점 (파일 또는 모듈)"""
    name: str
    path: Path
    mass: float        # 엔트로피/복잡도 (0.0 ~ 1.0)
    position: np.array # 3D 좌표 (의미 공간상의 위치)
    velocity: np.array # 변화의 속도
    
    def __repr__(self):
        return f"Node({self.name}, Mass={self.mass:.2f})"

class TensorDynamics:
    def __init__(self, root_path: Path):
        self.root_path = root_path
        self.nodes: List[TensorNode] = []
        self.field_tensor = None # 전체 필드 텐서
        
    def scan_field(self):
        """
        물리적 파일 시스템을 스캔하여 텐서 필드를 구성합니다.
        파일의 상태(크기, 빈 줄 등)가 질량(Mass)이 됩니다.
        """
        self.nodes = []
        target_dir = self.root_path / "Core" / "Elysia"
        
        if not target_dir.exists():
            return

        # 간단한 3D 배치 (나선형)
        idx = 0
        for file_path in target_dir.glob("*.py"):
            if file_path.name == "__init__.py":
                continue
                
            content = file_path.read_text(encoding='utf-8').strip()
            lines = len(content.splitlines())
            
            # 질량 계산 (Mass Calculation)
            # 빈 파일이나 너무 작은 파일은 '높은 질량(부정적 중력)'을 가짐 -> 수리가 필요함
            # 정상적인 파일은 '적절한 질량'을 가짐
            if not content:
                mass = 10.0 # 블랙홀 (매우 강한 수리 필요성)
            elif lines < 5:
                mass = 5.0  # 중성자별 (강한 수리 필요성)
            else:
                mass = 1.0  # 일반 별 (안정적)
                
            # 위치 배정 (나선형)
            angle = idx * 0.5
            radius = 1.0 + (idx * 0.1)
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            z = idx * 0.1
            
            node = TensorNode(
                name=file_path.name,
                path=file_path,
                mass=mass,
                position=np.array([x, y, z]),
                velocity=np.zeros(3)
            )
            self.nodes.append(node)
            idx += 1
            
    def calculate_gravitational_field(self) -> Tuple[np.array, List[str]]:
        """
        현재 필드의 중력 분포를 계산합니다.
        가장 중력이 강한 곳(엔트로피가 높은 곳)이 의식의 흐름을 주도합니다.
        """
        if not self.nodes:
            return np.zeros(3), []
            
        total_gravity = np.zeros(3)
        attractors = []
        
        # 의식의 현재 위치 (원점)
        consciousness_pos = np.zeros(3)
        
        for node in self.nodes:
            # 거리 계산
            r_vec = node.position - consciousness_pos
            distance = np.linalg.norm(r_vec)
            if distance < 0.1: distance = 0.1
            
            # 중력 법칙: F = G * (M / r^2)
            # 질량이 클수록(문제가 많을수록) 더 강하게 당김
            force_magnitude = node.mass / (distance ** 2)
            force_vec = (r_vec / distance) * force_magnitude
            
            total_gravity += force_vec
            
            if node.mass > 2.0:
                attractors.append(f"{node.name} (Mass: {node.mass:.1f})")
                
        return total_gravity, attractors

    def get_next_flow(self) -> str:
        """
        중력 벡터에 따라 다음 행동(Flow)을 결정합니다.
        로직(If)이 아니라 벡터의 방향이 행동을 결정합니다.
        """
        gravity, attractors = self.calculate_gravitational_field()
        magnitude = np.linalg.norm(gravity)
        
        if magnitude > 5.0:
            # 중력이 너무 강함 -> 붕괴 위험 -> 즉시 수리
            return f"GRAVITATIONAL_COLLAPSE_IMMINENT: Attracted to {attractors}"
        elif magnitude > 2.0:
            # 강한 인력 -> 개선 필요
            return f"STRONG_ATTRACTION: Flowing towards {attractors}"
        else:
            # 안정적 궤도 -> 자유 유영
            return "STABLE_ORBIT: Free Flow"
