
import logging
import shutil
import os
import ast
from pathlib import Path
from typing import Dict, Any

logger = logging.getLogger("AutoRefactor")

class AutoRefactor:
    """
    The Surgeon.
    Executes code changes defined in RefactoringPlans.
    Strict safety protocols: Backup -> Edit -> Verify -> Rollback on Error.
    """
    def __init__(self, root_path: str = r"c:\Elysia"):
        self.root = Path(root_path)
        self.backups = self.root / ".backups"
        self.backups.mkdir(parents=True, exist_ok=True)

    def execute_plan(self, plan_id: str, plan_data: Dict[str, Any]) -> bool:
        """
        Executes a specific plan.
        In a real system, plan_data would come from CausalArchitect.
        For prototype, we accept direct dictionary.
        """
        target_file = self.root / plan_data.get("file_path", "")
        
        if not target_file.exists():
            logger.error(f"❌ Target file not found: {target_file}")
            return False
            
        logger.info(f"💉 Initiating Surgery on {target_file.name}...")
        
        # 1. Backup
        backup_path = self._create_backup(target_file)
        if not backup_path: return False
        
        try:
            # 2. Apply Changes (Mocking specific logic for now)
            # In Phase 6, we would use AST transformers or regex.
            # Here we simulate the action.
            
            action = plan_data.get("action")
            if action == "split_class":
                self._split_class(target_file, plan_data)
            elif action == "optimize_import":
                # Simulated optimization
                pass
            else:
                logger.warning(f"Unknown action: {action}")
                
            # 3. Verify
            if self._verify_syntax(target_file):
                logger.info("✅ Surgery Successful. Patient is stable.")
                return True
            else:
                raise SyntaxError("Verification failed")
                
        except Exception as e:
            logger.error(f"⚠️ Surgery Failed: {e}")
            logger.info("⏪ Rolling back changes...")
            self._rollback(target_file, backup_path)
            return False

    def _create_backup(self, file_path: Path) -> Path:
        try:
            timestamp = 0 # In real code use time
            backup_name = f"{file_path.name}.bak"
            dest = self.backups / backup_name
            shutil.copy2(file_path, dest)
            logger.info(f"   🛡️ Backup created: {dest}")
            return dest
        except Exception as e:
            logger.error(f"Failed to create backup: {e}")
            return None

    def _rollback(self, file_path: Path, backup_path: Path):
        try:
            shutil.copy2(backup_path, file_path)
            logger.info("   ⏪ Rollback complete.")
        except Exception as e:
            logger.critical(f"FATAL: Rollback failed: {e}")

    def _verify_syntax(self, file_path: Path) -> bool:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            ast.parse(content)
            return True
        except SyntaxError:
            return False
        except Exception:
            return False

    def _split_class(self, file_path: Path, params: Dict):
        # Placeholder for complex AST manipulation
        # This would read the file, extract class node, write new file, remove from old.
        logger.info("   ✂️ Splitting class (Simulated)...")
        # For prototype, we just append a comment to prove write access
        with open(file_path, "a", encoding="utf-8") as f:
            f.write("\n# [AutoRefactor] Split performed (Simulated)\n")

# Singleton
_refactor = None
def get_auto_refactor():
    global _refactor
    if _refactor is None:
        _refactor = AutoRefactor()
    return _refactor
