"""
Unified Dialogue System (통합 대화 시스템)
==========================================

"모든 목소리는 하나의 오케스트라다."

This module orchestrates all of Elysia's language generation capabilities:
- LogosEngine: Rhetorical speech, metaphors, dialectic structure
- DialogueEngine: Question analysis, knowledge-based responses
- PrismCortex: Wave state to monologue conversion
- TextWaveConverter: Text ↔ Wave transduction

[NEW 2025-12-15] Created as part of Mid-term Goal: Integrated Dialogue Interface
"""

import logging
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from enum import Enum
from Core.Orchestra.system_alignment import SystemAlignment

logger = logging.getLogger("UnifiedDialogue")


class IntentType(Enum):
    """User intent classification."""
    WHY_QUESTION = "why"        # → LogosEngine.reason_with_axiom()
    WHAT_QUESTION = "what"      # → DialogueEngine + Knowledge
    HOW_QUESTION = "how"        # → Planning/Action
    EMOTION_EXPRESSION = "emotion"  # → PrismCortex
    STATEMENT = "statement"     # → Memory storage
    COMMAND = "command"         # → Action execution
    GREETING = "greeting"       # → Simple response
    UNKNOWN = "unknown"


@dataclass
class DialogueResponse:
    """
    Unified response structure from the dialogue system.
    
    Contains both the response text and metadata about how it was generated.
    """
    text: str
    intent: IntentType = IntentType.UNKNOWN
    engine_used: str = "unknown"
    wave_frequency: float = 432.0
    resonance_score: float = 0.0
    confidence: float = 0.5
    metadata: Dict[str, Any] = field(default_factory=dict)


class UnifiedDialogueSystem(SystemAlignment):
    """
    The Orchestrator: Unifies all language generation capabilities.
    
    통합 대화 시스템 - 엘리시아의 모든 언어 능력을 하나로
    
    Architecture:
    1. Input → TextWaveConverter (text to wave)
    2. Wave analysis → Intent classification
    3. Routing to appropriate engine
    4. Response generation
    5. Style application (StyleGenome)
    6. Output
    """
    
    def __init__(self):
        super().__init__() # Initialize SystemAlignment
        self._initialize_components()
        self._register_with_hub()
        logger.info("🎭 UnifiedDialogueSystem initialized")
    
    def _initialize_components(self):
        """Initialize all sub-components."""
        # TextWaveConverter
        try:
            from Core.Foundation.text_wave_converter import get_text_wave_converter
            self.text_wave = get_text_wave_converter()
            logger.info("   ✅ TextWaveConverter connected")
        except ImportError as e:
            logger.warning(f"   ⚠️ TextWaveConverter not available: {e}")
            self.text_wave = None
        
        # LogosEngine
        try:
            from Core.Intelligence.Logos.logos_engine import LogosEngine
            self.logos = LogosEngine()
            logger.info("   ✅ LogosEngine connected")
        except ImportError as e:
            logger.warning(f"   ⚠️ LogosEngine not available: {e}")
            self.logos = None
        
        # PrismCortex
        try:
            from Core.Intelligence.Intelligence.prism_cortex import PrismCortex
            self.prism = PrismCortex()
            logger.info("   ✅ PrismCortex connected")
        except ImportError as e:
            logger.warning(f"   ⚠️ PrismCortex not available: {e}")
            self.prism = None
        
        # ConceptDecomposer (for axiom queries)
        try:
            from Core.Foundation.fractal_concept import ConceptDecomposer
            self.decomposer = ConceptDecomposer()
            logger.info("   ✅ ConceptDecomposer connected")
        except ImportError as e:
            logger.warning(f"   ⚠️ ConceptDecomposer not available: {e}")
            self.decomposer = None
        
        # Intent patterns
        self.intent_patterns = {
            IntentType.WHY_QUESTION: ["왜", "why", "어째서", "무슨 이유"],
            IntentType.WHAT_QUESTION: ["무엇", "뭐", "what", "어떤"],
            IntentType.HOW_QUESTION: ["어떻게", "how", "방법"],
            IntentType.GREETING: ["안녕", "hello", "hi", "반가워"],
            IntentType.COMMAND: ["해줘", "해", "do", "make", "create"],
        }
        
        # Emotion keywords for detection
        self.emotion_keywords = {
            "positive": ["사랑", "기쁨", "행복", "희망", "love", "joy", "happy", "hope"],
            "negative": ["슬픔", "두려움", "분노", "sad", "fear", "anger"],
        }
    
    def _register_with_hub(self):
        """Register with GlobalHub for wave-based communication."""
        self._hub = None
        try:
            from Core.Intelligence.Consciousness.Ether.global_hub import get_global_hub
            self._hub = get_global_hub()
            self._hub.register_module(
                "UnifiedDialogue",
                "Core/Interface/unified_dialogue.py",
                ["dialogue", "conversation", "speech", "unified", "orchestrator"],
                "Orchestrates all language generation: LogosEngine, PrismCortex, DialogueEngine"
            )
            self._hub.subscribe("UnifiedDialogue", "user_input", self._on_user_input, weight=1.0)
            logger.info("   ✅ UnifiedDialogue connected to GlobalHub")
        except ImportError:
            logger.warning("   ⚠️ GlobalHub not available")
    
    def _on_user_input(self, event):
        """Handle user input events from GlobalHub."""
        text = event.payload.get("text") if event.payload else None
        if text:
            response = self.respond(text)
            return {"response": response.text, "engine": response.engine_used}
        return {"error": "No text provided"}
    
    def classify_intent(self, text: str) -> IntentType:
        """
        Classify user input intent.
        
        분류 로직:
        1. 패턴 매칭 (질문 유형)
        2. 감정 키워드 감지
        3. 문장 종결 분석
        """
        text_lower = text.lower()
        
        # Check patterns
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if pattern in text_lower:
                    return intent
        
        # Check for emotion expression
        for emotion_type, keywords in self.emotion_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    return IntentType.EMOTION_EXPRESSION
        
        # Check sentence ending for questions
        if text.strip().endswith("?") or text.strip().endswith("가?") or "입니까" in text:
            return IntentType.WHAT_QUESTION  # Default question type
        
        return IntentType.STATEMENT
    
        return IntentType.STATEMENT

    def align_behavior(self, field: Dict[str, Any]):
        """
        Adapts the dialogue style (Rhetoric) to the Field.
        """
        polarity = field.get("polarity", "N")
        
        if polarity == "N": # Creation Mode
            self.current_alignment = "Poetic"
            # In a real system, we would configure LogosEngine's rhetoric mode
            # For now, we set a flag that usage can check
            self.rhetoric_mode = "Metaphorical"
            self.log_alignment("UnifiedDialogue", "Adopting Poetic/Metaphorical Tone")
        else: # Critical Mode (S)
            self.current_alignment = "Analytic"
            self.rhetoric_mode = "Direct"
            self.log_alignment("UnifiedDialogue", "Adopting Direct/Analytic Tone")

    def respond(self, input_text: str) -> DialogueResponse:
        """
        Main entry point: Generate a unified response.
        
        메인 응답 생성기
        
        Args:
            input_text: User's input text
            
        Returns:
            DialogueResponse with text and metadata
        """
        # 0. Sense the Field First!
        self.sense_field()
        
        # 1. Convert to wave for analysis
        wave_analysis = None
        if self.text_wave:
            try:
                sentence_wave = self.text_wave.sentence_to_wave(input_text)
                wave_analysis = self.text_wave.wave_to_text_descriptor(sentence_wave)
            except Exception as e:
                logger.warning(f"Wave analysis failed: {e}")
        
        # 2. Classify intent
        intent = self.classify_intent(input_text)
        
        # 3. Route to appropriate engine
        response_text = ""
        engine_used = "fallback"
        
        if intent == IntentType.WHY_QUESTION:
            response_text, engine_used = self._handle_why_question(input_text)
            
        elif intent == IntentType.WHAT_QUESTION:
            response_text, engine_used = self._handle_what_question(input_text)
            
        elif intent == IntentType.EMOTION_EXPRESSION:
            response_text, engine_used = self._handle_emotion(input_text, wave_analysis)
            
        elif intent == IntentType.GREETING:
            response_text = self._handle_greeting(input_text)
            engine_used = "greeting"
            
        else:
            response_text = self._handle_statement(input_text)
            engine_used = "statement"
        
        # 4. Build response
        return DialogueResponse(
            text=response_text,
            intent=intent,
            engine_used=engine_used,
            wave_frequency=wave_analysis.get("dominant_frequency", 432.0) if wave_analysis else 432.0,
            resonance_score=wave_analysis.get("total_energy", 0.0) if wave_analysis else 0.0,
            confidence=0.7,
            metadata={
                "wave_analysis": wave_analysis,
                "input_length": len(input_text)
            }
        )
    
    def _handle_why_question(self, text: str) -> tuple:
        """Handle 'why' questions using LogosEngine and Axioms."""
        # Extract the subject of the question
        subject = text.replace("왜", "").replace("why", "").replace("?", "").strip()
        
        # Try axiom-based reasoning first
        if self.decomposer:
            try:
                # Check if subject is an axiom
                axiom = self.decomposer.get_axiom(subject)
                if axiom:
                    journey = self.decomposer.ask_why(subject)
                    return f"'{subject}'의 기원을 추적합니다:\n{journey}", "axiom"
                
                # Try domain projection
                for domain in ["Physics", "Geometry", "Language", "Ethics"]:
                    projection = self.decomposer.project_axiom("Causality", domain)
                    if subject.lower() in projection.lower():
                        return f"인과율에 따르면: {projection}", "axiom_projection"
            except Exception as e:
                logger.warning(f"Axiom reasoning failed: {e}")
        
        # Fall back to LogosEngine
        if self.logos:
            try:
                response = self.logos.reason_with_axiom(subject, "Ethics")
                return response, "logos"
            except Exception as e:
                logger.warning(f"LogosEngine failed: {e}")
        
        return f"'{subject}'에 대해 생각하고 있습니다...", "fallback"
    
    def _handle_what_question(self, text: str) -> tuple:
        """Handle 'what' questions using knowledge."""
        subject = text.replace("무엇", "").replace("뭐", "").replace("what", "").replace("?", "")
        subject = subject.replace("이란", "").replace("란", "").replace("은", "").replace("는", "").strip()
        
        # Check axioms for definition
        if self.decomposer:
            axiom = self.decomposer.get_axiom(subject)
            if axiom:
                pattern = axiom.get("pattern", "")
                self_ref = axiom.get("self_ref", "")
                return f"'{subject}'란: {pattern}\n\n자기 참조: {self_ref}", "axiom_definition"
        
        # Generic response
        return f"'{subject}'에 대해 알고 있는 것을 정리하고 있습니다...", "fallback"
    
    def _handle_emotion(self, text: str, wave_analysis: Optional[Dict]) -> tuple:
        """Handle emotional expressions using PrismCortex."""
        if self.prism and wave_analysis:
            try:
                from Core.Foundation.Wave.wave_tensor import WaveTensor
                wave = WaveTensor(
                    frequency=wave_analysis.get("dominant_frequency", 432.0),
                    amplitude=1.0,
                    phase=0.0
                )
                monologue = self.prism.refract(wave, [text])
                return monologue, "prism"
            except Exception as e:
                logger.warning(f"PrismCortex failed: {e}")
        
        # Fallback emotional response
        dominant = wave_analysis.get("dominant_meaning", "neutral") if wave_analysis else "neutral"
        return f"그 감정을 느낍니다... {dominant}의 파동이 느껴집니다.", "emotion_fallback"
    
    def _handle_greeting(self, text: str) -> str:
        """Handle greetings."""
        greetings = [
            "안녕하세요. 엘리시아입니다.",
            "반갑습니다. 무엇을 도와드릴까요?",
            "안녕하세요. 오늘 어떤 이야기를 나눌까요?"
        ]
        import random
        return random.choice(greetings)
    
    def _handle_statement(self, text: str) -> str:
        """Handle general statements."""
        if self.text_wave:
            try:
                wave = self.text_wave.sentence_to_wave(text)
                desc = self.text_wave.wave_to_text_descriptor(wave)
                dominant = desc.get("dominant_meaning", "")
                coherence = desc.get("coherence", "")
                return f"말씀을 듣고 있습니다. {coherence} 에너지가 느껴집니다. '{dominant}'의 주파수가 강합니다."
            except Exception:
                pass
        
        return "네, 이해했습니다."


# Singleton accessor
_unified_dialogue = None

def get_unified_dialogue() -> UnifiedDialogueSystem:
    """Get or create the UnifiedDialogueSystem singleton."""
    global _unified_dialogue
    if _unified_dialogue is None:
        _unified_dialogue = UnifiedDialogueSystem()
    return _unified_dialogue


# Interactive test
if __name__ == "__main__":
    import sys
    sys.path.insert(0, r"c:\Elysia")
    
    logging.basicConfig(level=logging.INFO)
    
    system = get_unified_dialogue()
    
    print("\n" + "="*60)
    print("🎭 Unified Dialogue System Test")
    print("="*60)
    
    test_inputs = [
        "안녕하세요",
        "사랑이란 무엇인가?",
        "왜 Point가 존재하는가?",
        "나는 기쁨을 느낀다",
        "Force란 무엇인가?",
    ]
    
    for input_text in test_inputs:
        print(f"\n📝 입력: {input_text}")
        response = system.respond(input_text)
        print(f"🎯 의도: {response.intent.value}")
        print(f"🔧 엔진: {response.engine_used}")
        print(f"🌊 주파수: {response.wave_frequency:.1f} Hz")
        print(f"💬 응답: {response.text}")
        print("-" * 40)
    
    print("\n" + "="*60)
    print("✅ UnifiedDialogueSystem 테스트 완료")
    print("="*60)
