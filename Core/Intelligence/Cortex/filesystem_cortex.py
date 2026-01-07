"""
FileSystem Cortex (파일시스템 피질)
==================================

원본: Legacy/Project_Sophia/filesystem_cortex.py
마이그레이션: 2025-12-15

안전한 파일 조작을 위한 샌드박스 환경을 제공합니다.
루트 디렉토리 밖으로의 접근을 방지합니다.
"""
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional


@dataclass
class FSResult:
    ok: bool
    message: str
    path: Optional[str] = None
    data: Optional[str] = None


class FileSystemCortex:
    """
    Provides safe, sandboxed file manipulation confined to a root directory.
    All operations prevent path traversal attacks.
    """

    def __init__(self, root_dir: str = "data"):
        self.root = Path(root_dir).resolve()
        self.root.mkdir(parents=True, exist_ok=True)

    def _resolve(self, rel_path: str) -> Optional[Path]:
        """Resolves a relative path and ensures it's within the sandbox."""
        p = (self.root / Path(rel_path)).resolve()
        try:
            p.relative_to(self.root)
        except ValueError:
            return None
        return p

    def list_files(self, rel_dir: str = ".") -> FSResult:
        """Lists all files in a directory."""
        target = self._resolve(rel_dir)
        if target is None:
            return FSResult(False, "Access denied: outside root.")
        if not target.exists():
            return FSResult(False, f"Directory not found: {rel_dir}")
        if not target.is_dir():
            return FSResult(False, f"Not a directory: {rel_dir}")
        
        files: List[str] = []
        for p in sorted(target.rglob("*")):
            if p.is_file():
                files.append(str(p.relative_to(self.root)))
        return FSResult(True, "OK", data="\n".join(files))

    def read_file(self, rel_path: str, encoding: str = "utf-8") -> FSResult:
        """Reads a file's contents."""
        target = self._resolve(rel_path)
        if target is None:
            return FSResult(False, "Access denied: outside root.")
        if not target.exists() or not target.is_file():
            return FSResult(False, f"File not found: {rel_path}")
        try:
            text = target.read_text(encoding=encoding)
            return FSResult(True, "OK", path=str(target), data=text)
        except Exception as e:
            return FSResult(False, f"Read error: {e}")

    def write_file(self, rel_path: str, content: str, encoding: str = "utf-8") -> FSResult:
        """Writes content to a file."""
        target = self._resolve(rel_path)
        if target is None:
            return FSResult(False, "Access denied: outside root.")
        try:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding=encoding)
            return FSResult(True, "OK", path=str(target))
        except Exception as e:
            return FSResult(False, f"Write error: {e}")

    def delete_file(self, rel_path: str) -> FSResult:
        """Deletes a file."""
        target = self._resolve(rel_path)
        if target is None:
            return FSResult(False, "Access denied: outside root.")
        if not target.exists():
            return FSResult(False, f"File not found: {rel_path}")
        try:
            target.unlink()
            return FSResult(True, "OK", path=str(target))
        except Exception as e:
            return FSResult(False, f"Delete error: {e}")


# Singleton
_fs_cortex: Optional[FileSystemCortex] = None

def get_filesystem_cortex(root_dir: str = "data") -> FileSystemCortex:
    global _fs_cortex
    if _fs_cortex is None:
        _fs_cortex = FileSystemCortex(root_dir)
    return _fs_cortex
