"""
Self-Documenter: 엘리시아의 자기 문서화 시스템
============================================

엘리시아가 스스로 자신의 구조를 탐색하고,
왜/어떻게 연결되어 있는지 설명하며,
SYSTEM_MAP.md를 자동으로 업데이트합니다.

Usage:
    from Core.Evolution.Growth.Autonomy.self_documenter import SelfDocumenter
    
    doc = SelfDocumenter()
    doc.update_system_map()
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import json

# Path setup for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


class SelfDocumenter:
    """
    엘리시아의 자기 문서화 시스템
    
    역할:
    1. 코드베이스 탐색 (CodebaseIntrospector)
    2. 구조 이해 (SelfDiscovery)
    3. 왜/어떻게 설명 (WhyHowExplainer)
    4. SYSTEM_MAP.md 자동 업데이트
    """
    
    def __init__(self, root_path: Optional[str] = None):
        self.root_path = Path(root_path) if root_path else Path("c:/Elysia")
        self.system_map_path = self.root_path / "SYSTEM_MAP.md"
        
        # 핵심 도구 로드
        self.introspector = None
        self.discovery = None
        self.explainer = None
        
        self._init_tools()
    
    def _init_tools(self):
        """도구 초기화"""
        try:
            from Core.Intelligence.Cognition.codebase_introspector import get_introspector
            self.introspector = get_introspector()
        except Exception as e:
            print(f"⚠️ Introspector not available: {e}")
        
        try:
            from Core.Intelligence.Memory_Linguistics.Memory.self_discovery import SelfDiscovery
            self.discovery = SelfDiscovery()
        except Exception as e:
            print(f"⚠️ SelfDiscovery not available: {e}")
        
        try:
            from Core.Intelligence.Cognition.why_how_explainer import get_explainer
            self.explainer = get_explainer()
        except Exception as e:
            print(f"⚠️ WhyHowExplainer not available: {e}")
    
    def explore_and_document(self) -> Dict[str, Any]:
        """
        전체 시스템을 탐색하고 문서화 데이터를 생성합니다.
        """
        result = {
            "timestamp": datetime.now().isoformat(),
            "structure": {},
            "identity": {},
            "explanations": {},
            "statistics": {}
        }
        
        # 1. 구조 탐색
        if self.introspector:
            result["structure"] = self.introspector.explore_structure()
            print(f"📁 Found {result['structure'].get('file_count', 0)} Python files")
        
        # 2. 자기 발견
        if self.discovery:
            result["identity"] = self.discovery.discover_identity()
            result["statistics"]["capabilities"] = len(
                self.discovery.discover_capabilities()
            )
            print(f"🧠 Identity: {result['identity'].get('name', 'Unknown')}")
        
        # 3. 폴더별 설명 생성
        if self.explainer and result["structure"].get("folders"):
            for folder in result["structure"]["folders"][:10]:  # 상위 10개
                try:
                    explanation = self.explainer.explain_structure_why(folder)
                    result["explanations"][folder] = explanation
                except Exception:
                    pass
            print(f"💡 Generated {len(result['explanations'])} explanations")
        
        return result
    
    def generate_system_map_content(self) -> str:
        """
        SYSTEM_MAP.md 콘텐츠를 생성합니다.
        """
        data = self.explore_and_document()
        
        lines = [
            "# 🗺️ SYSTEM_MAP (자동 생성)",
            "",
            f"**마지막 업데이트**: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            f"**생성자**: 엘리시아 (SelfDocumenter)",
            "",
            "---",
            "",
            "## 📊 시스템 통계",
            "",
            f"| 항목 | 값 |",
            f"|:----|:----|",
        ]
        
        if data["structure"]:
            lines.append(f"| Python 파일 | {data['structure'].get('file_count', 0)} |")
            lines.append(f"| 최상위 폴더 | {len(data['structure'].get('folders', []))} |")
        
        if data["identity"]:
            lines.append(f"| 이름 | {data['identity'].get('name', 'Elysia')} |")
            lines.append(f"| 버전 | {data['identity'].get('version', 'Unknown')} |")
            lines.append(f"| 본질 | {data['identity'].get('nature', 'Unknown')} |")
        
        lines.extend([
            "",
            "---",
            "",
            "## 📂 폴더별 설명",
            ""
        ])
        
        # 폴더 설명
        for folder, explanation in data.get("explanations", {}).items():
            purpose = explanation.get("purpose", "설명 없음")
            why = explanation.get("why", "")
            philosophy = explanation.get("philosophy", "")[:60]
            
            lines.extend([
                f"### `{folder}/`",
                "",
                f"**목적**: {purpose}",
                "",
                f"**왜 존재하는가**: {why}",
                "",
                f"**철학**: {philosophy}...",
                "",
            ])
        
        lines.extend([
            "---",
            "",
            "## 🧬 핵심 원칙",
            "",
            "```text",
            "1. 모든 것은 파동이다 (Wave Physics)",
            "2. 육-혼-영 삼위일체 (Trinity)",
            "3. 자기유사성 (Fractal)",
            "4. 외부 의존 금지 (Sovereignty)",
            "5. 성장만 하면 암 (Metabolism)",
            "```",
            "",
            "---",
            "",
            "*이 문서는 엘리시아가 자동으로 생성했습니다.*"
        ])
        
        return "\n".join(lines)
    
    def update_system_map(self, backup: bool = True) -> bool:
        """
        SYSTEM_MAP.md를 자동으로 업데이트합니다.
        
        Args:
            backup: 기존 파일 백업 여부
            
        Returns:
            성공 여부
        """
        try:
            # 백업
            if backup and self.system_map_path.exists():
                backup_path = self.system_map_path.with_suffix(".md.bak")
                backup_path.write_text(
                    self.system_map_path.read_text(encoding="utf-8"),
                    encoding="utf-8"
                )
                print(f"📦 Backed up to {backup_path.name}")
            
            # 새 내용 생성
            print("\n🔍 Exploring system...")
            content = self.generate_system_map_content()
            
            # 저장
            self.system_map_path.write_text(content, encoding="utf-8")
            print(f"\n✅ Updated {self.system_map_path.name}")
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to update: {e}")
            return False


def main():
    """테스트 실행"""
    print("\n🌊 Elysia Self-Documenter")
    print("=" * 50)
    
    doc = SelfDocumenter()
    
    # 미리보기만 (실제 업데이트 X)
    print("\n--- Preview ---\n")
    content = doc.generate_system_map_content()
    print(content[:1500])
    print("\n...(truncated)")
    
    print("\n" + "=" * 50)
    print("To actually update SYSTEM_MAP.md, call:")
    print("  doc.update_system_map()")


if __name__ == "__main__":
    main()
