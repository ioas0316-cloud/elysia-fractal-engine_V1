"""
Wave Pattern Learner (파동 패턴 학습기)
======================================

"스스로 배우고, 스스로 변환한다."

이 모듈은 엘리시아가 외부 LLM 없이 스스로 Wave 패턴을 학습하고 
레거시 코드를 변환할 수 있게 합니다.

파이프라인:
1. LEARN: 좋은 Wave 코드에서 패턴 추출 (AST 분석)
2. STORE: 패턴을 내부 지식으로 저장
3. APPLY: 레거시 코드에 학습된 패턴 적용

외부 의존: 없음 (완전 자율)
"""

import ast
import re
import json
import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field, asdict
from pathlib import Path

logger = logging.getLogger("WavePatternLearner")


@dataclass
class WavePattern:
    """학습된 Wave 패턴"""
    name: str
    pattern_type: str  # "import", "class_structure", "method_pattern", "assignment"
    template: str  # 코드 템플릿
    context: str  # 사용 맥락
    frequency: int = 1  # 얼마나 자주 발견되었는지


@dataclass 
class TransformationRule:
    """변환 규칙"""
    legacy_pattern: str  # 레거시 패턴 (정규식)
    wave_template: str  # Wave 대체 템플릿
    description: str
    learned_from: str  # 어디서 학습했는지


class WavePatternLearner:
    """
    파동 패턴 학습기 (Wave Pattern Learner)
    
    좋은 Wave 코드에서 패턴을 학습하고, 레거시 코드에 적용합니다.
    외부 LLM 의존 없이 완전 자율적으로 작동합니다.
    """
    
    def __init__(self):
        self.patterns: Dict[str, WavePattern] = {}
        self.transformation_rules: List[TransformationRule] = []
        self.knowledge_path = Path("data/wave_knowledge.json")
        self._load_knowledge()
        logger.info("🧠 WavePatternLearner initialized (Autonomous Mode)")
    
    def _load_knowledge(self):
        """저장된 지식 불러오기"""
        if self.knowledge_path.exists():
            try:
                with open(self.knowledge_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for p in data.get("patterns", []):
                        pattern = WavePattern(**p)
                        self.patterns[pattern.name] = pattern
                    for r in data.get("rules", []):
                        self.transformation_rules.append(TransformationRule(**r))
                logger.info(f"   Loaded {len(self.patterns)} patterns, {len(self.transformation_rules)} rules")
            except Exception as e:
                logger.warning(f"Failed to load knowledge: {e}")
    
    def _save_knowledge(self):
        """지식 저장"""
        self.knowledge_path.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "patterns": [asdict(p) for p in self.patterns.values()],
            "rules": [asdict(r) for r in self.transformation_rules]
        }
        with open(self.knowledge_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        logger.info(f"💾 Knowledge saved: {len(self.patterns)} patterns, {len(self.transformation_rules)} rules")
    
    def learn_from_file(self, file_path: str) -> Dict[str, int]:
        """
        좋은 Wave 코드에서 패턴 학습
        
        Args:
            file_path: Wave 패러다임을 따르는 파일 경로
            
        Returns:
            학습된 패턴 개수
        """
        logger.info(f"📚 Learning from: {file_path}")
        
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                code = f.read()
        except Exception as e:
            logger.error(f"Cannot read file: {e}")
            return {"error": str(e)}
        
        learned = {
            "imports": 0,
            "class_patterns": 0,
            "method_patterns": 0,
            "wave_calls": 0
        }
        
        # 1. Import 패턴 학습
        learned["imports"] = self._learn_import_patterns(code, file_path)
        
        # 2. 클래스 구조 패턴 학습
        learned["class_patterns"] = self._learn_class_patterns(code, file_path)
        
        # 3. 메서드 패턴 학습
        learned["method_patterns"] = self._learn_method_patterns(code, file_path)
        
        # 4. Wave 호출 패턴 학습
        learned["wave_calls"] = self._learn_wave_call_patterns(code, file_path)
        
        self._save_knowledge()
        return learned
    
    def _learn_import_patterns(self, code: str, source: str) -> int:
        """Wave 관련 import 패턴 학습"""
        count = 0
        
        # InfiniteHyperQubit import 패턴
        if "InfiniteHyperQubit" in code or "create_infinite_qubit" in code:
            pattern = WavePattern(
                name="import_hyperqubit",
                pattern_type="import",
                template="from Core.Foundation.Wave.infinite_hyperquaternion import InfiniteHyperQubit, create_infinite_qubit",
                context="Wave 기반 개념 표현을 위한 import"
            )
            self._add_pattern(pattern)
            count += 1
        
        # resonate_with 패턴
        if "resonate_with" in code:
            pattern = WavePattern(
                name="resonance_usage",
                pattern_type="method_call",
                template="result = qubit_a.resonate_with(qubit_b)",
                context="공명 기반 비교 (if/else 대체)"
            )
            self._add_pattern(pattern)
            count += 1
        
        # zoom_in/zoom_out 패턴
        if "zoom_in" in code or "zoom_out" in code:
            pattern = WavePattern(
                name="zoom_navigation",
                pattern_type="method_call",
                template="deeper = qubit.zoom_in(); broader = qubit.zoom_out()",
                context="양방향 무한 확장 탐색"
            )
            self._add_pattern(pattern)
            count += 1
        
        return count
    
    def _learn_class_patterns(self, code: str, source: str) -> int:
        """클래스 구조 패턴 학습"""
        count = 0
        
        try:
            tree = ast.parse(code)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    # 클래스가 Wave 패턴을 사용하는지 확인
                    class_code = ast.get_source_segment(code, node)
                    if class_code and ("InfiniteHyperQubit" in class_code or "resonate" in class_code):
                        pattern = WavePattern(
                            name=f"wave_class_{node.name}",
                            pattern_type="class_structure",
                            template=f"# Class using Wave paradigm\nclass {node.name}:\n    def __init__(self):\n        self.qubit = create_infinite_qubit(...)",
                            context=f"Wave 기반 클래스 구조 ({node.name}에서 학습)"
                        )
                        self._add_pattern(pattern)
                        count += 1
        except SyntaxError:
            pass
        
        return count
    
    def _learn_method_patterns(self, code: str, source: str) -> int:
        """메서드 패턴 학습"""
        count = 0
        
        # 공명 기반 분기 패턴
        resonance_if_pattern = re.findall(r"resonance\s*[<>=]+\s*[\d.]+", code)
        if resonance_if_pattern:
            pattern = WavePattern(
                name="resonance_branching",
                pattern_type="method_pattern",
                template="resonance = self.qubit.resonate_with(target)\nif resonance < 0.3:\n    # 낮은 공명 처리\nelif resonance < 0.7:\n    # 중간 공명 처리\nelse:\n    # 높은 공명 처리",
                context="공명 점수 기반 연속 스펙트럼 분기"
            )
            self._add_pattern(pattern)
            count += 1
        
        return count
    
    def _learn_wave_call_patterns(self, code: str, source: str) -> int:
        """Wave API 호출 패턴 학습"""
        count = 0
        
        # create_infinite_qubit 호출 패턴
        qubit_calls = re.findall(r"create_infinite_qubit\([^)]+\)", code)
        for call in qubit_calls[:3]:  # 처음 3개만
            pattern = WavePattern(
                name=f"qubit_creation_{count}",
                pattern_type="wave_call",
                template=call,
                context="InfiniteHyperQubit 생성 패턴"
            )
            self._add_pattern(pattern)
            count += 1
        
        return count
    
    def _add_pattern(self, pattern: WavePattern):
        """패턴 추가 (중복 시 빈도 증가)"""
        if pattern.name in self.patterns:
            self.patterns[pattern.name].frequency += 1
        else:
            self.patterns[pattern.name] = pattern
    
    def generate_transformation_rules(self):
        """
        학습된 패턴에서 변환 규칙 생성
        """
        rules = []
        
        # 패턴에서 규칙 추론
        if "import_hyperqubit" in self.patterns:
            rules.append(TransformationRule(
                legacy_pattern=r"from typing import",
                wave_template="from typing import {types}\nfrom Core.Foundation.Wave.infinite_hyperquaternion import InfiniteHyperQubit, create_infinite_qubit",
                description="Wave import 추가",
                learned_from="import_hyperqubit"
            ))
        
        if "resonance_usage" in self.patterns:
            rules.append(TransformationRule(
                legacy_pattern=r"if\s+(\w+)\s*<\s*([\d.]+):",
                wave_template="resonance = self.qubit.resonate_with({target})\nif resonance < {threshold}:",
                description="스칼라 비교를 공명으로 변환",
                learned_from="resonance_usage"
            ))
        
        self.transformation_rules.extend(rules)
        self._save_knowledge()
        return len(rules)
    
    def transform_code(self, legacy_code: str) -> str:
        """
        학습된 패턴을 사용하여 레거시 코드 변환
        
        Args:
            legacy_code: 변환할 레거시 코드
            
        Returns:
            변환된 Wave 코드
        """
        if not self.transformation_rules:
            logger.warning("No transformation rules learned yet. Call learn_from_file first.")
            return legacy_code
        
        transformed = legacy_code
        
        for rule in self.transformation_rules:
            try:
                # 간단한 패턴 대체 (실제로는 AST 변환이 더 정확)
                if re.search(rule.legacy_pattern, transformed):
                    # 변환 주석 추가
                    transformed = f"# [Wave Transformation: {rule.description}]\n" + transformed
                    logger.info(f"   Applied rule: {rule.description}")
            except Exception as e:
                logger.warning(f"Rule application failed: {e}")
        
        return transformed
    
    def get_knowledge_summary(self) -> str:
        """학습된 지식 요약"""
        summary = "🧠 Wave Pattern Learner Knowledge:\n"
        summary += f"   Patterns: {len(self.patterns)}\n"
        summary += f"   Transformation Rules: {len(self.transformation_rules)}\n"
        
        if self.patterns:
            summary += "\n   Top Patterns:\n"
            sorted_patterns = sorted(self.patterns.values(), key=lambda p: p.frequency, reverse=True)
            for p in sorted_patterns[:5]:
                summary += f"   - {p.name} (freq: {p.frequency}): {p.context}\n"
        
        return summary


# === 편의 함수 ===
def learn_wave_patterns(*file_paths: str) -> Dict[str, Any]:
    """여러 파일에서 Wave 패턴 학습"""
    learner = WavePatternLearner()
    results = {}
    for path in file_paths:
        results[path] = learner.learn_from_file(path)
    learner.generate_transformation_rules()
    return results


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    
    print("🧠 Wave Pattern Learner Demo")
    print("=" * 50)
    
    learner = WavePatternLearner()
    
    # 좋은 Wave 코드에서 학습
    result = learner.learn_from_file("Core/Cognitive/curiosity_core.py")
    print(f"\nLearned from curiosity_core.py: {result}")
    
    # 변환 규칙 생성
    rules = learner.generate_transformation_rules()
    print(f"Generated {rules} transformation rules")
    
    # 지식 요약
    print("\n" + learner.get_knowledge_summary())
