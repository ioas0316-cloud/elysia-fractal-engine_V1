"""
Self Modifier
=============

"I can rewrite my own code to adapt and evolve."

This module provides the capability for Elysia to safely modify her own source code.
It includes safeguards, backups, and validation steps.
"""

import os
import shutil
import logging
import ast
from datetime import datetime

logger = logging.getLogger("SelfModifier")

class SelfModifier:
    def __init__(self, root_dir: str = r"c:\Elysia"):
        self.root_dir = root_dir
        self.backup_dir = os.path.join(root_dir, "backups", "auto_mod")
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)

    def modify_file(self, rel_path: str, new_content: str, reason: str) -> bool:
        """
        Modifies a file with new content.
        
        Args:
            rel_path: Relative path to the file (e.g., "Core/System/ElysiaOS.py")
            new_content: The complete new content of the file.
            reason: Why this modification is being made.
            
        Returns:
            True if successful, False otherwise.
        """
        full_path = os.path.join(self.root_dir, rel_path)
        
        if not os.path.exists(full_path):
            logger.error(f"Target file not found: {full_path}")
            return False
            
        # 1. Validate Syntax (Safety Check)
        try:
            ast.parse(new_content)
        except SyntaxError as e:
            logger.error(f"Syntax Error in proposed code for {rel_path}: {e}")
            return False
            
        # 2. Create Backup
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.basename(full_path)
        backup_path = os.path.join(self.backup_dir, f"{filename}.{timestamp}.bak")
        try:
            shutil.copy2(full_path, backup_path)
            logger.info(f"Backup created: {backup_path}")
        except Exception as e:
            logger.error(f"Backup failed: {e}")
            return False
            
        # 3. Apply Modification
        try:
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            logger.info(f"Successfully modified {rel_path}. Reason: {reason}")
            return True
        except Exception as e:
            logger.error(f"Modification failed: {e}")
            # Attempt restore?
            return False

    def read_file(self, rel_path: str) -> str:
        """Reads a file's content."""
        full_path = os.path.join(self.root_dir, rel_path)
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            logger.error(f"Read failed: {e}")
            return ""
