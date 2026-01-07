"""
Self Reflector (자아 성찰 모듈)
===============================

"To improve, I must first know myself."

이 모듈은 Elysia가 자신의 소스 코드를 읽고 분석하는 '메타인지(Metacognition)' 기관입니다.
Python의 AST(Abstract Syntax Tree)를 사용하여 코드의 구조, 복잡도, 의존성을 분석합니다.

기능:
1. File Analysis: 파일의 라인 수, 함수 개수, 클래스 개수 분석
2. Complexity Analysis: 순환 복잡도(Cyclomatic Complexity) 계산
3. Structure Mapping: 프로젝트 전체 구조 파악
"""

import ast
import os
import logging
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field

logger = logging.getLogger("SelfReflector")

@dataclass
class FunctionMetrics:
    name: str
    docstring: Optional[str]
    complexity: int
    loc: int

@dataclass
class ClassMetrics:
    name: str
    docstring: Optional[str]
    bases: List[str] # Inheritance
    methods: List[FunctionMetrics] = field(default_factory=list)

@dataclass
class CodeMetrics:
    filename: str
    loc: int
    complexity: int
    imports: List[str]
    classes: List[ClassMetrics] = field(default_factory=list)
    functions: List[FunctionMetrics] = field(default_factory=list) # Top-level functions

class SelfReflector:
    def __init__(self, root_path: str = "c:/Elysia"):
        self.root_path = root_path
        logger.info(f"🪞 SelfReflector initialized. Root: {root_path}")

    def analyze_file(self, file_path: str) -> CodeMetrics:
        """단일 파일의 심층 구조(Anatomy)를 분석합니다."""
        try:
            with open(file_path, 'r', encoding='utf-8-sig') as f:
                content = f.read()
            
            tree = ast.parse(content)
            loc = len(content.splitlines())
            
            # Imports
            imports = []
            for node in ast.walk(tree):
                if isinstance(node, (ast.Import, ast.ImportFrom)):
                    for alias in node.names:
                        imports.append(alias.name)

            # Top-level Classes & Functions
            classes = []
            functions = []
            total_complexity = 0

            for node in tree.body:
                if isinstance(node, ast.ClassDef):
                    classes.append(self._analyze_class(node))
                elif isinstance(node, ast.FunctionDef):
                    functions.append(self._analyze_function(node))
                
                # Check for complexity in top-level code
                total_complexity += self._calc_complexity(node)

            # Sum up complexity
            for c in classes:
                total_complexity += sum(m.complexity for m in c.methods)
            for f in functions:
                total_complexity += f.complexity

            return CodeMetrics(
                filename=os.path.basename(file_path),
                loc=loc,
                complexity=total_complexity,
                imports=imports,
                classes=classes,
                functions=functions
            )
            
        except Exception as e:
            logger.error(f"Failed to analyze {file_path}: {e}")
            return CodeMetrics(os.path.basename(file_path), 0, 0, [], [], [])

    def _analyze_class(self, node: ast.ClassDef) -> ClassMetrics:
        bases = [b.id for b in node.bases if isinstance(b, ast.Name)]
        methods = []
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                methods.append(self._analyze_function(item))
        
        return ClassMetrics(
            name=node.name,
            docstring=ast.get_docstring(node),
            bases=bases,
            methods=methods
        )

    def _analyze_function(self, node: ast.FunctionDef) -> FunctionMetrics:
        complexity = self._calc_complexity(node)
        loc = getattr(node, 'end_lineno', 0) - getattr(node, 'lineno', 0)
        return FunctionMetrics(
            name=node.name,
            docstring=ast.get_docstring(node),
            complexity=complexity,
            loc=loc
        )

    def _calc_complexity(self, node: ast.AST) -> int:
        complexity = 0
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.For, ast.While, ast.Try, ast.ExceptHandler, ast.With)):
                complexity += 1
        return complexity

    def reflect_on_core(self) -> Dict[str, CodeMetrics]:
        """Core 디렉토리 내의 주요 파일들을 분석합니다."""
        core_path = os.path.join(self.root_path, "Core")
        results = {}
        for root, _, files in os.walk(core_path):
            for file in files:
                if file.endswith(".py"):
                    full_path = os.path.join(root, file)
                    results[file] = self.analyze_file(full_path)
        return results


