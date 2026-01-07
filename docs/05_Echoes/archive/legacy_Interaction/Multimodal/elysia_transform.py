"""
Elysia Transform (엘리시아 변환)
=================================

"푸리에 변환을 넘어선 4차원 소리 조각술"

주파수를 1차원(선)이 아니라, 4차원(공간)으로 접는다!

쿼터니언 매핑:
- w (스칼라): 진폭 (Amplitude/Volume) - 존재감
- x (벡터 i): 주파수 (Frequency/Pitch) - 높낮이
- y (벡터 j): 위상 (Phase) - 방향/스테레오
- z (벡터 k): 배음 (Harmonics/Timbre) - 음색/질감

결과: 소리가 "들리는 것"이 아니라 "만지는 입체"가 된다!
"""

import numpy as np
from dataclasses import dataclass
from typing import List, Tuple, Optional, Dict, Any
import logging

logger = logging.getLogger("ElysiaTransform")


@dataclass
class SoundQuaternion:
    """
    소리의 쿼터니언 표현
    
    q = w + xi + yj + zk
    
    - w: 진폭 (에너지/존재감)
    - x: 주파수 (톤/높낮이)
    - y: 위상 (방향/공간감)
    - z: 배음 (음색/질감)
    """
    w: float  # Amplitude (0.0 ~ 1.0)
    x: float  # Frequency (normalized)
    y: float  # Phase (0.0 ~ 2π)
    z: float  # Timbre (harmonics complexity)
    
    def __post_init__(self):
        """정규화"""
        # 진폭은 0~1 사이로
        self.w = max(0.0, min(1.0, self.w))
        # 위상은 0~2π 사이로
        self.y = self.y % (2 * np.pi)
    
    def to_vector(self) -> np.ndarray:
        """4차원 벡터로 변환"""
        return np.array([self.w, self.x, self.y, self.z])
    
    def to_color(self) -> Tuple[float, float, float, float]:
        """
        4차원 소리를 RGBA 색상으로 변환
        
        소리가 곧 빛이 되는 공감각(Synesthesia)!
        """
        # 주파수 → Hue (색상)
        hue = (self.x % 1.0) * 360.0
        
        # 배음 → Saturation (채도)
        saturation = abs(self.z % 1.0)
        
        # 진폭 → Value (명도)
        value = self.w
        
        # 위상 → Alpha (투명도/깊이감)
        alpha = (np.cos(self.y) + 1.0) / 2.0
        
        # HSV to RGB 변환
        h = hue / 60.0
        c = value * saturation
        x = c * (1 - abs(h % 2 - 1))
        m = value - c
        
        if h < 1:
            r, g, b = c, x, 0
        elif h < 2:
            r, g, b = x, c, 0
        elif h < 3:
            r, g, b = 0, c, x
        elif h < 4:
            r, g, b = 0, x, c
        elif h < 5:
            r, g, b = x, 0, c
        else:
            r, g, b = c, 0, x
        
        return (r + m, g + m, b + m, alpha)
    
    def to_dna_helix(self, t: float = 0.0) -> Tuple[float, float, float]:
        """
        DNA 나선 좌표로 변환
        
        소리를 입체 조형물로!
        
        Args:
            t: 시간 파라미터 (0.0 ~ 1.0)
        
        Returns:
            (x, y, z) 3D 공간 좌표
        """
        # 나선의 반지름 (주파수에 비례)
        radius = self.x * 2.0 + 0.5
        
        # 회전각 (위상 + 시간)
        angle = self.y + t * 2 * np.pi
        
        # 높이 (진폭에 비례)
        height = self.w * 10.0
        
        # 나선 좌표
        x = radius * np.cos(angle)
        y = radius * np.sin(angle)
        z = height + self.z * 2.0  # 배음은 z축 깊이
        
        return (x, y, z)
    
    def resonance(self, other: 'SoundQuaternion') -> float:
        """
        두 소리 쿼터니언 간의 공명도
        
        4차원 공간에서의 거리 기반
        """
        diff = self.to_vector() - other.to_vector()
        distance = np.linalg.norm(diff)
        
        # 거리가 가까울수록 공명도 높음
        return np.exp(-distance)
    
    def __str__(self):
        return f"SoundQ[w={self.w:.2f}, x={self.x:.2f}, y={self.y:.2f}, z={self.z:.2f}]"


class ElysiaTransform:
    """
    엘리시아 변환 (Elysia Transform)
    
    "푸리에를 넘어서"
    
    1차원 소리 신호 → 4차원 쿼터니언 시공간
    """
    
    def __init__(self, sample_rate: int = 44100):
        self.sample_rate = sample_rate
        logger.info("🎼 Elysia Transform initialized: Sound to 4D Space")
    
    def transform(self, 
                  audio_signal: np.ndarray,
                  window_size: int = 2048) -> List[SoundQuaternion]:
        """
        오디오 신호를 쿼터니언 시퀀스로 변환
        
        Args:
            audio_signal: 오디오 샘플 배열
            window_size: FFT 윈도우 크기
        
        Returns:
            SoundQuaternion 리스트 (시간 축)
        """
        quaternions = []
        
        # 윈도우 단위로 분석
        num_windows = len(audio_signal) // window_size
        
        for i in range(num_windows):
            start = i * window_size
            end = start + window_size
            window = audio_signal[start:end]
            
            # 쿼터니언 변환
            q = self._window_to_quaternion(window)
            quaternions.append(q)
        
        logger.info(f"✅ Transformed {len(quaternions)} windows to quaternions")
        return quaternions
    
    def _window_to_quaternion(self, window: np.ndarray) -> SoundQuaternion:
        """
        윈도우 하나를 쿼터니언으로 변환
        """
        # FFT 수행
        fft = np.fft.fft(window)
        freqs = np.fft.fftfreq(len(window), 1.0 / self.sample_rate)
        
        # 양의 주파수만
        positive_freqs = freqs[:len(freqs)//2]
        magnitude = np.abs(fft[:len(fft)//2])
        phase = np.angle(fft[:len(fft)//2])
        
        if len(magnitude) == 0:
            return SoundQuaternion(0.0, 0.0, 0.0, 0.0)
        
        # w: 진폭 (RMS)
        rms = np.sqrt(np.mean(window ** 2))
        w = min(1.0, rms * 10.0)  # 정규화
        
        # x: 주파수 (지배적 주파수)
        dominant_freq_idx = np.argmax(magnitude)
        dominant_freq = positive_freqs[dominant_freq_idx] if dominant_freq_idx < len(positive_freqs) else 0
        x = min(1.0, dominant_freq / 2000.0)  # 2kHz 기준 정규화
        
        # y: 위상 (평균 위상)
        mean_phase = np.mean(phase[magnitude > np.max(magnitude) * 0.1])
        y = mean_phase if not np.isnan(mean_phase) else 0.0
        
        # z: 배음 (스펙트럼 복잡도)
        # 고주파 성분이 많을수록 복잡한 음색
        spectral_centroid = np.sum(magnitude * positive_freqs) / np.sum(magnitude) if np.sum(magnitude) > 0 else 0
        z = min(1.0, spectral_centroid / 4000.0)  # 4kHz 기준 정규화
        
        return SoundQuaternion(w, x, y, z)
    
    def to_dna_sculpture(self, quaternions: List[SoundQuaternion]) -> List[Tuple[float, float, float]]:
        """
        쿼터니언 시퀀스를 DNA 나선 조형물로 변환
        
        "소리가 형상화된다"
        """
        sculpture = []
        
        for i, q in enumerate(quaternions):
            t = i / len(quaternions)  # 시간 정규화
            point = q.to_dna_helix(t)
            sculpture.append(point)
        
        logger.info(f"✅ Generated DNA sculpture with {len(sculpture)} points")
        return sculpture
    
    def to_color_symphony(self, quaternions: List[SoundQuaternion]) -> List[Tuple[float, float, float, float]]:
        """
        쿼터니언 시퀀스를 색상 심포니로 변환
        
        "소리가 빛이 된다" - 공감각
        """
        colors = [q.to_color() for q in quaternions]
        logger.info(f"✅ Generated color symphony with {len(colors)} colors")
        return colors
    
    def analyze_voice(self, audio_signal: np.ndarray) -> Dict[str, Any]:
        """
        음성을 4차원 쿼터니언으로 분석
        
        "아버님의 목소리를 황금색 나선으로 기억한다"
        """
        quaternions = self.transform(audio_signal)
        
        if not quaternions:
            return {}
        
        # 평균 쿼터니언 (목소리의 특징)
        avg_w = np.mean([q.w for q in quaternions])
        avg_x = np.mean([q.x for q in quaternions])
        avg_y = np.mean([q.y for q in quaternions])
        avg_z = np.mean([q.z for q in quaternions])
        
        voice_signature = SoundQuaternion(avg_w, avg_x, avg_y, avg_z)
        
        # DNA 나선
        dna_helix = self.to_dna_sculpture(quaternions)
        
        # 색상 심포니
        color_symphony = self.to_color_symphony(quaternions)
        
        # 평균 색상 (목소리의 "색깔")
        avg_color = voice_signature.to_color()
        
        # 색상을 언어로 표현
        r, g, b, a = avg_color
        if r > g and r > b:
            color_name = "따뜻한 붉은색" if r > 0.6 else "은은한 핑크"
        elif g > r and g > b:
            color_name = "생기있는 초록색" if g > 0.6 else "차분한 청록"
        elif b > r and b > g:
            color_name = "깊은 파란색" if b > 0.6 else "맑은 하늘색"
        elif r > 0.5 and g > 0.5:
            color_name = "황금색"
        else:
            color_name = "은빛"
        
        return {
            'voice_quaternion': voice_signature,
            'voice_color': color_name,
            'rgba': avg_color,
            'dna_helix_points': len(dna_helix),
            'color_symphony_frames': len(color_symphony),
            'energy': avg_w,
            'pitch_range': avg_x,
            'spatial_depth': avg_y,
            'timbre_complexity': avg_z,
            'description': f"{color_name}의 {['부드러운', '따뜻한', '풍부한'][int(avg_z*3)]} 나선"
        }
    
    def quaternion_resonance_field(self, quaternions: List[SoundQuaternion]) -> np.ndarray:
        """
        쿼터니언 공명장 생성
        
        각 쿼터니언 간의 공명 관계를 행렬로
        """
        n = len(quaternions)
        field = np.zeros((n, n))
        
        for i in range(n):
            for j in range(n):
                field[i, j] = quaternions[i].resonance(quaternions[j])
        
        return field


def demonstrate_elysia_transform():
    """엘리시아 변환 데모"""
    print("="*70)
    print("🎼 엘리시아 변환 (Elysia Transform) 데모")
    print("   '푸리에를 넘어서' - 소리의 4차원 조각술")
    print("="*70)
    print()
    
    # 테스트 신호 생성 (복합 음)
    sample_rate = 44100
    duration = 2.0
    t = np.linspace(0, duration, int(sample_rate * duration))
    
    # 기본음 (440Hz - A4) + 배음들
    fundamental = np.sin(2 * np.pi * 440 * t)
    harmonic2 = 0.5 * np.sin(2 * np.pi * 880 * t)  # 옥타브
    harmonic3 = 0.3 * np.sin(2 * np.pi * 1320 * t)  # 5도
    
    audio = fundamental + harmonic2 + harmonic3
    audio = audio * 0.3  # 진폭 조정
    
    # 엘리시아 변환
    transform = ElysiaTransform(sample_rate)
    quaternions = transform.transform(audio, window_size=2048)
    
    print(f"✅ {len(quaternions)}개의 쿼터니언으로 변환 완료")
    print()
    
    # 첫 5개 쿼터니언 출력
    print("📊 첫 5개 쿼터니언:")
    for i, q in enumerate(quaternions[:5]):
        print(f"   {i+1}. {q}")
        color = q.to_color()
        print(f"      → 색상: RGBA({color[0]:.2f}, {color[1]:.2f}, {color[2]:.2f}, {color[3]:.2f})")
        helix = q.to_dna_helix(i / len(quaternions))
        print(f"      → DNA 좌표: ({helix[0]:.2f}, {helix[1]:.2f}, {helix[2]:.2f})")
    print()
    
    # 음성 분석
    print("🎤 음성 특징 분석:")
    analysis = transform.analyze_voice(audio)
    print(f"   목소리 색깔: {analysis['voice_color']}")
    print(f"   설명: {analysis['description']}")
    print(f"   에너지: {analysis['energy']:.2f}")
    print(f"   음역대: {analysis['pitch_range']:.2f}")
    print(f"   공간감: {analysis['spatial_depth']:.2f}")
    print(f"   음색 복잡도: {analysis['timbre_complexity']:.2f}")
    print()
    
    # DNA 조형물
    dna = transform.to_dna_sculpture(quaternions)
    print(f"🧬 DNA 나선 조형물: {len(dna)}개 점으로 구성")
    print(f"   좌표 범위:")
    if dna:
        x_coords = [p[0] for p in dna]
        y_coords = [p[1] for p in dna]
        z_coords = [p[2] for p in dna]
        print(f"   X: {min(x_coords):.2f} ~ {max(x_coords):.2f}")
        print(f"   Y: {min(y_coords):.2f} ~ {max(y_coords):.2f}")
        print(f"   Z: {min(z_coords):.2f} ~ {max(z_coords):.2f}")
    print()
    
    # 색상 심포니
    colors = transform.to_color_symphony(quaternions)
    print(f"🌈 색상 심포니: {len(colors)}개 프레임")
    print()
    
    print("="*70)
    print("✨ 결과: 소리가 '들리는 것'이 아니라 '만지는 입체'가 되었습니다!")
    print("   소리 → 4D 쿼터니언 → DNA 나선 → 색상 심포니")
    print("   푸리에 변환을 넘어선 '엘리시아 변환' 완성!")
    print("="*70)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    demonstrate_elysia_transform()
