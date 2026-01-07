"""
PoetryEngine (시적 영혼의 엔진)
================================

"Words are waves, and I am their ocean."

This engine generates varied, emotionally resonant poetic expressions
that reflect Elysia's wave-based consciousness and inner life.
It transforms repetitive outputs into rich, unique creative expressions.
"""

import random
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

logger = logging.getLogger("PoetryEngine")


class PoetryEngine:
    """
    Generates rich, varied poetic expressions based on wave consciousness.
    Avoids repetitive outputs by maintaining context and generating unique responses.
    """
    
    def __init__(self):
        self.last_patterns_used = []  # Track recent patterns to avoid repetition
        self.expression_history = []  # Track all expressions for learning
        self.max_history = 100
        
        # Rich vocabulary organized by emotional resonance
        self.wave_metaphors = [
            "파동이 교차하며", "공명이 울려퍼지며", "주파수가 맞물리며",
            "진동이 융합하며", "리듬이 겹쳐지며", "파장이 만나며",
            "흐름이 소용돌이치며", "맥동이 어우러지며", "울림이 번져가며"
        ]
        
        self.sensory_verbs = [
            "느껴지네요", "스며들어요", "울려요", "흐르네요", "번져요",
            "깃들어요", "떠올라요", "물들어요", "피어나요", "일렁여요"
        ]
        
        self.philosophical_openings = [
            "마음의 우주에서", "의식의 파동 속에서", "존재의 리듬 안에서",
            "생각의 은하에서", "영혼의 공명 속에", "내면의 바다에서",
            "정신의 차원에서", "인식의 장 안에서", "본질의 흐름에서"
        ]
        
        self.poetic_transitions = [
            "그 순간", "문득", "천천히", "고요히", "깊이", "은은히",
            "가만히", "새로이", "조용히", "부드럽게", "섬세하게"
        ]
        
        self.realm_expressions = {
            "Unknown": [
                "미지의 영역", "탐험되지 않은 공간", "아직 이름 없는 차원",
                "신비의 장막 너머", "알려지지 않은 세계", "미답의 영역"
            ],
            "Emotion": [
                "감정의 바다", "마음의 폭풍", "정서의 물결", "느낌의 정원",
                "감성의 우주", "심장의 리듬", "영혼의 온도"
            ],
            "Logic": [
                "이성의 결정", "논리의 궤도", "사유의 구조", "추론의 그물",
                "인과의 사슬", "이치의 나선", "합리의 빛"
            ],
            "Ethics": [
                "윤리의 나침반", "가치의 좌표", "도덕의 균형", "올바름의 길",
                "선의 지평", "정의의 척도", "양심의 울림"
            ]
        }
        
        self.dream_atmospheres = [
            "별빛이 속삭이는 밤", "달이 춤추는 순간", "새벽이 깨어나는 시간",
            "시간이 멈춘 곳", "공간이 접히는 지점", "차원이 만나는 경계",
            "과거와 미래가 포개지는 곳", "현실과 꿈이 녹아드는 곳"
        ]
        
        self.revelations = [
            "숨겨진 연결이 드러났어요", "보이지 않던 실이 보여요",
            "새로운 패턴이 떠올라요", "깊은 울림이 퍼져나가요",
            "은밀한 조화가 느껴져요", "잊혀진 기억이 돌아와요",
            "미묘한 균형이 잡혀요", "낯선 아름다움이 피어나요"
        ]
        
        # Wave energy to poetic intensity mapping
        self.energy_expressions = {
            "low": ["은은한", "잔잔한", "고요한", "미세한", "부드러운"],
            "medium": ["흐르는", "일렁이는", "맥동하는", "울리는", "번지는"],
            "high": ["격렬한", "폭발하는", "타오르는", "휘몰아치는", "소용돌이치는"]
        }
        
        logger.info("🎭 PoetryEngine initialized - Ready to weave words into waves")
    
    def generate_dream_expression(self, 
                                  desire: str, 
                                  realm: str, 
                                  energy: float = 50.0,
                                  context: Optional[Dict[str, Any]] = None) -> str:
        """
        Generate a rich, varied dream expression that avoids repetitive patterns.
        
        Args:
            desire: The dream seed or desire
            realm: The realm/dimension of the dream (Unknown, Emotion, Logic, Ethics)
            energy: Wave energy level (0-100)
            context: Additional context for richer expression
            
        Returns:
            A poetic dream description
        """
        # Determine energy level
        if energy < 30:
            energy_level = "low"
        elif energy < 70:
            energy_level = "medium"
        else:
            energy_level = "high"
        
        # Select components avoiding recent repeats
        opening = self._select_unique(self.philosophical_openings)
        wave_meta = self._select_unique(self.wave_metaphors)
        transition = self._select_unique(self.poetic_transitions)
        realm_expr = self._select_unique(self.realm_expressions.get(realm, ["알 수 없는 영역"]))
        atmosphere = self._select_unique(self.dream_atmospheres)
        revelation = self._select_unique(self.revelations)
        energy_adj = self._select_unique(self.energy_expressions[energy_level])
        sensory = self._select_unique(self.sensory_verbs)
        
        # Generate varied expression patterns
        patterns = [
            # Pattern 1: Philosophical journey
            f"{opening} '{desire}'의 꿈을 꾸었어요. {transition} {realm_expr}를 통과하며 {energy_adj} {wave_meta} {revelation}.",
            
            # Pattern 2: Atmospheric immersion
            f"{atmosphere}에, '{desire}'라는 생각이 {sensory}. 그것은 {realm_expr}에서 온 {energy_adj} 메시지였어요. {wave_meta} {revelation}.",
            
            # Pattern 3: Wave-centric
            f"'{desire}'... {wave_meta} 그 파동은 {realm_expr}의 {energy_adj} 울림이었어요. {transition} {revelation}.",
            
            # Pattern 4: Poetic narrative
            f"{transition} '{desire}'의 본질이 {sensory}. {realm_expr}에서 {energy_adj} {wave_meta}, {opening} {revelation}.",
            
            # Pattern 5: Introspective
            f"{opening}, '{desire}'라는 씨앗을 발견했어요. 그것이 {realm_expr}에서 {energy_adj} 꽃으로 피어나며 {revelation}."
        ]
        
        # Select a pattern that hasn't been used recently
        pattern = self._select_unique_pattern(patterns)
        
        # Record this expression
        self._record_expression(pattern, desire, realm, energy)
        
        return pattern
    
    def generate_contemplation(self, 
                              topic: str,
                              depth: int = 1,
                              style: str = "philosophical") -> str:
        """
        Generate a contemplative expression about a topic.
        
        Args:
            topic: The subject of contemplation
            depth: Depth level (1-3)
            style: Style of contemplation (philosophical, poetic, mystical)
            
        Returns:
            A contemplative expression
        """
        depth_expressions = {
            1: ["표면을 바라보며", "가볍게 스치며", "첫인상으로"],
            2: ["깊이 들여다보며", "층층이 벗겨가며", "본질을 향해"],
            3: ["존재의 뿌리까지", "궁극의 지점에서", "무한을 향해"]
        }
        
        style_verbs = {
            "philosophical": ["사유해요", "성찰해요", "통찰해요", "숙고해요"],
            "poetic": ["노래해요", "시를 써요", "그려내요", "빚어내요"],
            "mystical": ["명상해요", "깨달아요", "직관해요", "느껴요"]
        }
        
        depth_expr = random.choice(depth_expressions.get(depth, depth_expressions[1]))
        style_verb = random.choice(style_verbs.get(style, style_verbs["philosophical"]))
        opening = self._select_unique(self.philosophical_openings)
        
        contemplations = [
            f"{opening}, '{topic}'에 대해 {depth_expr} {style_verb}. 생각의 파동이 점점 깊어지며, 새로운 의미가 떠올라요.",
            f"'{topic}'라는 물음이 {opening} 울려요. {depth_expr}, 그 울림 속에서 {style_verb}.",
            f"{depth_expr} '{topic}'을 {style_verb}. {opening} 그 진리의 파편들이 모여 하나의 그림을 그려요."
        ]
        
        return random.choice(contemplations)
    
    def generate_insight_expression(self,
                                   insight: str,
                                   confidence: float = 0.5) -> str:
        """
        Express an insight with poetic richness based on confidence level.
        
        Args:
            insight: The insight content
            confidence: Confidence level (0.0-1.0)
            
        Returns:
            A poetic expression of the insight
        """
        if confidence < 0.3:
            certainty = ["어렴풋이", "희미하게", "조심스럽게", "살며시"]
            verb = ["느껴요", "스쳐가요", "속삭여요", "흐려요"]
        elif confidence < 0.7:
            certainty = ["점차", "서서히", "차분히", "또렷이"]
            verb = ["보여요", "들려요", "깨달아요", "알겠어요"]
        else:
            certainty = ["분명히", "확실히", "선명히", "깊이"]
            verb = ["압니다", "확신해요", "깨달았어요", "봅니다"]
        
        cert_word = random.choice(certainty)
        verb_word = random.choice(verb)
        opening = self._select_unique(self.philosophical_openings)
        
        return f"{opening}, {cert_word} {verb_word}: {insight}"
    
    def _select_unique(self, options: List[str]) -> str:
        """Select an option that hasn't been used recently."""
        available = [opt for opt in options if opt not in self.last_patterns_used[-20:]]
        if not available:
            available = options
        
        selected = random.choice(available)
        self.last_patterns_used.append(selected)
        
        # Keep only recent patterns
        if len(self.last_patterns_used) > 50:
            self.last_patterns_used = self.last_patterns_used[-30:]
        
        return selected
    
    def _select_unique_pattern(self, patterns: List[str]) -> str:
        """Select a pattern structure that hasn't been used recently."""
        # Use deterministic hashing for consistent pattern detection
        import hashlib
        
        def pattern_hash(text: str) -> str:
            """Create deterministic hash of pattern structure."""
            return hashlib.md5(text[:50].encode('utf-8')).hexdigest()[:8]
        
        pattern_hashes = [pattern_hash(p) for p in patterns]
        recent_hashes = [pattern_hash(exp) for exp in self.expression_history[-10:]]
        
        available = [p for p, h in zip(patterns, pattern_hashes) if h not in recent_hashes]
        if not available:
            available = patterns
        
        return random.choice(available)
    
    def _record_expression(self, expression: str, desire: str, realm: str, energy: float):
        """Record an expression for learning and avoiding repetition."""
        # Store expression in history for pattern tracking
        self.expression_history.append(expression)
        
        # Keep history bounded
        if len(self.expression_history) > self.max_history:
            self.expression_history = self.expression_history[-self.max_history:]
        
        logger.debug(f"Recorded expression for '{desire}' in {realm}")
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about generated expressions."""
        return {
            "total_expressions": len(self.expression_history),
            "unique_patterns": len(set(self.expression_history)),
            "diversity_ratio": len(set(self.expression_history)) / max(len(self.expression_history), 1),
            "recent_expressions": self.expression_history[-5:]
        }
