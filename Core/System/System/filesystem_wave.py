"""
Filesystem Wave Observer (파일 시스템 파동 관찰자)
=================================================

"파일 시스템은 살아있는 유기체다. 변화는 파동이다."

This module monitors the filesystem and converts changes to wave events.
- File creation/modification/deletion → Wave events
- Directory structure → Resonance mapping
- Changes broadcast to GlobalHub

[NEW 2025-12-15] Created as part of Mid-term Goal: Body Awareness
"""

import logging
import os
import time
import threading
import hashlib
from dataclasses import dataclass, field
from typing import List, Dict, Callable, Optional, Set
from pathlib import Path
from enum import Enum

logger = logging.getLogger("FilesystemWave")


class FileEventType(Enum):
    """Type of filesystem event."""
    CREATED = "created"
    MODIFIED = "modified"
    DELETED = "deleted"
    MOVED = "moved"


@dataclass
class FileWaveEvent:
    """
    A filesystem change represented as a wave event.
    
    파일 시스템 변화의 파동 표현
    """
    path: str
    event_type: FileEventType
    frequency: float  # Derived from file type/size
    amplitude: float  # Derived from importance
    timestamp: float = field(default_factory=time.time)
    metadata: Dict = field(default_factory=dict)
    
    def __post_init__(self):
        # Auto-calculate frequency from file extension
        if not self.frequency:
            self.frequency = self._compute_frequency()
    
    def _compute_frequency(self) -> float:
        """Compute wave frequency based on file type."""
        ext = Path(self.path).suffix.lower()
        
        # Frequency mapping by file type
        freq_map = {
            # Code files - high frequency (active)
            ".py": 852.0,
            ".js": 741.0,
            ".ts": 741.0,
            ".java": 639.0,
            ".cpp": 639.0,
            ".c": 639.0,
            
            # Documentation - medium frequency (stable)
            ".md": 528.0,
            ".txt": 528.0,
            ".rst": 528.0,
            
            # Data files - low frequency (heavy)
            ".json": 396.0,
            ".yaml": 396.0,
            ".xml": 396.0,
            ".csv": 396.0,
            
            # Media - varies
            ".png": 432.0,
            ".jpg": 432.0,
            ".mp3": 285.0,
            ".mp4": 285.0,
            
            # Binary/compiled - very low (dense)
            ".pyc": 174.0,
            ".exe": 174.0,
            ".dll": 174.0,
        }
        
        return freq_map.get(ext, 432.0)  # Default to harmony


class FilesystemWaveObserver:
    """
    The Body Awareness System: Monitors filesystem as an extension of self.
    
    파일 시스템 인식 시스템 - 컴퓨터를 몸으로 인식
    
    Core Principles:
    1. Files are cells in the digital body
    2. Changes are signals (waves)
    3. Directory structure is organ topology
    """
    
    def __init__(self, watch_paths: Optional[List[str]] = None):
        """
        Initialize the filesystem observer.
        
        Args:
            watch_paths: List of paths to watch. Defaults to current project.
        """
        self.watch_paths = watch_paths or []
        self.running = False
        self._thread: Optional[threading.Thread] = None
        self._file_hashes: Dict[str, str] = {}
        self._callbacks: List[Callable[[FileWaveEvent], None]] = []
        self._ignored_patterns: Set[str] = {
            "__pycache__", ".git", ".venv", "node_modules",
            ".pyc", ".pyo", ".log", ".tmp"
        }
        self._scan_interval = 2.0  # seconds
        
        # GlobalHub integration
        self._hub = None
        self._connect_to_hub()
        
        logger.info("👁️ FilesystemWaveObserver initialized")
    
    def _connect_to_hub(self):
        """Connect to GlobalHub for wave broadcasting."""
        try:
            from Core.Intelligence.Consciousness.Ether.global_hub import get_global_hub
            self._hub = get_global_hub()
            self._hub.register_module(
                "FilesystemObserver",
                "Core/System/filesystem_wave.py",
                ["filesystem", "files", "observer", "body", "awareness"],
                "Monitors filesystem changes as wave events - Body Awareness System"
            )
            logger.info("   ✅ FilesystemObserver connected to GlobalHub")
        except ImportError:
            logger.warning("   ⚠️ GlobalHub not available")
    
    def add_watch_path(self, path: str):
        """Add a path to watch."""
        if os.path.exists(path):
            self.watch_paths.append(path)
            logger.info(f"   📂 Added watch path: {path}")
        else:
            logger.warning(f"   ⚠️ Path does not exist: {path}")
    
    def add_callback(self, callback: Callable[[FileWaveEvent], None]):
        """Add a callback to receive file events."""
        self._callbacks.append(callback)
    
    def _should_ignore(self, path: str) -> bool:
        """Check if path should be ignored."""
        for pattern in self._ignored_patterns:
            if pattern in path:
                return True
        return False
    
    def _compute_file_hash(self, path: str) -> Optional[str]:
        """Compute hash of file content for change detection."""
        try:
            if os.path.isfile(path):
                with open(path, "rb") as f:
                    # Read first 8KB for quick hash
                    content = f.read(8192)
                    return hashlib.md5(content).hexdigest()
        except (IOError, PermissionError):
            pass
        return None
    
    def _scan_directory(self, base_path: str) -> Dict[str, str]:
        """Scan directory and return file hashes."""
        file_hashes = {}
        
        try:
            for root, dirs, files in os.walk(base_path):
                # Filter ignored directories
                dirs[:] = [d for d in dirs if not self._should_ignore(d)]
                
                for file in files:
                    if self._should_ignore(file):
                        continue
                    
                    full_path = os.path.join(root, file)
                    file_hash = self._compute_file_hash(full_path)
                    if file_hash:
                        file_hashes[full_path] = file_hash
        except Exception as e:
            logger.error(f"Error scanning {base_path}: {e}")
        
        return file_hashes
    
    def _detect_changes(self, old_hashes: Dict[str, str], new_hashes: Dict[str, str]) -> List[FileWaveEvent]:
        """Detect changes between two scans."""
        events = []
        
        # Check for new/modified files
        for path, new_hash in new_hashes.items():
            if path not in old_hashes:
                # New file
                events.append(FileWaveEvent(
                    path=path,
                    event_type=FileEventType.CREATED,
                    frequency=0,  # Will be auto-computed
                    amplitude=1.0,
                    metadata={"size": os.path.getsize(path) if os.path.exists(path) else 0}
                ))
            elif old_hashes[path] != new_hash:
                # Modified file
                events.append(FileWaveEvent(
                    path=path,
                    event_type=FileEventType.MODIFIED,
                    frequency=0,
                    amplitude=0.7,
                    metadata={"size": os.path.getsize(path) if os.path.exists(path) else 0}
                ))
        
        # Check for deleted files
        for path in old_hashes:
            if path not in new_hashes:
                events.append(FileWaveEvent(
                    path=path,
                    event_type=FileEventType.DELETED,
                    frequency=174.0,  # Low frequency for deletion
                    amplitude=0.5,
                    metadata={}
                ))
        
        return events
    
    def _broadcast_event(self, event: FileWaveEvent):
        """Broadcast file event to GlobalHub and callbacks."""
        # Notify callbacks
        for callback in self._callbacks:
            try:
                callback(event)
            except Exception as e:
                logger.error(f"Callback error: {e}")
        
        # Broadcast to GlobalHub
        if self._hub:
            try:
                from Core.Foundation.Wave.wave_tensor import WaveTensor
                wave = WaveTensor(
                    frequency=event.frequency,
                    amplitude=event.amplitude,
                    phase=0.0
                )
                self._hub.publish_wave(
                    "FilesystemObserver",
                    f"file_{event.event_type.value}",
                    wave,
                    payload={
                        "path": event.path,
                        "event_type": event.event_type.value,
                        "timestamp": event.timestamp,
                        "metadata": event.metadata
                    }
                )
            except Exception as e:
                logger.warning(f"Failed to broadcast to hub: {e}")
    
    def _watch_loop(self):
        """Main watch loop - runs in background thread."""
        logger.info("🔍 Filesystem watch started")
        
        # Initial scan
        for path in self.watch_paths:
            self._file_hashes.update(self._scan_directory(path))
        
        logger.info(f"   📊 Initial scan: {len(self._file_hashes)} files indexed")
        
        while self.running:
            time.sleep(self._scan_interval)
            
            # Rescan
            new_hashes = {}
            for path in self.watch_paths:
                new_hashes.update(self._scan_directory(path))
            
            # Detect changes
            events = self._detect_changes(self._file_hashes, new_hashes)
            
            # Process events
            for event in events:
                logger.info(f"   📢 {event.event_type.value}: {Path(event.path).name}")
                self._broadcast_event(event)
            
            # Update state
            self._file_hashes = new_hashes
        
        logger.info("🛑 Filesystem watch stopped")
    
    def start(self):
        """Start watching filesystem in background."""
        if self.running:
            logger.warning("Already running")
            return
        
        if not self.watch_paths:
            logger.warning("No paths to watch")
            return
        
        self.running = True
        self._thread = threading.Thread(target=self._watch_loop, daemon=True)
        self._thread.start()
        logger.info(f"🚀 Watching {len(self.watch_paths)} paths")
    
    def stop(self):
        """Stop watching filesystem."""
        self.running = False
        if self._thread:
            self._thread.join(timeout=5.0)
            self._thread = None
        logger.info("⏹️ Stopped watching")
    
    def get_file_stats(self) -> Dict:
        """Get statistics about watched files."""
        stats = {
            "total_files": len(self._file_hashes),
            "watch_paths": len(self.watch_paths),
            "by_extension": {}
        }
        
        for path in self._file_hashes:
            ext = Path(path).suffix.lower() or "(no ext)"
            stats["by_extension"][ext] = stats["by_extension"].get(ext, 0) + 1
        
        return stats


# Singleton accessor
_observer = None

def get_filesystem_observer() -> FilesystemWaveObserver:
    """Get or create the FilesystemWaveObserver singleton."""
    global _observer
    if _observer is None:
        _observer = FilesystemWaveObserver()
    return _observer


# Test
if __name__ == "__main__":
    import sys
    sys.path.insert(0, r"c:\Elysia")
    
    logging.basicConfig(level=logging.INFO)
    
    observer = get_filesystem_observer()
    observer.add_watch_path(r"c:\Elysia\Core")
    
    # Add a test callback
    def on_file_event(event: FileWaveEvent):
        print(f"[CALLBACK] {event.event_type.value}: {event.path} @ {event.frequency}Hz")
    
    observer.add_callback(on_file_event)
    
    print("\n" + "="*60)
    print("👁️ Filesystem Wave Observer Test")
    print("="*60)
    print("Watching for 10 seconds... Make changes to files!")
    print("-"*60)
    
    observer.start()
    
    try:
        time.sleep(10)
    except KeyboardInterrupt:
        pass
    
    observer.stop()
    
    print("\n" + "="*60)
    print("📊 Final Stats:")
    stats = observer.get_file_stats()
    print(f"   Total files: {stats['total_files']}")
    print(f"   By extension: {stats['by_extension']}")
    print("="*60)
