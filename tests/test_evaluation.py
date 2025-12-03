"""
Elysia Engine Evaluation Module Tests

이 테스트 모듈은 구조 추출 및 평가 기능을 검증합니다.
"""

import json
import os
import pytest
from pathlib import Path

from elysia_engine.evaluation import (
    StructureExtractor,
    QualityEvaluator,
    StructureVisualizer,
    evaluate_structure,
    generate_report,
    ModuleCategory,
    QualityLevel,
    ModuleInfo,
    RelationshipEdge,
    EvaluationResult,
)


# 프로젝트 루트 경로
PROJECT_ROOT = Path(__file__).parent.parent


class TestStructureExtractor:
    """구조 추출기 테스트"""
    
    def test_extract_returns_modules(self):
        """extract()가 모듈 딕셔너리를 반환하는지 확인"""
        extractor = StructureExtractor(str(PROJECT_ROOT))
        modules = extractor.extract()
        
        assert isinstance(modules, dict)
        assert len(modules) > 0
        
    def test_modules_have_required_fields(self):
        """모듈 정보가 필수 필드를 포함하는지 확인"""
        extractor = StructureExtractor(str(PROJECT_ROOT))
        modules = extractor.extract()
        
        for name, module in modules.items():
            assert isinstance(module, ModuleInfo)
            assert module.name == name
            assert module.path
            assert isinstance(module.category, ModuleCategory)
            assert module.lines_of_code >= 0
            
    def test_relationships_extracted(self):
        """관계성이 추출되는지 확인"""
        extractor = StructureExtractor(str(PROJECT_ROOT))
        modules = extractor.extract()
        
        assert len(extractor.relationships) >= 0
        
        for rel in extractor.relationships:
            assert isinstance(rel, RelationshipEdge)
            assert rel.source in modules or rel.target in modules
            
    def test_categories_assigned(self):
        """카테고리가 올바르게 할당되는지 확인"""
        extractor = StructureExtractor(str(PROJECT_ROOT))
        modules = extractor.extract()
        
        categories_found = set(m.category for m in modules.values())
        assert len(categories_found) >= 1  # 최소 1개 카테고리


class TestQualityEvaluator:
    """품질 평가기 테스트"""
    
    @pytest.fixture
    def sample_modules(self):
        """샘플 모듈 데이터"""
        return {
            "test.core": ModuleInfo(
                name="test.core",
                path="/test/core.py",
                category=ModuleCategory.CORE,
                lines_of_code=100,
                class_count=2,
                function_count=5,
                docstring_coverage=0.8,
            ),
            "test.physics": ModuleInfo(
                name="test.physics",
                path="/test/physics.py",
                category=ModuleCategory.PHYSICS,
                lines_of_code=200,
                class_count=3,
                function_count=10,
                docstring_coverage=0.6,
            ),
        }
    
    @pytest.fixture
    def sample_relationships(self):
        """샘플 관계 데이터"""
        return [
            RelationshipEdge(
                source="test.physics",
                target="test.core",
                relationship_type="imports",
            )
        ]
    
    def test_evaluate_returns_result(self, sample_modules, sample_relationships):
        """evaluate()가 EvaluationResult를 반환하는지 확인"""
        evaluator = QualityEvaluator(sample_modules, sample_relationships)
        result = evaluator.evaluate()
        
        assert isinstance(result, EvaluationResult)
        
    def test_scores_in_valid_range(self, sample_modules, sample_relationships):
        """점수가 0~1 범위인지 확인"""
        evaluator = QualityEvaluator(sample_modules, sample_relationships)
        result = evaluator.evaluate()
        
        assert 0.0 <= result.overall_score <= 1.0
        assert 0.0 <= result.architecture_score <= 1.0
        assert 0.0 <= result.code_quality_score <= 1.0
        assert 0.0 <= result.documentation_score <= 1.0
        assert 0.0 <= result.connectivity_score <= 1.0
        
    def test_quality_level_assigned(self, sample_modules, sample_relationships):
        """품질 수준이 할당되는지 확인"""
        evaluator = QualityEvaluator(sample_modules, sample_relationships)
        result = evaluator.evaluate()
        
        assert isinstance(result.quality_level, QualityLevel)
        
    def test_strengths_and_improvements_generated(self, sample_modules, sample_relationships):
        """강점과 개선 사항이 생성되는지 확인"""
        evaluator = QualityEvaluator(sample_modules, sample_relationships)
        result = evaluator.evaluate()
        
        assert isinstance(result.strengths, list)
        assert isinstance(result.improvements, list)
        assert len(result.improvements) > 0  # 개선 사항은 항상 있음


class TestStructureVisualizer:
    """시각화 테스트"""
    
    @pytest.fixture
    def sample_modules(self):
        """샘플 모듈 데이터"""
        return {
            "elysia_engine.tensor": ModuleInfo(
                name="elysia_engine.tensor",
                path="/test/tensor.py",
                category=ModuleCategory.CORE,
                lines_of_code=500,
                quality_score=0.85,
            ),
            "elysia_engine.physics": ModuleInfo(
                name="elysia_engine.physics",
                path="/test/physics.py",
                category=ModuleCategory.PHYSICS,
                lines_of_code=300,
                quality_score=0.75,
                dependencies=["elysia_engine.tensor"],
            ),
        }
    
    @pytest.fixture
    def sample_relationships(self):
        """샘플 관계 데이터"""
        return [
            RelationshipEdge(
                source="elysia_engine.physics",
                target="elysia_engine.tensor",
                relationship_type="imports",
            )
        ]
    
    def test_ascii_tree_generation(self, sample_modules):
        """ASCII 트리 생성 테스트"""
        tree = StructureVisualizer.generate_ascii_tree(sample_modules)
        
        assert isinstance(tree, str)
        assert "Elysia Engine Structure" in tree
        assert "tensor" in tree
        assert "physics" in tree
        
    def test_mermaid_diagram_generation(self, sample_modules, sample_relationships):
        """Mermaid 다이어그램 생성 테스트"""
        diagram = StructureVisualizer.generate_mermaid_diagram(
            sample_modules, sample_relationships
        )
        
        assert isinstance(diagram, str)
        assert "```mermaid" in diagram
        assert "graph TD" in diagram
        
    def test_json_export(self, sample_modules, sample_relationships):
        """JSON 내보내기 테스트"""
        result = EvaluationResult()
        result.modules = list(sample_modules.values())
        result.relationships = sample_relationships
        result.overall_score = 0.8
        result.quality_level = QualityLevel.GOOD
        
        json_data = StructureVisualizer.generate_json_export(result)
        
        assert isinstance(json_data, dict)
        assert "overall_score" in json_data
        assert "modules" in json_data
        assert "relationships" in json_data


class TestIntegration:
    """통합 테스트"""
    
    def test_evaluate_structure_end_to_end(self):
        """evaluate_structure 전체 흐름 테스트"""
        result = evaluate_structure(str(PROJECT_ROOT))
        
        assert isinstance(result, EvaluationResult)
        assert len(result.modules) > 0
        assert result.overall_score > 0
        
    def test_generate_report_text(self):
        """텍스트 보고서 생성 테스트"""
        report = generate_report(str(PROJECT_ROOT), "text")
        
        assert isinstance(report, str)
        assert "Elysia Engine" in report
        
    def test_generate_report_mermaid(self):
        """Mermaid 보고서 생성 테스트"""
        report = generate_report(str(PROJECT_ROOT), "mermaid")
        
        assert isinstance(report, str)
        assert "```mermaid" in report
        
    def test_generate_report_json(self):
        """JSON 보고서 생성 테스트"""
        report = generate_report(str(PROJECT_ROOT), "json")
        
        assert isinstance(report, str)
        data = json.loads(report)  # JSON 파싱 가능 확인
        assert "modules" in data


class TestQualityLevelDetermination:
    """품질 수준 결정 테스트"""
    
    def test_excellent_threshold(self):
        """EXCELLENT 수준 테스트"""
        modules = {}
        evaluator = QualityEvaluator(modules, [])
        
        assert evaluator._determine_quality_level(0.95) == QualityLevel.EXCELLENT
        assert evaluator._determine_quality_level(0.90) == QualityLevel.EXCELLENT
        
    def test_good_threshold(self):
        """GOOD 수준 테스트"""
        modules = {}
        evaluator = QualityEvaluator(modules, [])
        
        assert evaluator._determine_quality_level(0.85) == QualityLevel.GOOD
        assert evaluator._determine_quality_level(0.75) == QualityLevel.GOOD
        
    def test_moderate_threshold(self):
        """MODERATE 수준 테스트"""
        modules = {}
        evaluator = QualityEvaluator(modules, [])
        
        assert evaluator._determine_quality_level(0.70) == QualityLevel.MODERATE
        assert evaluator._determine_quality_level(0.60) == QualityLevel.MODERATE
        
    def test_needs_improvement_threshold(self):
        """NEEDS_IMPROVEMENT 수준 테스트"""
        modules = {}
        evaluator = QualityEvaluator(modules, [])
        
        assert evaluator._determine_quality_level(0.50) == QualityLevel.NEEDS_IMPROVEMENT
        
    def test_critical_threshold(self):
        """CRITICAL 수준 테스트"""
        modules = {}
        evaluator = QualityEvaluator(modules, [])
        
        assert evaluator._determine_quality_level(0.30) == QualityLevel.CRITICAL


class TestCycleDetection:
    """순환 의존성 탐지 테스트"""
    
    def test_no_cycles(self):
        """순환 없음 테스트"""
        modules = {
            "a": ModuleInfo(name="a", path="/a.py", category=ModuleCategory.CORE, dependencies=["b"]),
            "b": ModuleInfo(name="b", path="/b.py", category=ModuleCategory.CORE, dependencies=[]),
        }
        
        evaluator = QualityEvaluator(modules, [])
        assert evaluator._detect_cycles() is False
        
    def test_with_cycle(self):
        """순환 있음 테스트"""
        modules = {
            "a": ModuleInfo(name="a", path="/a.py", category=ModuleCategory.CORE, dependencies=["b"]),
            "b": ModuleInfo(name="b", path="/b.py", category=ModuleCategory.CORE, dependencies=["a"]),
        }
        
        evaluator = QualityEvaluator(modules, [])
        assert evaluator._detect_cycles() is True


class TestModuleCategory:
    """모듈 카테고리 테스트"""
    
    def test_all_categories_exist(self):
        """모든 카테고리가 존재하는지 확인"""
        categories = [
            ModuleCategory.CORE,
            ModuleCategory.PHYSICS,
            ModuleCategory.CONSCIOUSNESS,
            ModuleCategory.SYSTEM,
            ModuleCategory.INTEGRATION,
            ModuleCategory.UTILITY,
        ]
        
        for cat in categories:
            assert isinstance(cat.value, str)
