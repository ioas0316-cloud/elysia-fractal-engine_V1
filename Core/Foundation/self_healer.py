"""
Elysia Self-Healer
==================
공명 기반 자가 치유 시스템.
깨진 모듈이 활성 모듈의 패턴을 학습하여 스스로 치유.

엘리시아에게 시간은 무한한 자원.
"""

import sys
import os
import re
import time
import shutil
from pathlib import Path
from typing import Set, Dict, List, Tuple

class SelfHealer:
    """
    공명 기반 자가 치유.
    활성 모듈의 import 패턴을 학습하고,
    깨진 모듈에 적용하여 치유.
    """
    
    def __init__(self, evolution_path: str = "Core/Evolution"):
        self.evolution_path = Path(evolution_path)
        self.base_paths = [
            evolution_path,
            f"{evolution_path}/architecture",
            f"{evolution_path}/high_engine",
            "Legacy/Project_Sophia/core",
            "Legacy/Project_Elysia/mechanics",
            "Legacy/Project_Elysia",
            "Tools",
        ]
        
        # 치유 패턴 (학습됨)
        self.healing_patterns: Dict[str, str] = {}
        
        # 상태
        self.cycles = 0
        self.total_healed = 0
        
    def setup_paths(self):
        """Python 경로 설정"""
        for p in self.base_paths:
            if p not in sys.path:
                sys.path.insert(0, p)
    
    def get_status(self) -> Tuple[int, int, List[Tuple[str, str]]]:
        """현재 상태: (total, active, broken_list)"""
        self.setup_paths()
        
        total = 0
        active = 0
        broken = []
        
        for f in self.evolution_path.glob("*.py"):
            if f.name.startswith("__"):
                continue
            
            total += 1
            name = f.stem
            
            try:
                if name in sys.modules:
                    del sys.modules[name]
                __import__(name)
                active += 1
            except Exception as e:
                broken.append((name, str(e)))
        
        return total, active, broken
    
    def learn_patterns(self, broken_errors: List[Tuple[str, str]]):
        """깨진 모듈의 에러에서 패턴 학습"""
        for name, error in broken_errors:
            # "No module named 'X'" 패턴
            match = re.search(r"No module named '([\w.]+)'", error)
            if match:
                missing = match.group(1)
                
                # 해결책 찾기
                if '.' in missing:
                    # from A.B.C → from C
                    parts = missing.split('.')
                    self.healing_patterns[f"from {missing}"] = f"from {parts[-1]}"
                else:
                    # 모듈 찾아서 복사 시도
                    self._find_and_migrate(missing)
    
    def _find_and_migrate(self, module_name: str):
        """누락된 모듈 찾아서 마이그레이션"""
        for root, dirs, files in os.walk("c:\\Elysia"):
            if "__pycache__" in root or ".git" in root:
                continue
            
            for f in files:
                if f == f"{module_name}.py":
                    src = Path(root) / f
                    dest = self.evolution_path / f
                    
                    if not dest.exists():
                        shutil.copy2(src, dest)
                        print(f"  ↳ Migrated: {module_name}")
                    return
    
    def apply_healing(self):
        """학습된 패턴 적용"""
        if not self.healing_patterns:
            return
        
        for filepath in self.evolution_path.rglob("*.py"):
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                code = f.read()
            
            original = code
            
            for old, new in self.healing_patterns.items():
                code = code.replace(old, new)
            
            # 상대 import 제거
            code = re.sub(r'from \.+(\w+)', r'from \1', code)
            
            if code != original:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(code)
    
    def heal_cycle(self) -> Tuple[int, int]:
        """한 치유 사이클 실행. (active, total) 반환"""
        self.cycles += 1
        
        total, active_before, broken = self.get_status()
        
        if not broken:
            return active_before, total
        
        # 패턴 학습
        self.learn_patterns(broken)
        
        # 치유 적용
        self.apply_healing()
        
        # 결과 확인
        total, active_after, _ = self.get_status()
        
        healed = active_after - active_before
        self.total_healed += max(0, healed)
        
        return active_after, total
    
    def run(self, max_cycles: int = 100, target_percent: float = 95.0):
        """
        목표 활성화율에 도달할 때까지 치유 사이클 실행.
        
        엘리시아의 주관 시간에서는 이게 순식간.
        """
        print("="*60)
        print("Elysia Self-Healing System")
        print("공명 기반 자가 치유 시작")
        print("="*60)
        print()
        
        start_time = time.time()
        
        for cycle in range(max_cycles):
            active, total = self.heal_cycle()
            percent = (active * 100 / total) if total > 0 else 0
            
            # 진행 표시
            bar = "█" * int(percent / 5) + "░" * (20 - int(percent / 5))
            print(f"\rCycle {cycle+1}: [{bar}] {percent:.1f}% ({active}/{total})", end="")
            
            if percent >= target_percent:
                print()
                print(f"\n✓ Target reached: {percent:.1f}%")
                break
            
            # 진전이 없으면 (5사이클 연속) 중단
            if cycle > 5 and self.total_healed == 0:
                print()
                print(f"\n→ Stabilized at {percent:.1f}%")
                break
        
        elapsed = time.time() - start_time
        
        print()
        print("="*60)
        print(f"Healing complete")
        print(f"  Cycles: {self.cycles}")
        print(f"  Time: {elapsed:.2f}s (주관시간: 무한)")
        print(f"  Active: {active}/{total} ({percent:.1f}%)")
        print("="*60)
        
        return active, total


def main():
    """자가 치유 실행"""
    healer = SelfHealer()
    healer.run(max_cycles=50, target_percent=90.0)


if __name__ == "__main__":
    main()
