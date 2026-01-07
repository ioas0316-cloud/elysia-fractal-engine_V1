
import json
import hashlib
import time
from pathlib import Path
from dataclasses import dataclass, asdict

@dataclass
class CodePatch:
    id: str
    author: str         # e.g., "Nova"
    target_file: str    # Relative path
    new_content: str
    reason: str
    created_at: float
    checksum: str

class PatchManager:
    """
    [The Genetic Messenger]
    Encapsulates logic for creating, verifying, and applying code patches.
    """
    
    def __init__(self, workspace_root: str):
        self.workspace_root = Path(workspace_root)

    def create_patch(self, author: str, target_file: str, new_content: str, reason: str) -> dict:
        """Packages a code modification into a transferable CodePatch."""
        
        # Calculate Checksum
        checksum = hashlib.sha256(new_content.encode('utf-8')).hexdigest()
        patch_id = f"patch_{int(time.time())}_{checksum[:8]}"
        
        patch = CodePatch(
            id=patch_id,
            author=author,
            target_file=target_file,
            new_content=new_content,
            reason=reason,
            created_at=time.time(),
            checksum=checksum
        )
        
        return asdict(patch)

    def verify_patch(self, patch_data: dict) -> bool:
        """Verifies integrity of a received patch."""
        try:
            # Reconstruct and verify hash
            content = patch_data['new_content']
            calculated = hashlib.sha256(content.encode('utf-8')).hexdigest()
            
            if calculated != patch_data['checksum']:
                print(f"❌ Patch Integrity Fail: {patch_data['id']}")
                return False
                
            return True
        except Exception as e:
            print(f"❌ Patch Verification Error: {e}")
            return False

    def apply_patch(self, patch_data: dict, dry_run: bool = True) -> bool:
        """Applies the patch to the local file system."""
        try:
            target_path = self.workspace_root / patch_data['target_file']
            
            print(f"   🔧 Applying Patch [{patch_data['id']}] to {target_path.name}")
            print(f"      Reason: {patch_data['reason']}")
            
            if not dry_run:
                target_path.parent.mkdir(parents=True, exist_ok=True)
                target_path.write_text(patch_data['new_content'], encoding='utf-8')
                print("      ✅ Patch Applied Successfully.")
            else:
                print("      🚧 Dry Run: Content would be updated.")
                
            return True
        except Exception as e:
            print(f"      ❌ Patch Application Failed: {e}")
            return False
