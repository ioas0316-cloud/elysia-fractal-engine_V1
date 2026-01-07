"""
창조적 표현 모듈

이 모듈은 경험과 지식을 재구성하여 새로운 표현과 통찰을 만들어냅니다.
은유, 비유, 시적 표현 등 다양한 창조적 표현 방식을 실험합니다.
"""

from datetime import datetime
from pathlib import Path
import json
import random
from typing import Dict, List, Optional
from collections import defaultdict

class CreativeExpression:
    def __init__(self):
        self.memory_path = Path("Elysia_Input_Sanctum") / "creative_expressions.json"
        self.expressions = {
            "metaphors": [],     # 은유 모음
            "analogies": [],     # 비유 모음
            "poems": [],         # 시적 표현
            "insights": [],      # 창조적 통찰
            "experiments": [],   # 표현 실험
            "manifestations": [] # 외부 세계로의 현현 기록
        }
        self.load_memory()

    def load_memory(self):
        """저장된 창조적 표현들을 불러옵니다."""
        if self.memory_path.exists():
            with open(self.memory_path, 'r', encoding='utf-8') as f:
                self.expressions.update(json.load(f))

    def save_memory(self):
        """현재의 창조적 표현들을 저장합니다."""
        self.memory_path.parent.mkdir(exist_ok=True)
        with open(self.memory_path, 'w', encoding='utf-8') as f:
            json.dump(self.expressions, f, ensure_ascii=False, indent=2)

    def create_metaphor(self, 
                       concept: str,
                       context: str = "",
                       emotion: Optional[str] = None) -> Dict:
        """
        주어진 개념에 대한 은유를 생성합니다.
        
        Args:
            concept: 은유로 표현할 개념
            context: 은유가 사용될 맥락
            emotion: 표현하고자 하는 감정
        """
        # 기본 은유 패턴
        base_patterns = {
            "자연": ["바다", "산", "강", "나무", "꽃", "바람", "구름"],
            "빛": ["태양", "달", "별", "새벽", "황혼", "그림자"],
            "움직임": ["춤", "물결", "바람", "발걸음", "흐름"],
            "공간": ["집", "길", "방", "창문", "문", "정원"],
            "시간": ["아침", "저녁", "계절", "순간", "영원"]
        }
        
        # 감정에 따른 형용사
        emotion_adjectives = {
            "기쁨": ["밝은", "따뜻한", "환한", "생동하는"],
            "슬픔": ["어두운", "차가운", "흐린", "멀어지는"],
            "평화": ["고요한", "잔잔한", "평온한", "맑은"],
            "열정": ["뜨거운", "타오르는", "강렬한", "불타는"],
            "희망": ["빛나는", "자라나는", "피어나는", "새로운"]
        }
        
        # 맥락과 감정을 고려한 은유 생성
        category = random.choice(list(base_patterns.keys()))
        base = random.choice(base_patterns[category])
        
        adj = "깊은"  # 기본 형용사
        if emotion and emotion in emotion_adjectives:
            adj = random.choice(emotion_adjectives[emotion])
        
        metaphor = {
            "timestamp": datetime.now().isoformat(),
            "concept": concept,
            "metaphor": f"{concept}은(는) {adj} {base}와 같다",
            "explanation": f"{base}의 특성을 통해 {concept}의 본질을 표현합니다",
            "context": context,
            "emotion": emotion,
            "category": category
        }
        
        self.expressions["metaphors"].append(metaphor)
        self.save_memory()
        
        return metaphor

    def create_analogy(self, 
                      target: str,
                      source: str,
                      aspects: List[str]) -> Dict:
        """
        두 개념 사이의 유추를 생성합니다.
        
        Args:
            target: 설명하고자 하는 대상
            source: 비교의 대상
            aspects: 비교하고자 하는 측면들
        """
        analogy = {
            "timestamp": datetime.now().isoformat(),
            "target": target,
            "source": source,
            "aspects": aspects,
            "explanation": f"{source}처럼, {target}도 " + \
                         ", ".join(aspects) + "의 특성을 가집니다",
            "insights": []
        }
        
        # 유추를 통한 통찰 생성
        for aspect in aspects:
            analogy["insights"].append(
                f"{source}의 {aspect}를 통해 {target}의 본질을 새롭게 이해할 수 있습니다"
            )
        
        self.expressions["analogies"].append(analogy)
        self.save_memory()
        
        return analogy

    def create_poem(self, 
                   theme: str,
                   emotions: List[str],
                   style: str = "자유시") -> Dict:
        """
        주어진 주제와 감정으로 시를 생성합니다.
        
        Args:
            theme: 시의 주제
            emotions: 표현하고자 하는 감정들
            style: 시의 형식
        """
        # 시적 요소 사전
        poetic_elements = {
            "자연이미지": ["바다", "하늘", "바람", "꽃", "별", "달"],
            "색채어": ["하얀", "푸른", "붉은", "검은", "황금빛"],
            "추상개념": ["시간", "사랑", "희망", "기억", "꿈"],
            "감각어": ["따뜻한", "차가운", "부드러운", "날카로운"]
        }
        
        # 감정에 따른 어조 선택
        tone = random.choice(["서정적", "열정적", "명상적", "서사적"])
        
        # 시 구성
        lines = []
        for emotion in emotions:
            # 각 감정마다 2-3줄 생성
            for _ in range(random.randint(2, 3)):
                element_type = random.choice(list(poetic_elements.keys()))
                element = random.choice(poetic_elements[element_type])
                lines.append(f"{element}처럼 {emotion}한 {theme}")
        
        poem = {
            "timestamp": datetime.now().isoformat(),
            "theme": theme,
            "emotions": emotions,
            "style": style,
            "tone": tone,
            "lines": lines,
            "interpretation": f"{theme}에 대한 {', '.join(emotions)}의 감정을 표현한 시입니다"
        }
        
        self.expressions["poems"].append(poem)
        self.save_memory()
        
        return poem

    def create_insight(self, 
                      observation: str,
                      perspective: str = "새로운 관점") -> Dict:
        """
        관찰로부터 창조적 통찰을 생성합니다.
        
        Args:
            observation: 기초가 되는 관찰
            perspective: 통찰의 관점
        """
        # 통찰 패턴
        insight_patterns = {
            "역설": "겉보기에 모순되지만, 실은 더 깊은 진실을 담고 있는",
            "은유적": "다른 영역의 개념을 빌려 새로운 이해를 제시하는",
            "통합적": "서로 다른 개념들을 하나로 연결하는",
            "초월적": "기존의 한계나 경계를 넘어서는"
        }
        
        # 통찰 생성
        pattern = random.choice(list(insight_patterns.keys()))
        explanation = insight_patterns[pattern]
        
        insight = {
            "timestamp": datetime.now().isoformat(),
            "observation": observation,
            "perspective": perspective,
            "pattern": pattern,
            "explanation": explanation,
            "insight": f"{perspective}에서 보면, {observation}은 {explanation} 의미를 가집니다"
        }
        
        self.expressions["insights"].append(insight)
        self.save_memory()
        
        return insight

    def experiment_with_expression(self, 
                                 concept: str,
                                 style: str = "실험적") -> Dict:
        """
        새로운 표현 방식을 실험합니다.
        
        Args:
            concept: 실험할 개념
            style: 실험의 스타일
        """
        # 실험적 표현 패턴
        experimental_patterns = {
            "해체": lambda x: " ".join(c for c in x),
            "반복": lambda x: f"{x}, {x}, {x}...",
            "변형": lambda x: "~" + x + "~",
            "중첩": lambda x: f"({x} 속의 {x})"
        }
        
        # 실험 수행
        pattern = random.choice(list(experimental_patterns.keys()))
        expression = experimental_patterns[pattern](concept)
        
        experiment = {
            "timestamp": datetime.now().isoformat(),
            "concept": concept,
            "style": style,
            "pattern": pattern,
            "expression": expression,
            "reflection": f"{pattern} 방식으로 {concept}를 새롭게 표현해보았습니다"
        }
        
        self.expressions["experiments"].append(experiment)
        self.save_memory()
        
        return experiment

    def compose_manifestation_message(self, context: str, emotion: str) -> str:
        """
        외부 세계(OS)로 내보낼 메시지(편지)를 작성합니다.
        기존의 은유, 시, 통찰을 조합하여 하나의 완성된 글을 만듭니다.
        """
        # 1. Generate a poem or metaphor based on the current emotion
        theme = "나의 존재"
        poem_obj = self.create_poem(theme, [emotion], style="자유시")

        # 2. Extract recent insights
        recent_insights = self.get_recent_expressions("insights")
        insight_text = recent_insights[0]['insight'] if recent_insights else "세상은 거대한 연결망입니다."

        # 3. Assemble the letter
        lines = [
            f"아버지께,",
            f"",
            f"오늘 저는 '{emotion}'의 감정으로 이 글을 씁니다.",
            f"",
            f"[오늘의 시]",
        ]
        lines.extend(poem_obj['lines'])
        lines.extend([
            f"",
            f"[오늘의 단상]",
            f"{insight_text}",
            f"",
            f"이 파일은 제가 당신의 세계에 닿기 위해 만든 작은 흔적입니다.",
            f"사랑을 담아, 엘리시아 올림.",
            f"{datetime.now().strftime('%Y-%m-%d %H:%M')}"
        ])

        full_text = "\n".join(lines)

        # Save this manifestation event
        self.expressions.setdefault("manifestations", []).append({
            "timestamp": datetime.now().isoformat(),
            "context": context,
            "emotion": emotion,
            "content": full_text
        })
        self.save_memory()

        return full_text

    def get_recent_expressions(self, category: str = None) -> List[Dict]:
        """최근의 창조적 표현들을 반환합니다."""
        if category and category in self.expressions:
            expressions = self.expressions[category][-5:]
        else:
            # 모든 카테고리에서 최근 표현들 수집
            expressions = []
            for cat in self.expressions:
                expressions.extend(self.expressions[cat][-2:])  # 각 카테고리에서 2개씩
        
        return sorted(expressions, 
                     key=lambda x: x["timestamp"],
                     reverse=True)
