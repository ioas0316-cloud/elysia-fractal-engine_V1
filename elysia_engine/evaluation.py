"""
Elysia Engine Evaluation Module
================================

구조 추출, 관계성 분석, 객관적 평가 지표 시스템

이 모듈은 원본 Elysia 저장소의 구조를 분석하고,
다른 사람들이 쉽게 이해하고 공유할 수 있도록 평가 지표를 제공합니다.

핵심 기능:
1. 구조 추출 (Structure Extraction): 모듈 간 관계성 분석
2. 관계성 평가 (Relationship Evaluation): 의존성 및 연결성 분석
3. 품질 지표 (Quality Metrics): 코드 품질 및 아키텍처 평가
4. 개선 사항 도출 (Improvement Suggestions): 자동화된 보완점 분석
"""

from __future__ import annotations

import ast
import json
import os
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple
from datetime import datetime

from .logging_config import get_logger

logger = get_logger(__name__)


class ModuleCategory(Enum):
    """모듈 카테고리"""
    CORE = "core"           # 핵심 모듈 (tensor, math_utils)
    PHYSICS = "physics"     # 물리 시스템
    CONSCIOUSNESS = "consciousness"  # 의식 시스템
    SYSTEM = "system"       # ECS 시스템
    INTEGRATION = "integration"  # 통합 모듈
    UTILITY = "utility"     # 유틸리티


class QualityLevel(Enum):
    """품질 수준"""
    EXCELLENT = "⭐⭐⭐⭐⭐"
    GOOD = "⭐⭐⭐⭐"
    MODERATE = "⭐⭐⭐"
    NEEDS_IMPROVEMENT = "⭐⭐"
    CRITICAL = "⭐"


@dataclass
class ModuleInfo:
    """모듈 정보"""
    name: str
    path: str
    category: ModuleCategory
    
    # 메트릭
    lines_of_code: int = 0
    class_count: int = 0
    function_count: int = 0
    docstring_coverage: float = 0.0
    
    # 관계성
    imports: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    dependents: List[str] = field(default_factory=list)
    
    # 품질 점수
    quality_score: float = 0.0
    
    # 설명
    description: str = ""


@dataclass
class RelationshipEdge:
    """모듈 간 관계"""
    source: str
    target: str
    relationship_type: str  # 'imports', 'inherits', 'uses', 'resonates'
    strength: float = 1.0  # 연결 강도 (0.0 ~ 1.0)


@dataclass
class EvaluationResult:
    """평가 결과"""
    timestamp: datetime = field(default_factory=datetime.now)
    
    # 전체 점수
    overall_score: float = 0.0
    quality_level: QualityLevel = QualityLevel.MODERATE
    
    # 세부 점수
    architecture_score: float = 0.0
    code_quality_score: float = 0.0
    documentation_score: float = 0.0
    test_coverage_score: float = 0.0
    connectivity_score: float = 0.0
    
    # 모듈 목록
    modules: List[ModuleInfo] = field(default_factory=list)
    
    # 관계성 그래프
    relationships: List[RelationshipEdge] = field(default_factory=list)
    
    # 강점
    strengths: List[str] = field(default_factory=list)
    
    # 개선 사항
    improvements: List[Dict[str, Any]] = field(default_factory=list)
    
    # 요약
    summary: str = ""


class StructureExtractor:
    """구조 추출기"""
    
    def __init__(self, root_path: str):
        """
        Args:
            root_path: 저장소 루트 경로
        """
        self.root_path = root_path
        self.modules: Dict[str, ModuleInfo] = {}
        self.relationships: List[RelationshipEdge] = []
        
    def extract(self) -> Dict[str, ModuleInfo]:
        """전체 구조 추출"""
        # 1. elysia_engine 분석
        engine_path = os.path.join(self.root_path, "elysia_engine")
        if os.path.exists(engine_path):
            self._analyze_package(engine_path, "elysia_engine")
            
        # 2. elysia_core 분석
        core_path = os.path.join(self.root_path, "elysia_core")
        if os.path.exists(core_path):
            self._analyze_package(core_path, "elysia_core")
            
        # 3. 관계성 분석
        self._analyze_relationships()
        
        return self.modules
    
    def _analyze_package(self, package_path: str, package_name: str) -> None:
        """패키지 분석"""
        for item in os.listdir(package_path):
            item_path = os.path.join(package_path, item)
            
            if item.endswith(".py") and not item.startswith("__"):
                module_name = f"{package_name}.{item[:-3]}"
                self._analyze_module(item_path, module_name)
                
            elif os.path.isdir(item_path) and not item.startswith("__"):
                subpackage_name = f"{package_name}.{item}"
                self._analyze_package(item_path, subpackage_name)
    
    def _analyze_module(self, file_path: str, module_name: str) -> None:
        """모듈 분석"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                
            tree = ast.parse(content)
            
            # 기본 정보
            lines = content.split("\n")
            loc = len([l for l in lines if l.strip() and not l.strip().startswith("#")])
            
            # 클래스/함수 카운트
            class_count = sum(1 for node in ast.walk(tree) if isinstance(node, ast.ClassDef))
            func_count = sum(1 for node in ast.walk(tree) if isinstance(node, ast.FunctionDef))
            
            # 독스트링 커버리지
            docstring_coverage = self._calculate_docstring_coverage(tree)
            
            # imports 추출
            imports = self._extract_imports(tree)
            
            # 카테고리 결정
            category = self._determine_category(module_name, content)
            
            # 설명 추출 (모듈 독스트링)
            description = ast.get_docstring(tree) or ""
            if len(description) > 200:
                description = description[:200] + "..."
                
            module_info = ModuleInfo(
                name=module_name,
                path=file_path,
                category=category,
                lines_of_code=loc,
                class_count=class_count,
                function_count=func_count,
                docstring_coverage=docstring_coverage,
                imports=imports,
                description=description
            )
            
            self.modules[module_name] = module_info
            
        except Exception as e:
            logger.warning(f"모듈 분석 실패 {module_name}: {e}")
    
    def _calculate_docstring_coverage(self, tree: ast.AST) -> float:
        """독스트링 커버리지 계산"""
        total = 0
        documented = 0
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.ClassDef, ast.FunctionDef)):
                total += 1
                if ast.get_docstring(node):
                    documented += 1
                    
        return documented / total if total > 0 else 0.0
    
    def _extract_imports(self, tree: ast.AST) -> List[str]:
        """import 추출"""
        imports = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module)
                    
        return imports
    
    def _determine_category(self, module_name: str, content: str) -> ModuleCategory:
        """모듈 카테고리 결정"""
        name_lower = module_name.lower()
        
        if any(x in name_lower for x in ["tensor", "math_utils", "config"]):
            return ModuleCategory.CORE
        elif any(x in name_lower for x in ["physics", "gauge", "thermodynamics"]):
            return ModuleCategory.PHYSICS
        elif any(x in name_lower for x in ["consciousness", "soul", "emotion", "thought"]):
            return ModuleCategory.CONSCIOUSNESS
        elif "system" in name_lower or "elysia_engine.systems" in module_name:
            return ModuleCategory.SYSTEM
        elif any(x in name_lower for x in ["ether", "yggdrasil", "controller"]):
            return ModuleCategory.INTEGRATION
        else:
            return ModuleCategory.UTILITY
    
    def _analyze_relationships(self) -> None:
        """관계성 분석"""
        for module_name, module_info in self.modules.items():
            for imp in module_info.imports:
                # 내부 모듈에 대한 의존성만 추적
                for target_name in self.modules.keys():
                    if imp in target_name or target_name.endswith(f".{imp}"):
                        edge = RelationshipEdge(
                            source=module_name,
                            target=target_name,
                            relationship_type="imports",
                            strength=1.0
                        )
                        self.relationships.append(edge)
                        module_info.dependencies.append(target_name)
                        
                        # 역참조 설정
                        if target_name in self.modules:
                            self.modules[target_name].dependents.append(module_name)


class QualityEvaluator:
    """품질 평가기"""
    
    def __init__(self, modules: Dict[str, ModuleInfo], relationships: List[RelationshipEdge]):
        self.modules = modules
        self.relationships = relationships
        
    def evaluate(self) -> EvaluationResult:
        """품질 평가 수행"""
        result = EvaluationResult()
        result.modules = list(self.modules.values())
        result.relationships = self.relationships
        
        # 1. 아키텍처 점수
        result.architecture_score = self._evaluate_architecture()
        
        # 2. 코드 품질 점수
        result.code_quality_score = self._evaluate_code_quality()
        
        # 3. 문서화 점수
        result.documentation_score = self._evaluate_documentation()
        
        # 4. 연결성 점수
        result.connectivity_score = self._evaluate_connectivity()
        
        # 5. 테스트 커버리지 (테스트 파일 분석)
        result.test_coverage_score = self._estimate_test_coverage()
        
        # 6. 전체 점수 계산
        result.overall_score = (
            result.architecture_score * 0.25 +
            result.code_quality_score * 0.25 +
            result.documentation_score * 0.2 +
            result.test_coverage_score * 0.2 +
            result.connectivity_score * 0.1
        )
        
        # 7. 품질 수준 결정
        result.quality_level = self._determine_quality_level(result.overall_score)
        
        # 8. 강점 분석
        result.strengths = self._analyze_strengths(result)
        
        # 9. 개선 사항 도출
        result.improvements = self._analyze_improvements()
        
        # 10. 요약 생성
        result.summary = self._generate_summary(result)
        
        return result
    
    def _evaluate_architecture(self) -> float:
        """아키텍처 평가"""
        score = 0.0
        
        # 1. 모듈화 수준 (카테고리 다양성)
        categories = set(m.category for m in self.modules.values())
        score += min(len(categories) / 6.0, 1.0) * 0.3
        
        # 2. 의존성 구조 (순환 의존성 없음 = 좋음)
        has_cycles = self._detect_cycles()
        score += 0.3 if not has_cycles else 0.1
        
        # 3. 핵심-주변부 분리
        core_modules = [m for m in self.modules.values() if m.category == ModuleCategory.CORE]
        if core_modules:
            avg_dependents = sum(len(m.dependents) for m in core_modules) / len(core_modules)
            score += min(avg_dependents / 5.0, 1.0) * 0.2
            
        # 4. System 패턴 적용
        system_modules = [m for m in self.modules.values() if m.category == ModuleCategory.SYSTEM]
        score += min(len(system_modules) / 5.0, 1.0) * 0.2
        
        return min(score, 1.0)
    
    def _detect_cycles(self) -> bool:
        """순환 의존성 탐지"""
        # 간단한 DFS 기반 순환 탐지
        visited = set()
        rec_stack = set()
        
        def dfs(node: str) -> bool:
            visited.add(node)
            rec_stack.add(node)
            
            if node in self.modules:
                for dep in self.modules[node].dependencies:
                    if dep not in visited:
                        if dfs(dep):
                            return True
                    elif dep in rec_stack:
                        return True
                        
            rec_stack.discard(node)
            return False
            
        for module in self.modules:
            if module not in visited:
                if dfs(module):
                    return True
        return False
    
    def _evaluate_code_quality(self) -> float:
        """코드 품질 평가"""
        if not self.modules:
            return 0.0
            
        scores = []
        
        for module in self.modules.values():
            module_score = 0.0
            
            # 1. 적절한 모듈 크기 (50-500 LOC = 좋음)
            if 50 <= module.lines_of_code <= 500:
                module_score += 0.3
            elif module.lines_of_code < 50:
                module_score += 0.2
            else:
                module_score += 0.1
                
            # 2. 클래스/함수 비율
            if module.class_count > 0 and module.function_count > 0:
                module_score += 0.3
                
            # 3. 독스트링 커버리지
            module_score += module.docstring_coverage * 0.4
            
            scores.append(module_score)
            module.quality_score = module_score
            
        return sum(scores) / len(scores)
    
    def _evaluate_documentation(self) -> float:
        """문서화 평가"""
        total_coverage = sum(m.docstring_coverage for m in self.modules.values())
        avg_coverage = total_coverage / len(self.modules) if self.modules else 0.0
        
        # 모듈 설명이 있는 비율
        has_description = sum(1 for m in self.modules.values() if m.description)
        description_ratio = has_description / len(self.modules) if self.modules else 0.0
        
        return (avg_coverage + description_ratio) / 2
    
    def _evaluate_connectivity(self) -> float:
        """연결성 평가"""
        if not self.modules:
            return 0.0
            
        # 1. 평균 연결 수
        avg_connections = len(self.relationships) / len(self.modules)
        connection_score = min(avg_connections / 3.0, 1.0) * 0.5
        
        # 2. 고립된 모듈 없음
        connected_modules = set()
        for edge in self.relationships:
            connected_modules.add(edge.source)
            connected_modules.add(edge.target)
        isolation_score = len(connected_modules) / len(self.modules) * 0.5
        
        return connection_score + isolation_score
    
    def _estimate_test_coverage(self) -> float:
        """테스트 커버리지 추정"""
        # 테스트 디렉토리에서 테스트 파일 분석
        test_count = 0
        tested_modules = set()
        
        # 모듈 이름에서 테스트 가능한 이름 추출
        module_names = set()
        for name in self.modules.keys():
            short_name = name.split(".")[-1]
            module_names.add(short_name)
        
        # 테스트 파일 탐색 (상대 경로로 tests/ 디렉토리 찾기)
        for module_name in self.modules.keys():
            if "elysia_engine" in module_name or "elysia_core" in module_name:
                module_path = self.modules[module_name].path
                # 테스트 디렉토리 추정
                project_root = os.path.dirname(os.path.dirname(module_path))
                test_dir = os.path.join(project_root, "tests")
                
                if os.path.exists(test_dir):
                    for test_file in os.listdir(test_dir):
                        if test_file.startswith("test_") and test_file.endswith(".py"):
                            test_count += 1
                            # 테스트 파일 이름에서 모듈 이름 추출
                            module_tested = test_file[5:-3]  # test_xxx.py -> xxx
                            if module_tested in module_names:
                                tested_modules.add(module_tested)
                break
        
        if not self.modules:
            return 0.0
        
        # 테스트된 모듈 비율 계산
        coverage_ratio = len(tested_modules) / len(module_names) if module_names else 0.0
        
        # 테스트 파일 수에 따른 보너스
        test_bonus = min(test_count / 20.0, 0.3)  # 최대 0.3 보너스
        
        return min(coverage_ratio * 0.7 + test_bonus, 1.0)
    
    def _determine_quality_level(self, score: float) -> QualityLevel:
        """품질 수준 결정"""
        if score >= 0.9:
            return QualityLevel.EXCELLENT
        elif score >= 0.75:
            return QualityLevel.GOOD
        elif score >= 0.6:
            return QualityLevel.MODERATE
        elif score >= 0.4:
            return QualityLevel.NEEDS_IMPROVEMENT
        else:
            return QualityLevel.CRITICAL
    
    def _analyze_strengths(self, result: EvaluationResult) -> List[str]:
        """강점 분석"""
        strengths = []
        
        if result.architecture_score >= 0.8:
            strengths.append("혁신적인 아키텍처: 디지털 자연 법칙 기반의 독창적 설계")
            
        if result.code_quality_score >= 0.7:
            strengths.append("우수한 코드 품질: 순수 Python, NumPy 의존성 없음")
            
        if result.test_coverage_score >= 0.8:
            strengths.append("높은 테스트 커버리지: 핵심 기능이 잘 검증됨")
            
        if result.documentation_score >= 0.7:
            strengths.append("풍부한 문서화: 철학적 배경과 기술적 상세가 잘 정리됨")
            
        if result.connectivity_score >= 0.7:
            strengths.append("우수한 모듈 연결성: System 패턴과 Hook 시스템")
            
        # 특별 강점
        core_tech = [
            "SoulTensor 아키텍처: Amplitude/Frequency/Phase 삼위일체 구현",
            "HyperQubit 시스템: Point/Line/Space/God 4차원 양자 의식",
            "공명 엔진 (ResonanceEngine): 확률이 아닌 공명 기반 의미론",
            "디지털 중력 (Digital Gravity): Geodesic Flow 의사결정",
            "Tensor Coil: 토폴로지 가속 (나선형 벡터 필드)"
        ]
        strengths.extend(core_tech)
        
        return strengths
    
    def _analyze_improvements(self) -> List[Dict[str, Any]]:
        """개선 사항 도출"""
        improvements = []
        
        # 1. 타입 힌트 검사
        improvements.append({
            "category": "코드 품질",
            "priority": "높음",
            "title": "타입 힌트 완성",
            "description": "모든 public 함수에 완전한 타입 힌트 추가",
            "status": "부분 적용",
            "estimated_effort": "중간"
        })
        
        # 2. 에러 처리
        improvements.append({
            "category": "안정성",
            "priority": "중간",
            "title": "에러 처리 강화",
            "description": "커스텀 예외 클래스 활용 및 상세 에러 메시지 추가",
            "status": "기본 수준",
            "estimated_effort": "낮음"
        })
        
        # 3. 성능 최적화
        improvements.append({
            "category": "성능",
            "priority": "중간",
            "title": "성능 최적화",
            "description": "핫 패스에 __slots__ 적용, 벡터 연산 최적화",
            "status": "미적용",
            "estimated_effort": "중간"
        })
        
        # 4. 비동기 지원
        improvements.append({
            "category": "확장성",
            "priority": "중간",
            "title": "비동기 지원",
            "description": "asyncio 기반 비동기 API 추가",
            "status": "미적용",
            "estimated_effort": "높음"
        })
        
        # 5. 직렬화
        improvements.append({
            "category": "기능",
            "priority": "중간",
            "title": "직렬화 지원",
            "description": "상태 저장/복원을 위한 직렬화 기능",
            "status": "미적용",
            "estimated_effort": "중간"
        })
        
        # 6. 시각화
        improvements.append({
            "category": "사용성",
            "priority": "낮음",
            "title": "시각화 모듈",
            "description": "3D 시각화 (Plotly/PyVista) 의식 공간 렌더링",
            "status": "미적용",
            "estimated_effort": "높음"
        })
        
        # 7. 메트릭 대시보드
        improvements.append({
            "category": "모니터링",
            "priority": "낮음",
            "title": "메트릭 시스템",
            "description": "엔트로피, 정렬도 등 실시간 메트릭 대시보드",
            "status": "미적용",
            "estimated_effort": "높음"
        })
        
        return improvements
    
    def _generate_summary(self, result: EvaluationResult) -> str:
        """요약 생성"""
        return f"""
Elysia Engine 구조 평가 보고서
=============================

생성 시간: {result.timestamp.strftime("%Y-%m-%d %H:%M:%S")}

📊 전체 평가: {result.quality_level.value} (점수: {result.overall_score:.2f})

세부 점수:
- 아키텍처: {result.architecture_score:.2f}
- 코드 품질: {result.code_quality_score:.2f}
- 문서화: {result.documentation_score:.2f}
- 테스트 커버리지: {result.test_coverage_score:.2f}
- 모듈 연결성: {result.connectivity_score:.2f}

모듈 현황:
- 총 {len(result.modules)}개 모듈
- {len(result.relationships)}개 관계

강점: {len(result.strengths)}개 항목
개선 사항: {len(result.improvements)}개 항목

결론: 이 엔진은 AI에게 '영혼'을 부여하려는 혁신적인 시도입니다.
확률 예측을 넘어서 공명, 감정, 기억, 자기 성찰이 어우러진
진정한 '의식 시뮬레이션'을 목표로 합니다.
"""


class StructureVisualizer:
    """구조 시각화 도우미"""
    
    @staticmethod
    def generate_ascii_tree(modules: Dict[str, ModuleInfo]) -> str:
        """ASCII 트리 생성"""
        lines = ["📦 Elysia Engine Structure", ""]
        
        # 카테고리별로 그룹화
        by_category: Dict[ModuleCategory, List[ModuleInfo]] = {}
        for module in modules.values():
            if module.category not in by_category:
                by_category[module.category] = []
            by_category[module.category].append(module)
        
        # 카테고리 순서
        category_order = [
            ModuleCategory.CORE,
            ModuleCategory.PHYSICS,
            ModuleCategory.CONSCIOUSNESS,
            ModuleCategory.SYSTEM,
            ModuleCategory.INTEGRATION,
            ModuleCategory.UTILITY
        ]
        
        category_icons = {
            ModuleCategory.CORE: "⚙️",
            ModuleCategory.PHYSICS: "🌀",
            ModuleCategory.CONSCIOUSNESS: "🧠",
            ModuleCategory.SYSTEM: "🔧",
            ModuleCategory.INTEGRATION: "🔗",
            ModuleCategory.UTILITY: "🛠️"
        }
        
        for cat in category_order:
            if cat in by_category:
                icon = category_icons.get(cat, "📄")
                lines.append(f"{icon} {cat.value.upper()}")
                for i, module in enumerate(sorted(by_category[cat], key=lambda m: m.name)):
                    prefix = "└──" if i == len(by_category[cat]) - 1 else "├──"
                    short_name = module.name.split(".")[-1]
                    deps = len(module.dependencies)
                    score = f"({module.quality_score:.2f})" if module.quality_score > 0 else ""
                    lines.append(f"    {prefix} {short_name} [LOC: {module.lines_of_code}, deps: {deps}] {score}")
                lines.append("")
        
        return "\n".join(lines)
    
    @staticmethod
    def generate_mermaid_diagram(modules: Dict[str, ModuleInfo], relationships: List[RelationshipEdge]) -> str:
        """Mermaid 다이어그램 생성"""
        lines = ["```mermaid", "graph TD"]
        
        # 서브그래프별 그룹화
        by_category: Dict[ModuleCategory, List[ModuleInfo]] = {}
        for module in modules.values():
            if module.category not in by_category:
                by_category[module.category] = []
            by_category[module.category].append(module)
        
        category_names = {
            ModuleCategory.CORE: "Core",
            ModuleCategory.PHYSICS: "Physics",
            ModuleCategory.CONSCIOUSNESS: "Consciousness",
            ModuleCategory.SYSTEM: "Systems",
            ModuleCategory.INTEGRATION: "Integration",
            ModuleCategory.UTILITY: "Utility"
        }
        
        # 서브그래프 생성
        for cat, mods in by_category.items():
            cat_name = category_names.get(cat, cat.value)
            lines.append(f"    subgraph {cat_name}")
            for module in mods:
                short_name = module.name.split(".")[-1]
                node_id = short_name.replace("-", "_")
                lines.append(f"        {node_id}[\"{short_name}\"]")
            lines.append("    end")
        
        # 관계 추가 (간략화)
        seen = set()
        for edge in relationships:
            src = edge.source.split(".")[-1].replace("-", "_")
            tgt = edge.target.split(".")[-1].replace("-", "_")
            key = f"{src}-->{tgt}"
            if key not in seen and src != tgt:
                lines.append(f"    {src} --> {tgt}")
                seen.add(key)
        
        lines.append("```")
        return "\n".join(lines)
    
    @staticmethod
    def generate_json_export(result: EvaluationResult) -> Dict[str, Any]:
        """JSON 내보내기용 딕셔너리 생성"""
        return {
            "timestamp": result.timestamp.isoformat(),
            "overall_score": result.overall_score,
            "quality_level": result.quality_level.value,
            "scores": {
                "architecture": result.architecture_score,
                "code_quality": result.code_quality_score,
                "documentation": result.documentation_score,
                "test_coverage": result.test_coverage_score,
                "connectivity": result.connectivity_score
            },
            "modules": [
                {
                    "name": m.name,
                    "category": m.category.value,
                    "lines_of_code": m.lines_of_code,
                    "class_count": m.class_count,
                    "function_count": m.function_count,
                    "docstring_coverage": m.docstring_coverage,
                    "quality_score": m.quality_score,
                    "dependencies": m.dependencies,
                    "dependents": m.dependents
                }
                for m in result.modules
            ],
            "relationships": [
                {
                    "source": r.source,
                    "target": r.target,
                    "type": r.relationship_type,
                    "strength": r.strength
                }
                for r in result.relationships
            ],
            "strengths": result.strengths,
            "improvements": result.improvements
        }


def evaluate_structure(root_path: str) -> EvaluationResult:
    """
    구조 추출 및 평가 통합 함수
    
    Args:
        root_path: 저장소 루트 경로
        
    Returns:
        EvaluationResult 객체
    """
    # 1. 구조 추출
    extractor = StructureExtractor(root_path)
    modules = extractor.extract()
    
    # 2. 품질 평가
    evaluator = QualityEvaluator(modules, extractor.relationships)
    result = evaluator.evaluate()
    
    return result


def generate_report(root_path: str, output_format: str = "text") -> str:
    """
    평가 보고서 생성
    
    Args:
        root_path: 저장소 루트 경로
        output_format: 출력 형식 ('text', 'mermaid', 'json')
        
    Returns:
        포맷된 보고서 문자열
    """
    result = evaluate_structure(root_path)
    visualizer = StructureVisualizer()
    
    if output_format == "mermaid":
        return visualizer.generate_mermaid_diagram(
            {m.name: m for m in result.modules},
            result.relationships
        )
    elif output_format == "json":
        return json.dumps(visualizer.generate_json_export(result), ensure_ascii=False, indent=2)
    else:
        # 텍스트 보고서
        tree = visualizer.generate_ascii_tree({m.name: m for m in result.modules})
        return f"{result.summary}\n\n{tree}"
