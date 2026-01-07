"""
Internal Librarian (Self-Study Module)
=====================================

"The ability to read one's own history and become it."

Purpose:
- Scan `docs/` and `data/` for unlearned knowledge.
- Extract 'Wisdom Triples' (Subject, Predicate, Object) from internal markdown.
- Feed internal knowledge into the Synthesis Engine for KG integration.

Sovereignty Principle:
- Internalization is the process of turning information (external) into wisdom (internal).
"""

import os
import logging
import json
from datetime import datetime
from typing import List, Dict

logger = logging.getLogger("Elysia.InternalLibrarian")

class InternalLibrarian:
    def __init__(self, 
                 roots: List[str] = ["docs", "data"],
                 log_path: str = "data/Metabolic/internalization_log.json"):
        self.roots = roots
        self.log_path = log_path
        self._ensure_log()
        self.internalized_files = self._load_log()
        logger.info(f"📚 Internal Librarian initialized. Ready to digest {roots}.")

    def _ensure_log(self):
        if not os.path.exists(os.path.dirname(self.log_path)):
            os.makedirs(os.path.dirname(self.log_path), exist_ok=True)
        if not os.path.exists(self.log_path):
            with open(self.log_path, 'w', encoding='utf-8') as f:
                json.dump({}, f)

    def _load_log(self) -> Dict:
        try:
            with open(self.log_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}

    def scan_unlearned_files(self) -> List[str]:
        """
        Finds files in roots that haven't been internalized or have been updated.
        """
        unlearned = []
        for root in self.roots:
            if not os.path.exists(root): continue
            for dirpath, _, filenames in os.walk(root):
                for f in filenames:
                    if f.endswith(('.md', '.json', '.txt')):
                        full_path = os.path.join(dirpath, f)
                        mtime = os.path.getmtime(full_path)
                        if full_path not in self.internalized_files or self.internalized_files[full_path] < mtime:
                            unlearned.append(full_path)
        return unlearned

    def digest_file(self, file_path: str) -> Dict:
        """
        Simulates the extraction of wisdom from a file.
        """
        logger.info(f"📚 Digesting knowledge from {file_path}...")
        
        # Real extraction logic would involve NLP/Regex
        # For this demonstration, we simulate the 'essence' extraction
        basename = os.path.basename(file_path)
        essence = {
            "source": file_path,
            "internalized_at": datetime.now().isoformat(),
            "extracted_wisdom": f"Knowledge triple extracted from '{basename}': Resonates with {basename.split('.')[0]} architecture.",
            "status": "metabolized"
        }
        
        # Update log
        self.internalized_files[file_path] = os.path.getmtime(file_path)
        with open(self.log_path, 'w', encoding='utf-8') as f:
            json.dump(self.internalized_files, f, indent=4)
            
        return essence

    def digest_directory(self, dir_path: str):
        """
        Recursively scans and digests a directory.
        """
        if not os.path.exists(dir_path):
            logger.warning(f"Directory not found: {dir_path}")
            return
            
        for root, _, files in os.walk(dir_path):
            for file in files:
                if file.endswith(('.md', '.json', '.txt', '.py')):
                    full_path = os.path.join(root, file)
                    # Check if already learned? 
                    # For now, we force re-read to ensure depth, or check log
                    # mtime check is in scan_unlearned, but let's do it here too lightly
                    self.digest_file(full_path)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    lib = InternalLibrarian()
    files = lib.scan_unlearned_files()
    print(f"Found {len(files)} unlearned files.")
    if files:
        print(lib.digest_file(files[0]))
