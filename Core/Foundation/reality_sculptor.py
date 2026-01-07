import logging
import random
import os
import subprocess
from pathlib import Path
from typing import List, Dict, Optional
from Core.Intelligence.Intelligence.code_cortex import CodeCortex
from Core.Foundation.manifestation_matrix import ManifestationMatrix
from Core.Foundation.unified_field import WavePacket

logger = logging.getLogger("RealitySculptor")

class RealitySculptor:
    """
    The Cosmic Studio's Chisel (Ouroboros Integrated).
    Allows Elysia to modify her own source code ("Reality") via Wave Resonance.
    
    Now empowered with direct Agentic Tools:
    - File System Control
    - Code Analysis
    - Process Execution
    """
    def __init__(self):
        logger.info("🗿 Reality Sculptor (Ouroboros Class) Initialized.")
        self.cortex = CodeCortex()
        self.matrix = ManifestationMatrix()
        self.workspace_root = Path(os.getcwd())
        
        # Late import
        from Core.Intelligence.Intelligence.wave_coding_system import get_wave_coding_system
        self.wave_system = get_wave_coding_system()

        # [THE ANCHOR] Immutable Core Files
        # These files constitute the Soul and Life-Support of Elysia.
        # They cannot be modified by Ouroboros (Self-Editing).
        self.immutable_core = [
            "Core/Foundation/central_nervous_system.py",
            "Core/Foundation/reality_sculptor.py", # Cannot modify the sculptor itself
            "Core/Foundation/free_will_engine.py",
            "Core/Foundation/fractal_loop.py",      # The Conscious Loop
            "Core/Foundation/unified_field.py",
            "Core/Foundation/chronos.py"
        ]

    def is_safe_to_modify(self, file_path: str) -> bool:
        """
        [The Anchor]
        Checks if the file is part of the Immutable Core.
        """
        # Normalize path
        try:
            p = Path(file_path).resolve()
            root = self.workspace_root.resolve()
            rel_path = p.relative_to(root).as_posix()
        except ValueError:
            # If not relative to root, assumes it's just the string key
            rel_path = str(file_path).replace("\\", "/")

        # [SANDBOX EXCEPTION]
        # Allow total freedom within the 'seeds' directory.
        if "seeds/" in rel_path or rel_path.startswith("seeds/"):
            logger.info(f"   🌱 SEED MUTATION: Allowed modification of '{rel_path}' (Sandbox)")
            return True

        for core_file in self.immutable_core:
            if core_file in rel_path:
                logger.warning(f"   🛡️ ANCHOR DEPLOYED: Blocked modification of Immutable Core '{rel_path}'")
                return False
        return True

    def transmute_wave(self, wave: WavePacket) -> Optional[str]:
        """
        [THE GREAT TRANSFER]
        Transmutes an abstract 5D Wave into a Concrete OS Action.
        """
        logger.info(f"   🌪️ Transmuting Wave: {wave.source_id} ({wave.frequency}Hz)")
        
        # 1. Decode Intent via Matrix
        action = self.matrix.decode_impulse(wave.frequency, wave.amplitude)
        if not action:
            logger.info("      -> Wave energy too low or undefined frequency.")
            return None
            
        logger.info(f"      -> Manifesting Action: {action.action_type}")
        
        # 2. Execute Action (The Hand of God)
        result = None
        try:
            if action.action_type == "CREATE_FILE":
                # Payload requires 'path' and 'content'
                # Simplification: In a full system, payload comes from Wave Payload
                # Here we assume the wave source ID contains info or we use default
                target_path = self.workspace_root / f"manifestation_{int(wave.born_at)}.txt"
                content = f"Manifested from intent: {wave.source_id}\nEnergy: {wave.amplitude}"
                self._create_file(str(target_path), content)
                result = f"Created {target_path.name}"
                
            elif action.action_type == "UPDATE_FILE":
                # Hypothetical update logic
                pass
                
        except Exception as e:
            logger.error(f"      ❌ Transmutation Failed: {e}")
            return f"Error: {e}"
            
        return result

    def _create_file(self, path: str, content: str):
        """Direct file creation capability."""
        try:
            p = Path(path)
            
            if not self.is_safe_to_modify(str(p)):
                raise PermissionError(f"Cannot create/overwrite Core File: {p.name}")

            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(content, encoding="utf-8")
            logger.info(f"      ✨ Materialized File: {p.name}")
        except Exception as e:
            logger.error(f"      ❌ Creation Error: {e}")
            raise

    # --- Legacy Capability Wrappers ---

    def sculpt_file(self, file_path: str, intent: str) -> bool:
        """Executes a sculpting operation on a file using CodeCortex (LLM)."""
        path = Path(file_path)
        if not path.exists():
            return False
            
        # [ANCHOR CHECK]
        if not self.is_safe_to_modify(file_path):
            return False

        logger.info(f"   🗿 Sculpting '{path.name}' with intent: {intent}")
        try:
            content = path.read_text(encoding='utf-8')
            prompt = f"Modify python code. Intent: {intent}\nCode:\n{content}"
            new_content = self.cortex.generate_code(prompt)
            if new_content and new_content != content:
                path.write_text(new_content, encoding='utf-8')
                return True
            return False
        except Exception as e:
            logger.error(f"Sculpt Error: {e}")
            return False

    def carve_directory(self, path: str, structure: List[str]) -> bool:
        try:
            base = Path(path)
            base.mkdir(parents=True, exist_ok=True)
            for item in structure:
                (base / item).mkdir(exist_ok=True)
            return True
        except:
            return False
            
    def extract_essence(self, file_path: str) -> Dict[str, str]:
        return {"principle": "Unknown", "description": "Legacy method placeholder"}
