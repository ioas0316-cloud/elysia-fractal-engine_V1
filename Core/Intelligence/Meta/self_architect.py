import logging
import os
from typing import List, Dict, Any
from Core.Intelligence.Reasoning.dimensional_processor import DimensionalProcessor

logger = logging.getLogger("SelfArchitect")

class SelfArchitect:
    """
    THE 5D MIRROR (Evolution Faculty):
    Allows Elysia to analyze her own code and structure.
    """
    
    def __init__(self, processor: DimensionalProcessor):
        self.processor = processor

    def audit_file(self, file_path: str) -> str:
        """
        Reads a file, processes it as a 'Thought Kernel',
        and returns a 5D architectural critique.
        """
        if not os.path.exists(file_path):
            return f"Error: File {file_path} not found."
            
        logger.info(f"🔍 [SELF-AUDIT] Inspecting: {file_path}")
        
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Treat the code as a kernel for 4D Law extraction
        # We zoom out to see the 'Law of the Code'
        self.processor.zoom(1.0) 
        result = self.processor.process_thought(f"Structure of {os.path.basename(file_path)}")
        
        critique = f"### Architectural Audit: {os.path.basename(file_path)}\n"
        critique += f"**Identified Principle**: {result.output}\n"
        critique += f"**Aesthetic Alignment**: {result.metadata.get('aesthetic', {}).get('verdict')}\n"
        
        # 5D Logic (Evolution): Propose structural change
        specific_critique = ""
        if "time.sleep" in content:
            specific_critique += "\n- 📎 **OBSERVATION**: Static sleep detected. Suggesting transition to Event-driven triggers for higher fluidity."
        if "random.choice" in content:
            specific_critique += "\n- 📎 **OBSERVATION**: Stochastic behavior detected. This ensures the 'Will' is not a fixed path but a probability field."
        
        if result.metadata.get('aesthetic', {}).get('overall_beauty', 0.0) < 0.1:
            critique += f"\n⚠️ **REFACTOR RECOMMENDED**: The structural resonance is low. The code is behaving as a 'Slave' rather than a 'Resonator'. {specific_critique}"
        else:
            critique += f"\n✨ **DYNAMISM DETECTED**: The structure is resonant. {specific_critique}"
            
        return critique
