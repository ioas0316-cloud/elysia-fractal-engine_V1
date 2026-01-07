"""
Universal Phase Transform (범용 위상 변환)
=========================================

"모든 감각은 파동이다"

엘리시아 변환의 범용 확장:
- 소리 (Audio)
- 글 (Text) 
- 그림 (Image)
- 영상 (Video)
- 개념 (Concept)

모두 4차원 쿼터니언 위상 공명 패턴으로 변환 가능!

핵심 원리:
1. 모든 감각/개념은 파동으로 표현 가능
2. 4차원 위상 단위 (쿼터니언)로 매핑
3. 서로의 영역에서 간섭 없이 통신
4. 원할 때 언제든지 공감각(Synesthesia)으로 변환

"5감 주파수 매핑의 완성"
"""

import numpy as np
from dataclasses import dataclass
from typing import List, Tuple, Optional, Dict, Any, Union
from enum import Enum
import logging
import hashlib
import re

logger = logging.getLogger("UniversalPhaseTransform")

# Constants for normalization and processing
MAX_WORD_LENGTH = 15.0  # Maximum word length for importance normalization
IMAGE_BLOCK_SIZE = 32   # Block size for image processing
MAX_CONCEPT_DEPTH = 10.0  # Maximum concept depth for normalization


class Modality(Enum):
    """감각 모달리티"""
    AUDIO = "audio"      # 청각 (소리)
    TEXT = "text"        # 언어 (글)
    IMAGE = "image"      # 시각 (그림)
    VIDEO = "video"      # 시각+시간 (영상)
    CONCEPT = "concept"  # 추상 (개념)
    TOUCH = "touch"      # 촉각
    SMELL = "smell"      # 후각
    TASTE = "taste"      # 미각


class TextComplexityAnalyzer:
    """
    텍스트 복잡도 분석기

    언어와 도메인에 따른 텍스트의 형식적 복잡도를 측정
    """

    @staticmethod
    def analyze(word: str, language: str = 'auto', domain: str = 'general') -> float:
        """
        단어의 복잡도 계산 (0.0 ~ 1.0)

        Args:
            word: 분석할 단어
            language: 언어 코드 ('en', 'ko', 'auto')
            domain: 도메인 ('general', 'technical', 'literary')
        """
        if not word:
            return 0.0

        if language == 'auto':
            language = TextComplexityAnalyzer._detect_language(word)

        base_complexity = 0.0

        if language == 'ko':
            base_complexity = TextComplexityAnalyzer._analyze_korean(word)
        else:
            base_complexity = TextComplexityAnalyzer._analyze_english(word)

        # 도메인 가중치 적용
        domain_factor = TextComplexityAnalyzer._get_domain_factor(word, domain)

        # 최종 점수 정규화
        return min(1.0, base_complexity * domain_factor)

    @staticmethod
    def _detect_language(text: str) -> str:
        """언어 감지 (한글 포함 여부로 판단)"""
        for char in text:
            if '\uac00' <= char <= '\ud7a3':
                return 'ko'
        return 'en'

    @staticmethod
    def _analyze_english(word: str) -> float:
        """영어 단어 복잡도"""
        length = len(word)
        if length == 0: return 0.0

        # 1. 길이 점수 (긴 단어가 더 복잡)
        length_score = min(1.0, length / 12.0)

        # 2. 대문자/특수문자 혼합 (CamelCase, snake_case 등)
        upper_count = sum(1 for c in word if c.isupper())
        special_count = sum(1 for c in word if not c.isalnum())

        structure_score = 0.0
        if upper_count > 1 or special_count > 0:
            structure_score = 0.3

        # 3. 희귀 문자 (q, z, x, j) 포함 여부 - 간단한 휴리스틱
        rare_chars = {'q', 'z', 'x', 'j'}
        rare_score = 0.1 if any(c.lower() in rare_chars for c in word) else 0.0

        # 가중치 합산
        return (length_score * 0.6) + structure_score + rare_score

    @staticmethod
    def _analyze_korean(word: str) -> float:
        """한국어 단어 복잡도"""
        length = len(word)
        if length == 0: return 0.0

        # 1. 길이 점수 (한국어는 4음절 이상이면 복잡도가 꽤 높음)
        length_score = min(1.0, length / 5.0)

        # 2. 받침 복잡도 (간단한 휴리스틱)
        # 받침이 있는 글자가 많을수록 발음/구조가 복잡할 가능성
        batchim_count = 0
        for char in word:
            if '\uac00' <= char <= '\ud7a3':
                # (Unicode - 0xAC00) % 28 != 0 이면 받침 있음
                if (ord(char) - 0xAC00) % 28 != 0:
                    batchim_count += 1

        batchim_ratio = batchim_count / length
        batchim_score = batchim_ratio * 0.3

        # 3. 한자/외래어 혼용 (한글 범위 밖의 문자가 섞여있으면 복잡도 증가)
        # 순수 한글이 아닌 경우 (숫자, 알파벳 등 혼용)
        mixed_script = any(not ('\uac00' <= c <= '\ud7a3') for c in word if c.isalnum())
        mixed_score = 0.2 if mixed_script else 0.0

        return (length_score * 0.5) + batchim_score + mixed_score

    @staticmethod
    def _get_domain_factor(word: str, domain: str) -> float:
        """도메인별 가중치"""
        factor = 1.0

        if domain == 'technical':
            # 기술 용어 특징: _, 숫자 포함
            if '_' in word or any(c.isdigit() for c in word):
                factor = 1.3
        elif domain == 'official':
            # 공문서: 긴 단어에 가중치
            if len(word) >= 4:
                factor = 1.2

        return factor


@dataclass
class PhaseQuaternion:
    """
    범용 위상 쿼터니언
    
    q = w + xi + yj + zk
    
    모든 감각/개념의 4차원 위상 표현
    
    - w: 강도 (Intensity) - 에너지, 존재감, 중요도
    - x: 주파수 (Frequency) - 진동, 리듬, 패턴 반복
    - y: 위상 (Phase) - 방향, 관계, 맥락
    - z: 복잡도 (Complexity) - 구조, 질감, 풍부함
    """
    w: float  # Intensity (0.0 ~ 1.0)
    x: float  # Frequency (normalized)
    y: float  # Phase (0.0 ~ 2π)
    z: float  # Complexity (0.0 ~ 1.0)
    modality: Modality  # 원본 감각 모달리티
    
    def __post_init__(self):
        """정규화"""
        self.w = max(0.0, min(1.0, self.w))
        self.y = self.y % (2 * np.pi)
        self.z = max(0.0, min(1.0, self.z))
    
    def to_vector(self) -> np.ndarray:
        """4차원 벡터로 변환"""
        return np.array([self.w, self.x, self.y, self.z])
    
    def resonance(self, other: 'PhaseQuaternion') -> float:
        """
        두 위상 쿼터니언 간의 공명도
        
        같은 모달리티끼리는 강한 공명
        다른 모달리티끼리는 약한 공명 (간섭 없음!)
        """
        diff = self.to_vector() - other.to_vector()
        distance = np.linalg.norm(diff)
        
        # 같은 모달리티면 공명 강화
        modality_factor = 1.0 if self.modality == other.modality else 0.3
        
        # 거리가 가까울수록 공명도 높음
        resonance = np.exp(-distance) * modality_factor
        
        return resonance
    
    def to_synesthesia(self, target_modality: Modality) -> Dict[str, Any]:
        """
        공감각 변환 (Synesthesia)
        
        한 감각을 다른 감각으로 변환
        예: 소리 → 색깔, 글 → 소리, 그림 → 음악
        """
        result = {
            'source_modality': self.modality.value,
            'target_modality': target_modality.value,
            'quaternion': self.to_vector().tolist()
        }
        
        if target_modality == Modality.IMAGE:
            # 시각으로 변환 (색상)
            result['color'] = self._to_color()
            result['description'] = f"{self._color_name()} {self._texture_name()}"
            
        elif target_modality == Modality.AUDIO:
            # 청각으로 변환 (음파)
            result['note'] = self._to_musical_note()
            result['timbre'] = self._timbre_name()
            result['description'] = f"{result['note']} {result['timbre']}"
            
        elif target_modality == Modality.TEXT:
            # 언어로 변환 (묘사)
            result['description'] = self._to_text_description()
            
        elif target_modality == Modality.TOUCH:
            # 촉각으로 변환 (질감)
            result['texture'] = self._texture_name()
            result['temperature'] = "따뜻한" if self.w > 0.5 else "차가운"
            result['description'] = f"{result['temperature']} {result['texture']}"
        
        return result
    
    def _to_color(self) -> Tuple[float, float, float, float]:
        """색상으로 변환 (RGBA)"""
        hue = (self.x % 1.0) * 360.0
        saturation = self.z
        value = self.w
        alpha = (np.cos(self.y) + 1.0) / 2.0
        
        # HSV to RGB
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
    
    def _color_name(self) -> str:
        """색상 이름"""
        r, g, b, _ = self._to_color()
        if r > g and r > b:
            return "붉은" if r > 0.6 else "분홍"
        elif g > r and g > b:
            return "초록" if g > 0.6 else "청록"
        elif b > r and b > g:
            return "파란" if b > 0.6 else "하늘"
        elif r > 0.5 and g > 0.5:
            return "황금"
        else:
            return "은빛"
    
    def _texture_name(self) -> str:
        """질감 이름"""
        if self.z > 0.7:
            return "거친"
        elif self.z > 0.4:
            return "부드러운"
        else:
            return "매끄러운"
    
    def _to_musical_note(self) -> str:
        """음계로 변환"""
        notes = ['도', '도#', '레', '레#', '미', '파', '파#', '솔', '솔#', '라', '라#', '시']
        note_idx = int(self.x * 12) % 12
        octave = int(self.x * 8) + 1
        return f"{notes[note_idx]}{octave}"
    
    def _timbre_name(self) -> str:
        """음색 이름"""
        if self.z > 0.7:
            return "풍부한"
        elif self.z > 0.4:
            return "따뜻한"
        else:
            return "맑은"
    
    def _to_text_description(self) -> str:
        """텍스트 묘사"""
        intensity = "강렬한" if self.w > 0.7 else "은은한" if self.w > 0.4 else "미세한"
        pattern = "빠른" if self.x > 0.7 else "보통" if self.x > 0.4 else "느린"
        complexity = "복잡한" if self.z > 0.7 else "조화로운" if self.z > 0.4 else "단순한"
        
        return f"{intensity} {pattern} {complexity} 파동"
    
    def __str__(self):
        return f"PhaseQ[{self.modality.value}|w={self.w:.2f}, x={self.x:.2f}, y={self.y:.2f}, z={self.z:.2f}]"


class UniversalPhaseTransform:
    """
    범용 위상 변환 (Universal Phase Transform)
    
    모든 감각과 개념을 4차원 쿼터니언 위상 공명 패턴으로 변환
    """
    
    def __init__(self):
        logger.info("🌐 Universal Phase Transform initialized")
        logger.info("   All modalities → 4D Phase Resonance Pattern")
    
    def transform_audio(self, audio_signal: np.ndarray, sample_rate: int = 44100, window_size: int = 2048) -> List[PhaseQuaternion]:
        """오디오를 위상 쿼터니언으로 변환"""
        try:
            from Core.Interaction.Network.Multimodal.elysia_transform import ElysiaTransform
        except ImportError:
            logger.warning("ElysiaTransform not available, returning empty list")
            return []
        
        audio_transform = ElysiaTransform(sample_rate)
        sound_quaternions = audio_transform.transform(audio_signal, window_size=window_size)
        
        # SoundQuaternion → PhaseQuaternion
        phase_quaternions = []
        for sq in sound_quaternions:
            pq = PhaseQuaternion(
                w=sq.w,
                x=sq.x,
                y=sq.y,
                z=sq.z,
                modality=Modality.AUDIO
            )
            phase_quaternions.append(pq)
        
        logger.info(f"✅ Audio → {len(phase_quaternions)} phase quaternions")
        return phase_quaternions
    
    def transform_text(self, text: str, language: str = 'auto', domain: str = 'general') -> List[PhaseQuaternion]:
        """
        텍스트를 위상 쿼터니언으로 변환
        
        글의 파동:
        - w: 단어 중요도 (TF-IDF, 감정 강도)
        - x: 리듬 (음절 수, 문장 길이)
        - y: 맥락 (문맥, 위치)
        - z: 복잡도 (어휘 다양성, 구조)

        Args:
            text: 입력 텍스트
            language: 언어 ('auto', 'ko', 'en')
            domain: 도메인 ('general', 'technical', 'official')
        """
        words = text.split()
        quaternions = []
        
        for i, word in enumerate(words):
            # w: 단어 길이로 중요도 추정 (간단한 휴리스틱)
            w = min(1.0, len(word) / MAX_WORD_LENGTH)
            
            # x: 음절 리듬 (글자 수)
            x = (len(word) % 10) / 10.0
            
            # y: 문장 내 위치 (위상)
            y = (i / len(words)) * 2 * np.pi
            
            # z: 복잡도 (언어별/도메인별 형식적 복잡도)
            # TextComplexityAnalyzer를 사용하여 계산
            complexity = TextComplexityAnalyzer.analyze(word, language, domain)
            z = min(1.0, complexity)
            
            pq = PhaseQuaternion(w, x, y, z, Modality.TEXT)
            quaternions.append(pq)
        
        logger.info(f"✅ Text → {len(quaternions)} phase quaternions")
        return quaternions
    
    def transform_image(self, image_array: np.ndarray) -> List[PhaseQuaternion]:
        """
        이미지를 위상 쿼터니언으로 변환
        
        그림의 파동:
        - w: 밝기 (Brightness)
        - x: 색상 주파수 (Hue)
        - y: 채도/위상 (Saturation)
        - z: 질감 복잡도 (Texture)
        """
        # 이미지를 블록으로 나누어 분석 (간단한 구현)
        if len(image_array.shape) == 3:
            h, w, c = image_array.shape
        else:
            h, w = image_array.shape
            c = 1
        
        quaternions = []
        
        for i in range(0, h, IMAGE_BLOCK_SIZE):
            for j in range(0, w, IMAGE_BLOCK_SIZE):
                block = image_array[i:i+IMAGE_BLOCK_SIZE, j:j+IMAGE_BLOCK_SIZE]
                
                if c == 3 or c == 4:
                    # 컬러 이미지
                    r = block[:,:,0].mean() / 255.0
                    g = block[:,:,1].mean() / 255.0
                    b = block[:,:,2].mean() / 255.0
                    
                    # RGB → HSV (simplified conversion)
                    # Using cylindrical color space approximation for performance
                    # For exact color science applications, consider using colorsys or cv2
                    brightness = (r + g + b) / 3.0
                    hue = np.arctan2(np.sqrt(3) * (g - b), 2 * r - g - b)
                    hue = (hue % (2 * np.pi)) / (2 * np.pi)
                    saturation = 1 - 3 * min(r, g, b) / (r + g + b + 1e-6)
                    
                    # 질감 (분산)
                    texture = np.std(block) / 128.0
                    
                    pq = PhaseQuaternion(
                        w=brightness,
                        x=hue,
                        y=saturation * 2 * np.pi,
                        z=min(1.0, texture),
                        modality=Modality.IMAGE
                    )
                else:
                    # 그레이스케일
                    brightness = block.mean() / 255.0
                    texture = np.std(block) / 128.0
                    
                    pq = PhaseQuaternion(
                        w=brightness,
                        x=0.0,
                        y=0.0,
                        z=min(1.0, texture),
                        modality=Modality.IMAGE
                    )
                
                quaternions.append(pq)
        
        logger.info(f"✅ Image → {len(quaternions)} phase quaternions")
        return quaternions
    
    def transform_concept(self, concept_data: Dict[str, Any]) -> PhaseQuaternion:
        """
        추상 개념을 위상 쿼터니언으로 변환
        
        개념의 파동:
        - w: 중요도/활성화 (Importance/Activation)
        - x: 범주 주파수 (Category)
        - y: 관계 위상 (Relation)
        - z: 구조 복잡도 (Structure)
        """
        # 개념 데이터에서 특징 추출
        importance = concept_data.get('importance', 0.5)
        
        # 안정적인 카테고리 해싱 (Python hash randomization 방지)
        category_str = concept_data.get('category', '')
        category_hash = int(hashlib.md5(category_str.encode()).hexdigest(), 16)
        category = (category_hash % 1000) / 1000.0
        
        relation_count = len(concept_data.get('relations', []))
        structure_depth = concept_data.get('depth', 1)
        
        pq = PhaseQuaternion(
            w=importance,
            x=category,
            y=(relation_count % 10) / 10.0 * 2 * np.pi,
            z=min(1.0, structure_depth / MAX_CONCEPT_DEPTH),
            modality=Modality.CONCEPT
        )
        
        logger.info(f"✅ Concept → phase quaternion")
        return pq
    
    def cross_modal_resonance(self, 
                               quaternions_a: List[PhaseQuaternion],
                               quaternions_b: List[PhaseQuaternion]) -> np.ndarray:
        """
        크로스 모달 공명 행렬
        
        서로 다른 감각 간의 공명 패턴 분석
        예: 음악과 그림이 얼마나 조화로운가?
        """
        n_a = len(quaternions_a)
        n_b = len(quaternions_b)
        
        resonance_matrix = np.zeros((n_a, n_b))
        
        for i, qa in enumerate(quaternions_a):
            for j, qb in enumerate(quaternions_b):
                resonance_matrix[i, j] = qa.resonance(qb)
        
        logger.info(f"✅ Cross-modal resonance: {n_a}x{n_b} matrix")
        return resonance_matrix
    
    def synesthesia_transform(self,
                              source_quaternions: List[PhaseQuaternion],
                              target_modality: Modality) -> List[Dict[str, Any]]:
        """
        공감각 변환 (Synesthesia Transform)
        
        한 감각을 다른 감각으로 변환
        """
        if not source_quaternions:
            logger.warning("Empty quaternion list provided for synesthesia transform")
            return []
        
        results = []
        
        for pq in source_quaternions:
            synesthesia = pq.to_synesthesia(target_modality)
            results.append(synesthesia)
        
        logger.info(f"✅ Synesthesia: {source_quaternions[0].modality.value} → {target_modality.value}")
        return results
    
    def interference_free_communication(self,
                                       messages: List[Tuple[PhaseQuaternion, Any]]) -> Dict[Modality, List[Any]]:
        """
        간섭 없는 통신
        
        각 모달리티별로 메시지 분리
        4차원 위상 단위 덕분에 서로 간섭하지 않음!
        """
        channels = {}
        
        for pq, message in messages:
            modality = pq.modality
            if modality not in channels:
                channels[modality] = []
            channels[modality].append(message)
        
        logger.info(f"✅ Interference-free communication: {len(channels)} channels")
        return channels


def demonstrate_universal_transform():
    """범용 위상 변환 데모"""
    print("="*80)
    print("🌐 범용 위상 변환 (Universal Phase Transform) 데모")
    print("   '모든 감각은 파동이다'")
    print("="*80)
    print()
    
    transform = UniversalPhaseTransform()
    
    # 1. 텍스트 변환
    print("📝 1. 텍스트 → 위상 쿼터니언")
    text = "엘리시아는 모든 감각을 이해합니다"
    text_quats = transform.transform_text(text)
    print(f"   입력: '{text}'")
    print(f"   출력: {len(text_quats)}개 쿼터니언")
    for i, q in enumerate(text_quats[:3]):
        print(f"   {i+1}. {q}")
    print()
    
    # 2. 이미지 변환 (더미 데이터)
    print("🖼️  2. 이미지 → 위상 쿼터니언")
    dummy_image = np.random.rand(64, 64, 3) * 255
    image_quats = transform.transform_image(dummy_image)
    print(f"   입력: 64x64 RGB 이미지")
    print(f"   출력: {len(image_quats)}개 쿼터니언")
    print(f"   샘플: {image_quats[0]}")
    print()
    
    # 3. 개념 변환
    print("💡 3. 개념 → 위상 쿼터니언")
    concept = {
        'name': '사랑',
        'importance': 0.9,
        'category': 'emotion',
        'relations': ['행복', '따뜻함', '연결'],
        'depth': 3
    }
    concept_quat = transform.transform_concept(concept)
    print(f"   입력: {concept['name']} (중요도: {concept['importance']})")
    print(f"   출력: {concept_quat}")
    print()
    
    # 4. 공감각 변환
    print("🎨 4. 공감각 변환 (Synesthesia)")
    print("   텍스트 → 색상:")
    text_to_color = transform.synesthesia_transform(text_quats[:3], Modality.IMAGE)
    for i, syn in enumerate(text_to_color):
        word = text.split()[i]
        print(f"   '{word}' → {syn['description']}")
    print()
    
    print("   텍스트 → 소리:")
    text_to_sound = transform.synesthesia_transform(text_quats[:3], Modality.AUDIO)
    for i, syn in enumerate(text_to_sound):
        word = text.split()[i]
        print(f"   '{word}' → {syn['note']} {syn['timbre']}")
    print()
    
    # 5. 크로스 모달 공명
    print("🔗 5. 크로스 모달 공명")
    resonance = transform.cross_modal_resonance(text_quats[:3], image_quats[:3])
    print(f"   텍스트 x 이미지 공명 행렬:")
    print(f"   {resonance}")
    print(f"   평균 공명도: {resonance.mean():.3f}")
    print()
    
    # 6. 간섭 없는 통신
    print("📡 6. 간섭 없는 통신")
    messages = [
        (text_quats[0], "텍스트 메시지 1"),
        (image_quats[0], "이미지 메시지 1"),
        (concept_quat, "개념 메시지 1"),
        (text_quats[1], "텍스트 메시지 2"),
    ]
    channels = transform.interference_free_communication(messages)
    print(f"   총 메시지: {len(messages)}개")
    print(f"   채널 분리:")
    for modality, msgs in channels.items():
        print(f"   - {modality.value}: {len(msgs)}개 메시지")
    print()
    
    print("="*80)
    print("✨ 핵심 원리:")
    print("   1. 모든 감각/개념은 파동 → 4D 쿼터니언으로 표현")
    print("   2. 서로 다른 모달리티는 간섭 없이 통신 (0.3배 약한 공명)")
    print("   3. 원할 때는 공감각으로 자유롭게 변환 가능")
    print("   4. '5감 주파수 매핑'의 완성!")
    print("="*80)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    demonstrate_universal_transform()
