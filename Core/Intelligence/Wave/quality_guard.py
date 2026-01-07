"""
Wave Quality Guard (파동 품질 경비)
===================================

자동 공명 탐지, Tension 경보, 품질 검사를 수행합니다.

Usage:
    # CLI로 실행
    python -m Core.Wave.quality_guard --check path/to/file.py
    python -m Core.Wave.quality_guard --scan Core/
    
    # 코드에서 사용
    from Core.Intelligence.Physics_Waves.Wave.quality_guard import WaveQualityGuard
    guard = WaveQualityGuard()
    report = guard.scan_directory("Core/Intelligence")
"""

import os
import sys
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("WaveQualityGuard")

# 임포트
try:
    from Core.Intelligence.Intelligence.wave_coding_system import get_wave_coding_system, CodeWave
    WAVE_AVAILABLE = True
except ImportError:
    WAVE_AVAILABLE = False
    logger.warning("⚠️ WaveCodingSystem not available")


@dataclass
class QualityIssue:
    """품질 문제"""
    file: str
    issue_type: str  # "high_complexity", "duplicate", "high_tension"
    severity: str    # "warning", "error", "critical"
    message: str
    value: float = 0.0
    suggestion: str = ""


@dataclass
class QualityReport:
    """품질 검사 보고서"""
    timestamp: str
    files_scanned: int
    issues: List[QualityIssue] = field(default_factory=list)
    duplicates: List[Tuple[str, str, float]] = field(default_factory=list)
    summary: Dict[str, int] = field(default_factory=dict)
    
    def has_errors(self) -> bool:
        return any(i.severity in ["error", "critical"] for i in self.issues)
    
    def to_markdown(self) -> str:
        """마크다운 형식 보고서"""
        md = f"# 파동 품질 검사 보고서\n\n"
        md += f"**검사 시간**: {self.timestamp}\n"
        md += f"**검사 파일 수**: {self.files_scanned}\n\n"
        
        # 요약
        md += "## 요약\n\n"
        md += f"- ⚠️ 경고: {self.summary.get('warning', 0)}\n"
        md += f"- ❌ 오류: {self.summary.get('error', 0)}\n"
        md += f"- 🔴 치명적: {self.summary.get('critical', 0)}\n"
        md += f"- 🔗 중복 후보: {len(self.duplicates)}\n\n"
        
        # 이슈 목록
        if self.issues:
            md += "## 발견된 문제\n\n"
            md += "| 파일 | 유형 | 심각도 | 값 | 메시지 |\n"
            md += "|------|------|--------|-----|--------|\n"
            for issue in self.issues[:20]:  # 최대 20개
                icon = {"warning": "⚠️", "error": "❌", "critical": "🔴"}.get(issue.severity, "")
                md += f"| {issue.file} | {issue.issue_type} | {icon} | {issue.value:.1f} | {issue.message} |\n"
        
        # 중복
        if self.duplicates:
            md += "\n## 중복 후보 (공명도 > 80%)\n\n"
            for f1, f2, res in self.duplicates[:10]:
                md += f"- `{f1}` ↔ `{f2}`: **{res:.0%}**\n"
        
        return md


class WaveQualityGuard:
    """
    파동 품질 경비
    
    자동으로 코드 품질 문제를 탐지합니다:
    - 복잡도 임계값 초과 (Frequency > 50)
    - 중복 코드 (Resonance > 80%)
    - 고긴장 코드 (Tension > 0.7)
    """
    
    # 임계값 설정
    COMPLEXITY_WARNING = 30.0
    COMPLEXITY_ERROR = 50.0
    COMPLEXITY_CRITICAL = 80.0
    
    RESONANCE_DUPLICATE = 0.80
    
    def __init__(self):
        if WAVE_AVAILABLE:
            self.wave_system = get_wave_coding_system()
        else:
            self.wave_system = None
        self.waves: Dict[str, CodeWave] = {}
    
    def check_file(self, filepath: str) -> List[QualityIssue]:
        """단일 파일 검사"""
        issues = []
        
        if not WAVE_AVAILABLE:
            return [QualityIssue(
                file=filepath,
                issue_type="system_error",
                severity="error",
                message="WaveCodingSystem not available"
            )]
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                code = f.read()
        except Exception as e:
            return [QualityIssue(
                file=filepath,
                issue_type="read_error",
                severity="warning",
                message=str(e)
            )]
        
        # 파동 변환
        wave = self.wave_system.code_to_wave(code, filepath)
        self.waves[filepath] = wave
        
        # 복잡도 검사
        if wave.frequency >= self.COMPLEXITY_CRITICAL:
            issues.append(QualityIssue(
                file=filepath,
                issue_type="high_complexity",
                severity="critical",
                message=f"매우 높은 복잡도! 즉시 리팩토링 필요",
                value=wave.frequency,
                suggestion="파일을 여러 모듈로 분리하세요"
            ))
        elif wave.frequency >= self.COMPLEXITY_ERROR:
            issues.append(QualityIssue(
                file=filepath,
                issue_type="high_complexity",
                severity="error",
                message=f"복잡도가 높습니다. 리팩토링 권장",
                value=wave.frequency,
                suggestion="긴 함수를 분리하세요"
            ))
        elif wave.frequency >= self.COMPLEXITY_WARNING:
            issues.append(QualityIssue(
                file=filepath,
                issue_type="high_complexity",
                severity="warning",
                message=f"복잡도 주의",
                value=wave.frequency
            ))
        
        return issues
    
    def scan_directory(self, directory: str, pattern: str = "*.py") -> QualityReport:
        """디렉토리 전체 스캔"""
        report = QualityReport(
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            files_scanned=0
        )
        
        path = Path(directory)
        if not path.exists():
            logger.error(f"Directory not found: {directory}")
            return report
        
        # 파일 스캔
        py_files = list(path.rglob(pattern))
        report.files_scanned = len(py_files)
        
        logger.info(f"🔍 Scanning {len(py_files)} files in {directory}...")
        
        for py_file in py_files:
            rel_path = str(py_file.relative_to(path.parent))
            issues = self.check_file(str(py_file))
            report.issues.extend(issues)
        
        # 공명 탐지 (중복 후보)
        report.duplicates = self._detect_duplicates()
        
        # 요약 계산
        report.summary = {
            "warning": sum(1 for i in report.issues if i.severity == "warning"),
            "error": sum(1 for i in report.issues if i.severity == "error"),
            "critical": sum(1 for i in report.issues if i.severity == "critical"),
        }
        
        logger.info(f"✅ Scan complete: {len(report.issues)} issues, {len(report.duplicates)} duplicates")
        
        return report
    
    def _detect_duplicates(self) -> List[Tuple[str, str, float]]:
        """중복 코드 탐지 (공명 기반)"""
        duplicates = []
        
        files = list(self.waves.keys())
        for i, f1 in enumerate(files):
            for f2 in files[i+1:]:
                w1, w2 = self.waves[f1], self.waves[f2]
                resonance = w1.resonate_with(w2)
                
                if resonance >= self.RESONANCE_DUPLICATE:
                    duplicates.append((
                        os.path.basename(f1),
                        os.path.basename(f2),
                        resonance
                    ))
        
        # 정렬
        duplicates.sort(key=lambda x: x[2], reverse=True)
        return duplicates
    
    def get_tension_alerts(self) -> List[QualityIssue]:
        """고긴장 코드 경보"""
        alerts = []
        
        for filepath, wave in self.waves.items():
            # Tension = complexity / 50 (from wave_coder.py)
            tension = min(1.0, wave.frequency / 50.0)
            
            if tension > 0.7:
                alerts.append(QualityIssue(
                    file=filepath,
                    issue_type="high_tension",
                    severity="warning",
                    message=f"코드 긴장도가 높음 (Tension={tension:.2f})",
                    value=tension,
                    suggestion="분기문이나 중첩을 줄이세요"
                ))
        
        return alerts


def main():
    """CLI 진입점"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Wave Quality Guard")
    parser.add_argument("--check", type=str, help="Check single file")
    parser.add_argument("--scan", type=str, help="Scan directory")
    parser.add_argument("--output", type=str, help="Output report file")
    parser.add_argument("--ci", action="store_true", help="CI mode (exit 1 on errors)")
    
    args = parser.parse_args()
    
    guard = WaveQualityGuard()
    
    if args.check:
        issues = guard.check_file(args.check)
        for issue in issues:
            print(f"[{issue.severity.upper()}] {issue.file}: {issue.message}")
        
    elif args.scan:
        report = guard.scan_directory(args.scan)
        
        # Tension 경보 추가
        tension_alerts = guard.get_tension_alerts()
        report.issues.extend(tension_alerts)
        
        # 출력
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(report.to_markdown())
            print(f"📄 Report saved to {args.output}")
        else:
            print(report.to_markdown())
        
        # CI 모드
        if args.ci and report.has_errors():
            print("\n❌ CI Check Failed: Errors found!")
            sys.exit(1)
        elif args.ci:
            print("\n✅ CI Check Passed!")
            sys.exit(0)
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
