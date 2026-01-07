"""
Knowledge Migrator (The Hands of Order)
=======================================
"Entropy is natural, but Intelligence is the organization of Entropy."

This module autonomously scans the environment for "scattered" knowledge 
(orphaned files, unorganized notes) and integrates them into the 
Hierarchical Knowledge Graph, ensuring Elysia's mind remains coherent.

Mechanism:
1. Scan: Look for .txt/.md files in root or specific directories.
2. Read: Extract content.
3. Understand: Use ReasoningEngine to classify Domain and Purpose.
4. Absorb: Feed into ResonanceLearner/InternalUniverse.
5. Archive: Move processed files to 'data/archived_knowledge/'.
"""

import os
import shutil
import logging
import datetime
from typing import List, Optional, Any

from elysia_core import Cell, Organ

@Cell("KnowledgeMigrator", category="Learning")
class KnowledgeMigrator:
    """
    Autonomous Knowledge Digestion System.
    """
    
    def __init__(self, root_path: str = "c:/Elysia"):
        self.logger = logging.getLogger("Elysia.KnowledgeMigrator")
        self.root_path = root_path
        self.archive_path = os.path.join(root_path, "data/archived_knowledge")
        self.ignore_dirs = {".git", ".gemini", "Core", "data", "venv", "__pycache__", "scripts", "docs"}
        
        # Ensure archive exists
        os.makedirs(self.archive_path, exist_ok=True)

    def _get_resonance_learner(self):
        try:
            return Organ.get("ResonanceLearner")
        except:
            from Core.Intelligence.Cognition.Learning.resonance_learner import ResonanceLearner
            return ResonanceLearner()

    def scan_and_migrate(self):
        """
        Main Routine: Scan -> Ingest -> Archive.
        """
        self.logger.info("🧹 Initiating Knowledge Migration Sequence...")
        
        candidates = self._scan_for_scattered_files()
        
        if not candidates:
            self.logger.info("✨ Workspace is clean. No scattered knowledge found.")
            return

        self.logger.info(f"📂 Found {len(candidates)} scattered files. Beginning integration.")
        
        learner = self._get_resonance_learner()
        universe = learner._get_internal_universe() # Access via learner for consistency
        
        for file_path in candidates:
            try:
                self._process_file(file_path, universe)
            except Exception as e:
                self.logger.error(f"❌ Failed to process '{file_path}': {e}")

    def _scan_for_scattered_files(self) -> List[str]:
        """
        Finds .txt or .md files in the root directory (excluding system dirs).
        """
        candidates = []
        try:
            # We only scan the ROOT level for now to avoid messing up project structure recursively
            with os.scandir(self.root_path) as entries:
                for entry in entries:
                    if entry.is_file() and entry.name.endswith((".txt", ".md")):
                        # Check ignore list (files)
                        if entry.name in ["task.md", "README.md", "SYSTEM_MAP.md", "AGENT_GUIDE.md"]:
                            continue
                        candidates.append(entry.path)
            
            # Use 'reading_room' if it exists (Convention)
            reading_room = os.path.join(self.root_path, "reading_room")
            if os.path.exists(reading_room):
                 with os.scandir(reading_room) as entries:
                    for entry in entries:
                         if entry.is_file() and entry.name.endswith((".txt", ".md")):
                             candidates.append(entry.path)
                             
        except Exception as e:
            self.logger.error(f"Scan failed: {e}")
            
        return candidates

    def _process_file(self, file_path: str, universe: Any):
        """
        Ingests a single file.
        """
        filename = os.path.basename(file_path)
        self.logger.info(f"📖 Reading '{filename}'...")
        
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        if not content.strip():
            self.logger.warning(f"⚠️ File '{filename}' is empty. Skipping.")
            return

        # 1. Absorb into Universe
        # We treat the filename as the Concept Name initially
        concept_name = os.path.splitext(filename)[0]
        self.logger.info(f"   🧠 Absorbing concept: '{concept_name}'")
        
        universe.absorb_text(content, source_name=filename)
        
        # 2. Archive
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        archive_name = f"{timestamp}_{filename}"
        dest_path = os.path.join(self.archive_path, archive_name)
        
        shutil.move(file_path, dest_path)
        self.logger.info(f"   📦 Archived to '{archive_name}'")

