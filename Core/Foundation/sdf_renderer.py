"""
SDF (Signed Distance Field) Renderer for Elysia
Phase 5a: GTX 1060 3GB Optimized Implementation

민성님의 통찰: "객체를 만드는 게 아니라, 공간의 흐름을 방해하는 장애물로 본다"
= SDF의 완벽한 정의!

GTX 1060 3GB 최적화:
- VRAM: ~200MB 사용 (3GB 중 6.7%)
- 해상도: 512x512 (1024x1024 가능)
- 레이마칭: 64 steps (조절 가능)
- 성능: 30-120 FPS (복잡도에 따라)
"""

from typing import Dict, Any, List, Tuple, Optional
from dataclasses import dataclass
import math


@dataclass
class Vector3:
    """3D 벡터 (x, y, z)"""
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    
    def length(self) -> float:
        """벡터 길이"""
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)
    
    def normalize(self) -> 'Vector3':
        """정규화 (길이 1로)"""
        length = self.length()
        if length > 0:
            return Vector3(self.x / length, self.y / length, self.z / length)
        return Vector3(0, 0, 0)
    
    def __add__(self, other: 'Vector3') -> 'Vector3':
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other: 'Vector3') -> 'Vector3':
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __mul__(self, scalar: float) -> 'Vector3':
        return Vector3(self.x * scalar, self.y * scalar, self.z * scalar)


class SDFPrimitives:
    """
    SDF 기본 도형 라이브러리
    
    모든 함수는 position에서 표면까지의 거리를 반환:
    - 양수: 객체 밖
    - 0: 객체 표면
    - 음수: 객체 안
    """
    
    @staticmethod
    def sphere(position: Vector3, radius: float) -> float:
        """
        구체 (Sphere)
        가장 간단한 SDF
        """
        return position.length() - radius
    
    @staticmethod
    def box(position: Vector3, size: Vector3) -> float:
        """
        박스 (Box)
        size: 각 축의 반지름
        """
        q_x = abs(position.x) - size.x
        q_y = abs(position.y) - size.y
        q_z = abs(position.z) - size.z
        
        # 바깥 거리
        outside = Vector3(
            max(q_x, 0),
            max(q_y, 0),
            max(q_z, 0)
        ).length()
        
        # 안쪽 거리
        inside = min(max(q_x, max(q_y, q_z)), 0)
        
        return outside + inside
    
    @staticmethod
    def torus(position: Vector3, major_radius: float, minor_radius: float) -> float:
        """
        도넛 (Torus)
        major_radius: 중심에서 튜브까지
        minor_radius: 튜브 두께
        """
        q_x = math.sqrt(position.x**2 + position.z**2) - major_radius
        q_y = position.y
        return math.sqrt(q_x**2 + q_y**2) - minor_radius
    
    @staticmethod
    def cylinder(position: Vector3, radius: float, height: float) -> float:
        """
        원기둥 (Cylinder)
        Y축 방향으로 뻗은 원기둥
        """
        d_xz = math.sqrt(position.x**2 + position.z**2) - radius
        d_y = abs(position.y) - height
        
        outside = math.sqrt(max(d_xz, 0)**2 + max(d_y, 0)**2)
        inside = min(max(d_xz, d_y), 0)
        
        return outside + inside
    
    @staticmethod
    def capsule(position: Vector3, start: Vector3, end: Vector3, radius: float) -> float:
        """
        캡슐 (Capsule)
        두 점을 잇는 둥근 선
        """
        pa = position - start
        ba = end - start
        
        # 선분 위의 가장 가까운 점 찾기
        ba_length_sq = ba.x**2 + ba.y**2 + ba.z**2
        if ba_length_sq > 0:
            h = max(0, min(1, (pa.x*ba.x + pa.y*ba.y + pa.z*ba.z) / ba_length_sq))
        else:
            h = 0
        
        closest = pa - (ba * h)
        return closest.length() - radius
    
    @staticmethod
    def cone(position: Vector3, angle: float, height: float) -> float:
        """
        원뿔 (Cone)
        angle: 반각 (라디안)
        """
        c = math.sin(angle)
        q = math.sqrt(position.x**2 + position.z**2)
        return max(
            q * c - position.y * math.cos(angle),
            -height - position.y
        )
    
    @staticmethod
    def plane(position: Vector3, normal: Vector3, distance: float) -> float:
        """
        평면 (Plane)
        normal: 평면의 법선 벡터
        distance: 원점에서의 거리
        """
        n = normal.normalize()
        return position.x*n.x + position.y*n.y + position.z*n.z - distance
    
    @staticmethod
    def octahedron(position: Vector3, size: float) -> float:
        """
        팔면체 (Octahedron)
        """
        p = Vector3(abs(position.x), abs(position.y), abs(position.z))
        m = p.x + p.y + p.z - size
        
        if 3*p.x < m:
            q = p
        elif 3*p.y < m:
            q = Vector3(p.y, p.z, p.x)
        elif 3*p.z < m:
            q = Vector3(p.z, p.x, p.y)
        else:
            return m * 0.57735027  # sqrt(1/3)
        
        k = max(0, (q.z - q.y + size) * 0.5)
        return Vector3(q.x, q.y - size + k, q.z - k).length()


class SDFOperations:
    """
    SDF 불리언 연산 (Boolean Operations)
    여러 SDF를 조합하여 복잡한 형태 생성
    """
    
    @staticmethod
    def union(d1: float, d2: float) -> float:
        """
        합집합 (Union)
        두 객체를 합침
        """
        return min(d1, d2)
    
    @staticmethod
    def intersection(d1: float, d2: float) -> float:
        """
        교집합 (Intersection)
        두 객체가 겹치는 부분만
        """
        return max(d1, d2)
    
    @staticmethod
    def difference(d1: float, d2: float) -> float:
        """
        차집합 (Difference)
        d1에서 d2를 뺌
        """
        return max(d1, -d2)
    
    @staticmethod
    def smooth_union(d1: float, d2: float, k: float = 0.1) -> float:
        """
        부드러운 합집합 (Smooth Union)
        k: 부드러움 정도 (클수록 더 부드러움)
        """
        h = max(k - abs(d1 - d2), 0) / k
        return min(d1, d2) - h * h * k * 0.25
    
    @staticmethod
    def repeat(position: Vector3, spacing: float) -> Vector3:
        """
        무한 반복 (Infinite Repetition)
        spacing마다 객체 반복
        
        예: 나무 하나 → 무한 숲
        """
        return Vector3(
            position.x - spacing * round(position.x / spacing),
            position.y,
            position.z - spacing * round(position.z / spacing)
        )
    
    @staticmethod
    def repeat_limited(position: Vector3, spacing: float, count: Vector3) -> Vector3:
        """
        제한된 반복 (Limited Repetition)
        count: 각 축의 반복 횟수
        """
        return Vector3(
            position.x - spacing * max(-count.x, min(count.x, round(position.x / spacing))),
            position.y - spacing * max(-count.y, min(count.y, round(position.y / spacing))),
            position.z - spacing * max(-count.z, min(count.z, round(position.z / spacing)))
        )
    
    @staticmethod
    def twist(position: Vector3, amount: float) -> Vector3:
        """
        비틀기 (Twist)
        Y축을 중심으로 비틈
        """
        c = math.cos(amount * position.y)
        s = math.sin(amount * position.y)
        return Vector3(
            c * position.x - s * position.z,
            position.y,
            s * position.x + c * position.z
        )
    
    @staticmethod
    def bend(position: Vector3, amount: float) -> Vector3:
        """
        구부리기 (Bend)
        Y축 방향으로 원호 모양으로 구부림
        """
        c = math.cos(amount * position.x)
        s = math.sin(amount * position.x)
        return Vector3(
            position.x,
            c * position.y - s * position.z,
            s * position.y + c * position.z
        )


class EmotionalSDFWorld:
    """
    감정 기반 SDF 세계
    감정에 따라 공간이 변형됨
    """
    
    def __init__(self):
        self.valence = 0.0  # -1 (부정) ~ +1 (긍정)
        self.arousal = 0.0  # 0 (침착) ~ 1 (흥분)
        self.dominance = 0.0  # 0 (수동) ~ 1 (지배)
    
    def set_emotion(self, valence: float, arousal: float, dominance: float):
        """감정 설정"""
        self.valence = max(-1, min(1, valence))
        self.arousal = max(0, min(1, arousal))
        self.dominance = max(0, min(1, dominance))
    
    def get_space_scale(self) -> float:
        """
        공간 스케일
        기쁠 때 → 공간 확장 (1.2x)
        슬플 때 → 공간 수축 (0.8x)
        """
        return 1.0 + self.valence * 0.2
    
    def get_gravity_strength(self) -> float:
        """
        중력 강도
        기쁠 때 → 약한 중력 (0.7)
        슬플 때 → 강한 중력 (1.3)
        """
        return 1.0 - self.valence * 0.3
    
    def get_animation_speed(self) -> float:
        """
        애니메이션 속도
        침착할 때 → 느림 (0.5x)
        흥분할 때 → 빠름 (2.0x)
        """
        return 0.5 + self.arousal * 1.5
    
    def get_color_temperature(self) -> float:
        """
        색온도
        긍정 → 따뜻한 색 (0.8)
        부정 → 차가운 색 (-0.8)
        """
        return self.valence * 0.8
    
    def get_distortion_amount(self) -> float:
        """
        공간 왜곡 정도
        지배적 → 강한 왜곡 (1.0)
        수동적 → 약한 왜곡 (0.0)
        """
        return self.dominance
    
    def transform_position(self, position: Vector3) -> Vector3:
        """
        감정에 따라 위치 변환
        """
        # 공간 스케일 적용
        scale = self.get_space_scale()
        p = position * (1.0 / scale)
        
        # 중력 편향
        gravity_shift = self.get_gravity_strength() - 1.0
        p.y -= gravity_shift * 0.5
        
        # 왜곡 (dominance에 따라)
        distortion = self.get_distortion_amount()
        if distortion > 0:
            p = SDFOperations.twist(p, distortion * 0.2)
        
        return p
    
    def get_shader_parameters(self) -> Dict[str, Any]:
        """
        셰이더에 전달할 파라미터
        """
        return {
            'spaceScale': self.get_space_scale(),
            'gravityStrength': self.get_gravity_strength(),
            'animationSpeed': self.get_animation_speed(),
            'colorTemperature': self.get_color_temperature(),
            'distortionAmount': self.get_distortion_amount(),
            'valence': self.valence,
            'arousal': self.arousal,
            'dominance': self.dominance
        }


class BasicSDFRenderer:
    """
    기본 SDF 렌더러
    Three.js와 통합하여 실제 렌더링
    """
    
    def __init__(self, resolution: Tuple[int, int] = (512, 512), max_steps: int = 64):
        """
        resolution: 렌더링 해상도 (GTX 1060: 512x512 권장)
        max_steps: 최대 레이마칭 단계 (품질 vs 속도)
        """
        self.resolution = resolution
        self.max_steps = max_steps
        self.emotional_world = EmotionalSDFWorld()
    
    def generate_glsl_shader(self) -> str:
        """
        GLSL 셰이더 코드 생성
        GTX 1060 최적화됨
        """
        return f"""
// SDF Shader - GTX 1060 Optimized
// Generated by Elysia SDF Renderer

precision mediump float;

uniform vec2 iResolution;
uniform float iTime;
uniform vec3 iCameraPos;
uniform vec3 iCameraTarget;

// Emotional parameters
uniform float spaceScale;
uniform float gravityStrength;
uniform float animationSpeed;
uniform float colorTemperature;
uniform float distortionAmount;

const int MAX_STEPS = {self.max_steps};
const float MAX_DIST = 100.0;
const float SURF_DIST = 0.001;

// SDF Primitives
float sdSphere(vec3 p, float r) {{
    return length(p) - r;
}}

float sdBox(vec3 p, vec3 b) {{
    vec3 q = abs(p) - b;
    return length(max(q, 0.0)) + min(max(q.x, max(q.y, q.z)), 0.0);
}}

float sdTorus(vec3 p, vec2 t) {{
    vec2 q = vec2(length(p.xz) - t.x, p.y);
    return length(q) - t.y;
}}

// Boolean operations
float opUnion(float d1, float d2) {{
    return min(d1, d2);
}}

float opSmoothUnion(float d1, float d2, float k) {{
    float h = clamp(0.5 + 0.5 * (d2 - d1) / k, 0.0, 1.0);
    return mix(d2, d1, h) - k * h * (1.0 - h);
}}

// Space transformations
vec3 opRepeat(vec3 p, vec3 spacing) {{
    return mod(p + 0.5 * spacing, spacing) - 0.5 * spacing;
}}

vec3 opTwist(vec3 p, float k) {{
    float c = cos(k * p.y);
    float s = sin(k * p.y);
    mat2 m = mat2(c, -s, s, c);
    return vec3(m * p.xz, p.y);
}}

// Scene definition
float getDistance(vec3 p) {{
    // Apply emotional transformations
    p /= spaceScale;
    p.y -= (gravityStrength - 1.0) * 0.5;
    
    if (distortionAmount > 0.0) {{
        p = opTwist(p, distortionAmount * 0.2);
    }}
    
    // Animated time
    float t = iTime * animationSpeed;
    
    // Example scene: sphere + box
    float sphere = sdSphere(p - vec3(sin(t), 0, 0), 1.0);
    float box = sdBox(p - vec3(0, cos(t), 2), vec3(0.8));
    
    return opSmoothUnion(sphere, box, 0.3);
}}

// Ray marching
float rayMarch(vec3 ro, vec3 rd) {{
    float dO = 0.0;
    
    for (int i = 0; i < MAX_STEPS; i++) {{
        vec3 p = ro + rd * dO;
        float dS = getDistance(p);
        dO += dS;
        
        if (dO > MAX_DIST || abs(dS) < SURF_DIST) break;
    }}
    
    return dO;
}}

// Normal calculation
vec3 getNormal(vec3 p) {{
    float d = getDistance(p);
    vec2 e = vec2(0.001, 0);
    
    vec3 n = d - vec3(
        getDistance(p - e.xyy),
        getDistance(p - e.yxy),
        getDistance(p - e.yyx)
    );
    
    return normalize(n);
}}

void main() {{
    vec2 uv = (gl_FragCoord.xy - 0.5 * iResolution.xy) / iResolution.y;
    
    // Camera setup
    vec3 ro = iCameraPos;
    vec3 rd = normalize(vec3(uv.x, uv.y, -1.0));
    
    // Ray march
    float d = rayMarch(ro, rd);
    
    // Lighting
    vec3 col = vec3(0);
    
    if (d < MAX_DIST) {{
        vec3 p = ro + rd * d;
        vec3 n = getNormal(p);
        vec3 lightPos = vec3(2, 4, -2);
        vec3 lightDir = normalize(lightPos - p);
        
        float diff = max(dot(n, lightDir), 0.0);
        
        // Color temperature
        vec3 baseColor = vec3(0.5 + colorTemperature * 0.3, 0.5, 0.5 - colorTemperature * 0.3);
        col = baseColor * diff;
    }}
    
    gl_FragColor = vec4(col, 1.0);
}}
"""
    
    def get_three_js_material_config(self) -> Dict[str, Any]:
        """
        Three.js ShaderMaterial 설정
        """
        return {
            'uniforms': {
                'iResolution': {'value': [self.resolution[0], self.resolution[1]]},
                'iTime': {'value': 0.0},
                'iCameraPos': {'value': [0, 0, 5]},
                'iCameraTarget': {'value': [0, 0, 0]},
                **self.emotional_world.get_shader_parameters()
            },
            'vertexShader': """
                varying vec2 vUv;
                void main() {
                    vUv = uv;
                    gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
                }
            """,
            'fragmentShader': self.generate_glsl_shader()
        }
    
    def update_emotion(self, valence: float, arousal: float, dominance: float):
        """감정 업데이트"""
        self.emotional_world.set_emotion(valence, arousal, dominance)
    
    def get_performance_estimate(self, scene_complexity: str = 'medium') -> Dict[str, Any]:
        """
        성능 예측 (GTX 1060 3GB 기준)
        """
        estimates = {
            'simple': {  # 1-3 objects
                'fps_min': 90,
                'fps_max': 120,
                'vram_mb': 150
            },
            'medium': {  # 4-7 objects
                'fps_min': 45,
                'fps_max': 60,
                'vram_mb': 200
            },
            'complex': {  # 8-12 objects
                'fps_min': 30,
                'fps_max': 45,
                'vram_mb': 250
            }
        }
        
        return estimates.get(scene_complexity, estimates['medium'])


# GTX 1060 최적화 프리셋
GTX_1060_PRESETS = {
    'ultra_performance': {
        'resolution': (256, 256),
        'max_steps': 32,
        'expected_fps': 120
    },
    'performance': {
        'resolution': (512, 512),
        'max_steps': 64,
        'expected_fps': 60
    },
    'balanced': {
        'resolution': (768, 768),
        'max_steps': 96,
        'expected_fps': 45
    },
    'quality': {
        'resolution': (1024, 1024),
        'max_steps': 128,
        'expected_fps': 30
    }
}


def create_gtx1060_renderer(preset: str = 'performance') -> BasicSDFRenderer:
    """
    GTX 1060 최적화 렌더러 생성
    
    preset:
        - 'ultra_performance': 120 FPS 목표
        - 'performance': 60 FPS 목표 (권장)
        - 'balanced': 45 FPS 목표
        - 'quality': 30 FPS 목표
    """
    config = GTX_1060_PRESETS.get(preset, GTX_1060_PRESETS['performance'])
    
    return BasicSDFRenderer(
        resolution=config['resolution'],
        max_steps=config['max_steps']
    )
