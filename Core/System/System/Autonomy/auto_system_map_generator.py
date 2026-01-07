"""
Auto System Map Generator (자동 시스템 맵 생성기)
=================================================

이 모듈은 SystemRegistry의 스캔 결과를 바탕으로
SYSTEM_MAP.md 문서를 자동으로 생성하거나 업데이트합니다.

핵심 기능:
- 실제 구조와 문서의 동기화
- 중복 감지 결과 포함
- 카테고리별 통계 생성

사용법:
    python auto_system_map_generator.py
"""

import os
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List

logger = logging.getLogger("Elysia.AutoMapGenerator")


class AutoSystemMapGenerator:
    """
    SystemRegistry와 연동하여 SYSTEM_MAP.md를 자동 생성
    """
    
    def __init__(self, output_path: str = None):
        self.output_path = output_path or "docs/SYSTEM_MAP.md"
        self.registry = None
        
    def _get_registry(self):
        """SystemRegistry 인스턴스 획득"""
        if self.registry is None:
            try:
                from Core.Foundation.System.system_registry import get_system_registry
                self.registry = get_system_registry()
            except ImportError as e:
                logger.error(f"SystemRegistry not available: {e}")
                return None
        return self.registry
        
    def generate(self) -> str:
        """
        SYSTEM_MAP.md 콘텐츠 생성
        
        Returns:
            생성된 마크다운 문자열
        """
        registry = self._get_registry()
        if registry is None:
            return "# Error: SystemRegistry not available"
        
        # 스캔 수행
        stats = registry.scan_all_systems()
        duplicates = registry.find_duplicates()
        
        # 카테고리 통계
        categories = {}
        for entry in registry.systems.values():
            cat = entry.category
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(entry)
        
        # 마크다운 생성
        md = self._build_markdown(stats, categories, duplicates)
        
        return md
        
    def _build_markdown(self, stats: Dict, categories: Dict, duplicates: Dict) -> str:
        """마크다운 문서 빌드"""
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        lines = [
            f"# Elysia System Map (자동 생성)",
            "",
            f"**자동 생성 시간**: {now}",
            f"**목적**: 실제 구조와 문서의 동기화",
            "",
            "> ⚠️ 이 문서는 `AutoSystemMapGenerator`에 의해 자동 생성됩니다.",
            "",
            "---",
            "",
            "## 📊 통계",
            "",
            f"| 항목 | 수치 |",
            f"|------|------|",
            f"| 총 파일 | {stats.get('total_files', 0)} |",
            f"| 총 클래스 | {stats.get('total_classes', 0)} |",
            f"| 카테고리 | {len(categories)} |",
            f"| 중복 클래스 | {len(duplicates)} |",
            "",
            "---",
            "",
            "## 📂 카테고리별 구조",
            "",
        ]
        
        # 카테고리별 섹션
        for cat_name, entries in sorted(categories.items(), key=lambda x: -len(x[1])):
            lines.append(f"### {cat_name.capitalize()} ({len(entries)} files)")
            lines.append("")
            lines.append("| 파일명 | 목적 | 상태 |")
            lines.append("|--------|------|------|")
            
            for entry in entries[:10]:  # 상위 10개만 표시
                purpose = entry.purpose[:50] + "..." if len(entry.purpose) > 50 else entry.purpose
                lines.append(f"| `{entry.name}` | {purpose} | {entry.status} |")
            
            if len(entries) > 10:
                lines.append(f"| ... | ({len(entries) - 10} more) | |")
            
            lines.append("")
        
        # 중복 섹션
        if duplicates:
            lines.extend([
                "---",
                "",
                "## ⚠️ 중복 감지",
                "",
                "| 클래스명 | 위치 수 | 파일들 |",
                "|----------|---------|--------|",
            ])
            
            for class_name, files in list(duplicates.items())[:15]:
                file_list = ", ".join(os.path.basename(f) for f in files[:3])
                if len(files) > 3:
                    file_list += f" (+{len(files)-3})"
                lines.append(f"| `{class_name}` | {len(files)} | {file_list} |")
            
            lines.append("")
        
        lines.extend([
            "---",
            "",
            f"*Auto-generated: {now}*",
        ])
        
        return "\n".join(lines)
        
    def save(self) -> str:
        """
        SYSTEM_MAP.md 생성 및 저장
        
        Returns:
            저장된 파일 경로
        """
        md_content = self.generate()
        
        # 디렉토리 생성
        output_path = Path(self.output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(md_content)
        
        logger.info(f"✅ SYSTEM_MAP.md saved to {output_path}")
        return str(output_path)
        

def sync_system_map():
    """
    편의 함수: 시스템 맵 동기화
    
    다른 모듈에서 호출하여 문서를 최신 상태로 유지
    """
    generator = AutoSystemMapGenerator()
    return generator.save()


if __name__ == "__main__":
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent.parent))
    
    logging.basicConfig(level=logging.INFO)
    
    generator = AutoSystemMapGenerator()
    content = generator.generate()
    print(content)
    
    # 저장 여부 확인
    if len(sys.argv) > 1 and sys.argv[1] == "--save":
        generator.save()
