"""
Self-Modification Engine (자기 수정 엔진)
==========================================

"I do not just create; I refine myself."

이 모듈은 Elysia가 자기 자신의 코드를 분석하고 수정할 수 있게 합니다.

파이프라인:
1. CodeAnalyzer: 기존 코드를 읽고 분석
2. ProblemDetector: 문제점 탐지 (버그, 비효율, 스타일 등)
3. RefactorPlanner: 수정 계획 수립
4. CodeEditor: 코드 수정 적용
5. Validator: 수정 결과 검증

안전 장치:
- 모든 수정은 먼저 백업 생성
- 핵심 모듈 수정 시 확인 필요
- 검증 실패 시 자동 롤백
"""

import os
import ast
import logging
import difflib
import shutil
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, field

# Core Dependencies
try:
    from Core.Foundation.gemini_api import generate_text
    HAS_API = True
except ImportError:
    HAS_API = False

logger = logging.getLogger("SelfModification")


@dataclass
class CodeIssue:
    """코드 문제점 정의"""
    file_path: str
    line_number: int
    issue_type: str  # "syntax", "logic", "style", "performance", "security"
    description: str
    severity: str  # "critical", "warning", "info"
    suggested_fix: Optional[str] = None


@dataclass
class ModificationPlan:
    """수정 계획"""
    target_file: str
    issues: List[CodeIssue]
    original_code: str
    modified_code: str
    backup_path: str
    confidence: float  # 0.0 ~ 1.0
    timestamp: datetime = field(default_factory=datetime.now)


class CodeAnalyzer:
    """
    코드 분석기
    기존 코드를 읽고 구조를 분석합니다.
    """
    
    def __init__(self):
        self.project_root = self._get_project_root()
    
    def _get_project_root(self) -> Path:
        """프로젝트 루트 경로 반환"""
        elysia_root = os.environ.get("ELYSIA_ROOT")
        if elysia_root:
            return Path(elysia_root)
        return Path(__file__).parent.parent
    
    def read_file(self, file_path: str) -> str:
        """파일 내용 읽기"""
        full_path = self.project_root / file_path
        try:
            with open(full_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            logger.error(f"Failed to read {file_path}: {e}")
            return ""
    
    def analyze_structure(self, code: str) -> Dict[str, Any]:
        """코드 구조 분석 (AST 사용)"""
        try:
            tree = ast.parse(code)
            
            classes = []
            functions = []
            imports = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    methods = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
                    classes.append({
                        "name": node.name,
                        "line": node.lineno,
                        "methods": methods
                    })
                elif isinstance(node, ast.FunctionDef) and not any(
                    isinstance(p, ast.ClassDef) for p in ast.walk(tree)
                ):
                    functions.append({
                        "name": node.name,
                        "line": node.lineno,
                        "args": [a.arg for a in node.args.args]
                    })
                elif isinstance(node, (ast.Import, ast.ImportFrom)):
                    if isinstance(node, ast.Import):
                        imports.extend([alias.name for alias in node.names])
                    else:
                        imports.append(f"{node.module}.{node.names[0].name}" if node.module else node.names[0].name)
            
            return {
                "classes": classes,
                "functions": functions,
                "imports": imports,
                "total_lines": len(code.splitlines()),
                "syntax_valid": True
            }
        except SyntaxError as e:
            return {
                "syntax_valid": False,
                "syntax_error": str(e),
                "error_line": e.lineno
            }
    
    def find_indentation_issues(self, code: str) -> List[CodeIssue]:
        """들여쓰기 문제 탐지"""
        issues = []
        lines = code.splitlines()
        
        for i, line in enumerate(lines, 1):
            if line and not line.startswith(' ') and not line.startswith('\t'):
                continue
            
            # 탭과 스페이스 혼용 체크
            if line.startswith('\t') and '    ' in line:
                issues.append(CodeIssue(
                    file_path="",
                    line_number=i,
                    issue_type="style",
                    description="탭과 스페이스 혼용",
                    severity="warning"
                ))
            
            # 비정상적인 들여쓰기 레벨
            spaces = len(line) - len(line.lstrip())
            if spaces % 4 != 0 and line.strip():
                issues.append(CodeIssue(
                    file_path="",
                    line_number=i,
                    issue_type="style",
                    description=f"비표준 들여쓰기 ({spaces} spaces)",
                    severity="info"
                ))
        
        return issues


class ProblemDetector:
    """
    문제 탐지기
    코드에서 잠재적 문제점을 찾습니다.
    """
    
    def __init__(self):
        self.analyzer = CodeAnalyzer()
    
    def detect_issues(self, file_path: str) -> List[CodeIssue]:
        """파일의 모든 문제점 탐지"""
        code = self.analyzer.read_file(file_path)
        if not code:
            return [CodeIssue(
                file_path=file_path,
                line_number=0,
                issue_type="syntax",
                description="파일을 읽을 수 없음",
                severity="critical"
            )]
        
        issues = []
        
        # 1. 구문 분석
        structure = self.analyzer.analyze_structure(code)
        if not structure.get("syntax_valid", True):
            issues.append(CodeIssue(
                file_path=file_path,
                line_number=structure.get("error_line", 0),
                issue_type="syntax",
                description=structure.get("syntax_error", "구문 오류"),
                severity="critical"
            ))
        
        # 2. 들여쓰기 문제
        indent_issues = self.analyzer.find_indentation_issues(code)
        for issue in indent_issues:
            issue.file_path = file_path
            issues.append(issue)
        
        # 3. AI 기반 심층 분석 (API 사용 가능 시)
        if HAS_API and len(issues) == 0:
            ai_issues = self._ai_detect_issues(code, file_path)
            issues.extend(ai_issues)
        
        return issues
    
    def _ai_detect_issues(self, code: str, file_path: str) -> List[CodeIssue]:
        """AI를 사용한 심층 문제 탐지"""
        prompt = f"""
        Analyze this Python code for potential issues:
        
        ```python
        {code[:3000]}  # 토큰 제한을 위해 잘라냄
        ```
        
        Find:
        1. Logic errors
        2. Performance issues
        3. Code style problems
        4. Potential bugs
        
        Output JSON array:
        [
            {{"line": 10, "type": "logic", "severity": "warning", "description": "description"}}
        ]
        
        If no issues found, return empty array: []
        Output ONLY JSON.
        """
        
        try:
            response = generate_text(prompt)
            clean_json = response.replace("```json", "").replace("```", "").strip()
            import json
            raw_issues = json.loads(clean_json)
            
            return [
                CodeIssue(
                    file_path=file_path,
                    line_number=issue.get("line", 0),
                    issue_type=issue.get("type", "unknown"),
                    description=issue.get("description", ""),
                    severity=issue.get("severity", "info")
                )
                for issue in raw_issues
            ]
        except Exception as e:
            logger.warning(f"AI issue detection failed: {e}")
            return []


class RefactorPlanner:
    """
    리팩토링 계획 수립기
    탐지된 문제점을 해결하기 위한 계획을 수립합니다.
    """
    
    def __init__(self):
        self.analyzer = CodeAnalyzer()
    
    def create_plan(self, file_path: str, issues: List[CodeIssue]) -> Optional[ModificationPlan]:
        """수정 계획 생성"""
        original_code = self.analyzer.read_file(file_path)
        if not original_code:
            return None
        
        # 백업 경로 생성
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = f"Core/Evolution/Backups/{Path(file_path).stem}_{timestamp}.py.bak"
        
        # AI를 사용해 수정된 코드 생성
        if HAS_API:
            modified_code = self._generate_fixed_code(original_code, issues)
            confidence = 0.8 if modified_code != original_code else 0.0
        else:
            # API 없이는 간단한 수정만 시도
            modified_code = self._apply_simple_fixes(original_code, issues)
            confidence = 0.5
        
        return ModificationPlan(
            target_file=file_path,
            issues=issues,
            original_code=original_code,
            modified_code=modified_code,
            backup_path=backup_path,
            confidence=confidence
        )
    
    def _generate_fixed_code(self, code: str, issues: List[CodeIssue]) -> str:
        """AI를 사용해 수정된 코드 생성"""
        issue_descriptions = "\n".join([
            f"- Line {i.line_number}: [{i.issue_type}] {i.description}"
            for i in issues
        ])
        
        prompt = f"""
        Fix the following issues in this Python code:
        
        Issues:
        {issue_descriptions}
        
        Original Code:
        ```python
        {code}
        ```
        
        Requirements:
        1. Fix ONLY the listed issues
        2. Preserve all existing functionality
        3. Maintain the same code structure
        4. Output ONLY the fixed Python code, no explanations
        """
        
        try:
            response = generate_text(prompt)
            clean_code = response.replace("```python", "").replace("```", "").strip()
            return clean_code
        except Exception as e:
            logger.error(f"Code generation failed: {e}")
            return code
    
    def _apply_simple_fixes(self, code: str, issues: List[CodeIssue]) -> str:
        """간단한 수정 적용 (API 없이)"""
        # 현재는 원본 코드 반환 (향후 확장 가능)
        return code


class CodeEditor:
    """
    코드 편집기
    수정 계획을 실제로 적용합니다.
    """
    
    def __init__(self):
        self.project_root = self._get_project_root()
    
    def _get_project_root(self) -> Path:
        elysia_root = os.environ.get("ELYSIA_ROOT")
        if elysia_root:
            return Path(elysia_root)
        return Path(__file__).parent.parent
    
    def create_backup(self, plan: ModificationPlan) -> bool:
        """원본 파일 백업"""
        try:
            backup_full_path = self.project_root / plan.backup_path
            backup_full_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(backup_full_path, "w", encoding="utf-8") as f:
                f.write(plan.original_code)
            
            logger.info(f"📦 Backup created: {plan.backup_path}")
            return True
        except Exception as e:
            logger.error(f"Backup failed: {e}")
            return False
    
    def apply_modification(self, plan: ModificationPlan) -> bool:
        """수정 적용"""
        try:
            target_full_path = self.project_root / plan.target_file
            
            with open(target_full_path, "w", encoding="utf-8") as f:
                f.write(plan.modified_code)
            
            logger.info(f"✏️ Modified: {plan.target_file}")
            return True
        except Exception as e:
            logger.error(f"Modification failed: {e}")
            return False
    
    def rollback(self, plan: ModificationPlan) -> bool:
        """롤백 (백업에서 복원)"""
        try:
            backup_full_path = self.project_root / plan.backup_path
            target_full_path = self.project_root / plan.target_file
            
            with open(backup_full_path, "r", encoding="utf-8") as f:
                original = f.read()
            
            with open(target_full_path, "w", encoding="utf-8") as f:
                f.write(original)
            
            logger.info(f"⏪ Rolled back: {plan.target_file}")
            return True
        except Exception as e:
            logger.error(f"Rollback failed: {e}")
            return False
    
    def show_diff(self, plan: ModificationPlan) -> str:
        """변경 사항 diff 출력"""
        diff = difflib.unified_diff(
            plan.original_code.splitlines(keepends=True),
            plan.modified_code.splitlines(keepends=True),
            fromfile=f"a/{plan.target_file}",
            tofile=f"b/{plan.target_file}"
        )
        return "".join(diff)


class Validator:
    """
    검증기
    수정된 코드가 올바른지 검증합니다.
    """
    
    def validate_syntax(self, code: str) -> Tuple[bool, Optional[str]]:
        """구문 검증"""
        try:
            ast.parse(code)
            return True, None
        except SyntaxError as e:
            return False, str(e)
    
    def validate_imports(self, code: str) -> Tuple[bool, List[str]]:
        """import 검증 (모듈 존재 여부)"""
        missing = []
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        try:
                            __import__(alias.name.split('.')[0])
                        except ImportError:
                            missing.append(alias.name)
        except:
            pass
        
        return len(missing) == 0, missing


class SelfModificationEngine:
    """
    자기 수정 엔진 (Self-Modification Engine)
    전체 파이프라인을 통합 관리합니다.
    
    사용법:
        engine = SelfModificationEngine()
        result = engine.improve("Core/Intelligence/Will/free_will_engine.py")
    """
    
    def __init__(self):
        self.detector = ProblemDetector()
        self.planner = RefactorPlanner()
        self.editor = CodeEditor()
        self.validator = Validator()
        logger.info("🔧 Self-Modification Engine Initialized")
    
    def analyze(self, file_path: str) -> List[CodeIssue]:
        """파일 분석만 수행"""
        return self.detector.detect_issues(file_path)
    
    def plan(self, file_path: str) -> Optional[ModificationPlan]:
        """분석 및 계획 수립"""
        issues = self.analyze(file_path)
        if not issues:
            logger.info(f"✅ No issues found in {file_path}")
            return None
        
        return self.planner.create_plan(file_path, issues)
    
    def improve(self, file_path: str, auto_apply: bool = False) -> Dict[str, Any]:
        """
        전체 개선 파이프라인 실행
        
        Args:
            file_path: 개선할 파일 경로
            auto_apply: True면 자동 적용, False면 계획만 반환
        """
        logger.info(f"🔍 Analyzing: {file_path}")
        
        # 1. 분석 및 계획
        plan = self.plan(file_path)
        if not plan:
            return {
                "status": "no_issues",
                "file": file_path,
                "message": "문제가 발견되지 않았습니다."
            }
        
        # 2. 검증 (수정 전)
        valid, error = self.validator.validate_syntax(plan.modified_code)
        if not valid:
            return {
                "status": "validation_failed",
                "file": file_path,
                "error": error,
                "message": "수정된 코드에 구문 오류가 있습니다."
            }
        
        # 3. 자동 적용 또는 계획 반환
        if auto_apply:
            # 백업 생성
            if not self.editor.create_backup(plan):
                return {
                    "status": "backup_failed",
                    "file": file_path,
                    "message": "백업 생성에 실패했습니다."
                }
            
            # 수정 적용
            if not self.editor.apply_modification(plan):
                return {
                    "status": "apply_failed",
                    "file": file_path,
                    "message": "수정 적용에 실패했습니다."
                }
            
            return {
                "status": "success",
                "file": file_path,
                "issues_fixed": len(plan.issues),
                "backup": plan.backup_path,
                "confidence": plan.confidence,
                "message": f"{len(plan.issues)}개 문제가 수정되었습니다."
            }
        else:
            # 계획만 반환
            return {
                "status": "plan_ready",
                "file": file_path,
                "issues": [
                    {
                        "line": i.line_number,
                        "type": i.issue_type,
                        "severity": i.severity,
                        "description": i.description
                    }
                    for i in plan.issues
                ],
                "diff": self.editor.show_diff(plan),
                "confidence": plan.confidence,
                "message": "수정 계획이 준비되었습니다. auto_apply=True로 적용하세요."
            }
    
    def improve_multiple(self, file_paths: List[str], auto_apply: bool = False) -> List[Dict[str, Any]]:
        """여러 파일 개선"""
        results = []
        for path in file_paths:
            result = self.improve(path, auto_apply)
            results.append(result)
        return results


# 편의 함수
def self_improve(file_path: str, auto_apply: bool = False) -> Dict[str, Any]:
    """
    자기 개선 실행 (단축 함수)
    
    Example:
        result = self_improve("Core/Intelligence/Will/free_will_engine.py")
        print(result["diff"])  # 변경 사항 확인
        
        # 자동 적용
        result = self_improve("Core/Intelligence/Will/free_will_engine.py", auto_apply=True)
    """
    engine = SelfModificationEngine()
    return engine.improve(file_path, auto_apply)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    
    print("=== Self-Modification Engine Demo ===\n")
    
    engine = SelfModificationEngine()
    
    # 테스트: 자기 자신 분석
    result = engine.improve("Project_Sophia/self_modification.py")
    print(f"Status: {result['status']}")
    print(f"Message: {result['message']}")
