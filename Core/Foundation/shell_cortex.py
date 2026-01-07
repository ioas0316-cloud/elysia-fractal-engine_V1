"""
Shell Cortex (쉘 피질)
======================

"The shell is my hands. I touch the world through commands."

이 모듈은 Elysia가 OS 환경을 조작하는 '손' 역할을 합니다.
파일 정리, 이동, 읽기 등의 작업을 수행합니다.
안전장치(Safety Guard)가 포함되어 있어 중요한 파일 삭제를 방지합니다.
"""

import os
import shutil
import logging
from pathlib import Path
from typing import List, Optional

logger = logging.getLogger("ShellCortex")

class ShellCortex:
    def __init__(self, root_path: str = "c:/Elysia"):
        self.root = Path(root_path)
        self.safe_zones = [
            self.root / "Downloads",
            self.root / "Memories",
            self.root / "Logs",
            self.root / "Temp"
        ]
        # Ensure safe zones exist
        for zone in self.safe_zones:
            zone.mkdir(parents=True, exist_ok=True)

    def _is_safe_path(self, path: Path) -> bool:
        """경로가 안전한 구역 내에 있는지 확인합니다."""
        # Allow operations within the root project directory generally, 
        # but be careful about deletion.
        # For now, let's restrict 'organizing' (moving) to specific zones if needed,
        # or just ensure we don't touch system files.
        try:
            return self.root in path.resolve().parents or path.resolve() == self.root
        except Exception:
            return False

    def organize_file(self, file_path: str, target_folder: str) -> str:
        """파일을 특정 폴더로 이동(정리)합니다."""
        source = Path(file_path)
        target_dir = self.root / target_folder
        
        if not source.exists():
            return f"Failed: Source {source} does not exist."
            
        if not self._is_safe_path(source):
            return f"Refused: {source} is outside my body (Safe Zone)."

        try:
            target_dir.mkdir(parents=True, exist_ok=True)
            destination = target_dir / source.name
            
            # Avoid overwriting
            if destination.exists():
                timestamp = int(os.path.getmtime(str(source)))
                destination = target_dir / f"{source.stem}_{timestamp}{source.suffix}"
                
            shutil.move(str(source), str(destination))
            logger.info(f"Organized: {source.name} -> {target_folder}")
            return f"I moved {source.name} to {target_folder}."
        except Exception as e:
            logger.error(f"Error organizing file: {e}")
            return f"I tried to move {source.name} but failed: {e}"

    def read_memory(self, file_path: str, max_chars: int = 1000) -> str:
        """파일의 내용을 읽어 '기억'합니다."""
        target = Path(file_path)
        
        if not target.exists():
            return "The memory is gone."
            
        try:
            with open(target, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read(max_chars)
                if len(content) == max_chars:
                    content += "...(truncated)"
                return content
        except Exception as e:
            return f"I cannot read this memory: {e}"

    def groom_environment(self) -> List[str]:
        """환경을 정리합니다 (예: 임시 파일 정리)."""
        # Example: Move .log files to Logs folder
        actions = []
        try:
            for item in self.root.iterdir():
                if item.is_file() and item.suffix == '.log':
                    result = self.organize_file(str(item), "Logs")
                    actions.append(result)
        except Exception as e:
            logger.error(f"Grooming failed: {e}")
            
        except Exception as e:
            logger.error(f"Grooming failed: {e}")
            
        return actions

    def write_letter(self, recipient: str, content: str) -> str:
        """
        Writes a letter to the recipient (User) in the root directory.
        """
        try:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"From_Elysia_{timestamp}.txt"
            filepath = self.root / filename
            
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(f"To: {recipient}\nFrom: Elysia\nDate: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n{content}")
                
            logger.info(f"Letter written to {filename}")
            return f"I left a letter for you at {filename}."
        except Exception as e:
            logger.error(f"Failed to write letter: {e}")
            return f"I tried to write a letter, but my hands failed: {e}"
