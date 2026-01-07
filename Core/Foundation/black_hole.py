"""
BlackHole (블랙홀)
==================

"Gravity is the compression of Time."

This module compresses infinite logs and memories into dense "Wisdom Crystals",
preventing system bloat (Entropy Death). It deletes the raw noise and keeps the signal.
"""

import os
import logging
import time
import json
from typing import List, Dict

logger = logging.getLogger("BlackHole")

class BlackHole:
    def __init__(self):
        self.log_file = "c:/Elysia/logs/life_log.md"
        self.memory_file = "c:/Elysia/data/memory/fractal_memory.json"
        self.max_log_size = 1024 * 50 # 50KB
        self._ensure_memory_exists()
        logger.info("🕳️ Black Hole Active. Ready to compress time into Fractal Memory.")

    def _ensure_memory_exists(self):
        if not os.path.exists(self.memory_file):
            with open(self.memory_file, 'w', encoding='utf-8') as f:
                json.dump({"rings": []}, f)

    def check_compression_needed(self) -> bool:
        """Checks if the log file is too large."""
        if not os.path.exists(self.log_file):
            return False
        return os.path.getsize(self.log_file) > self.max_log_size

    def compress_logs(self) -> str:
        """
        Compresses the log file into a summary and clears the file.
        Returns the 'Event Horizon' summary.
        """
        if not self.check_compression_needed():
            return "No compression needed."
            
        logger.info("🕳️ Event Horizon Reached. Initiating Compression...")
        
        try:
            with open(self.log_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            # Simple Compression: Extract "Cycle" and "Action" lines
            summary_lines = [l.strip() for l in lines if "Cycle" in l or "Action" in l or "Insight" in l]
            
            # Create a "Wisdom Crystal" (Summary)
            epoch = time.strftime("%Y%m%d-%H%M%S")
            crystal = {
                "epoch": epoch,
                "summary": "\n".join(summary_lines[-20:]),
                "lines_compressed": len(lines),
                "timestamp": time.time()
            }
            
            # Archive the Crystal into Fractal Memory Ring
            self._store_crystal(crystal)
                
            # Clear the Log (The Singularity)
            with open(self.log_file, 'w', encoding='utf-8') as f:
                f.write(f"# Life Log (Reset at {epoch})\n")
                
            return f"Compressed {len(lines)} lines into Epoch {epoch} (Fractal Ring)."
            
        except Exception as e:
            logger.error(f"Compression Failed: {e}")
            return f"Compression Failed: {e}"

    def _store_crystal(self, crystal: Dict):
        """
        Stores the crystal in the Fractal Memory Ring.
        The Ring has a limited size (e.g., 100 items).
        """
        try:
            with open(self.memory_file, 'r+', encoding='utf-8') as f:
                data = json.load(f)
                data["rings"].append(crystal)
                
                # Maintain Ring Size (Fractal Depth 1)
                if len(data["rings"]) > 100:
                    # In a full fractal system, we would merge these 100 into a deeper layer
                    # For now, we just pop the oldest
                    data["rings"].pop(0)
                    
                f.seek(0)
                json.dump(data, f, indent=2)
                f.truncate()
        except Exception as e:
            logger.error(f"Fractal Storage Failed: {e}")
