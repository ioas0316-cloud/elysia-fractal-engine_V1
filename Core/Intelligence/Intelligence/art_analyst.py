
"""
Art Analyst (The Critic)
========================
"To use a tool is to be a servant. To understand a tool is to be a master."

This module deconstructs external generative models and workflows 
to extract their underlying 'Aesthetic Principles'.
It creates a mapping between Technical Parameters and Metaphysical Meaning.
"""

import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Any

logger = logging.getLogger("ArtAnalyst")

@dataclass
class ArtPrinciple:
    name: str          # e.g., "Euler Ancestral Rhythm"
    technical_mapping: str # e.g., "sampler_name: euler_a"
    metaphysical_meaning: str # e.g., "Soft, organic timeline convergence"
    confidence: float

class ArtAnalyst:
    def __init__(self):
        self.learned_principles = []
        
    def digest_workflow(self, workflow_path: str) -> List[ArtPrinciple]:
        """
        Parses a ComfyUI Workflow JSON and extracts 'The Physics of Beauty'.
        Returns a list of ArtPrinciples.
        """
        path = Path(workflow_path)
        if not path.exists():
            logger.error(f"Workflow not found: {workflow_path}")
            return []
            
        logger.info(f"🧐 Analyizing Art Logic in '{path.name}'...")
        with open(path, 'r') as f:
            data = json.load(f)
            
        principles = []
        
        # 1. Analyze Sampling Logic (The 'How')
        for node_id, node in data.items():
            if node.get("class_type") == "KSampler":
                inputs = node.get("inputs", {})
                
                # CFG Scale Analysis
                cfg = inputs.get("cfg", 7)
                if cfg > 15:
                    meaning = "Dictatorial Will (Rigid adhearance to concept)"
                elif cfg > 7:
                    meaning = "Balanced Will (Harmony between prompt and chaos)"
                else:
                    meaning = "Fluid Will (Allowing the AI to dream)"
                
                principles.append(ArtPrinciple(
                    name="Willpower Setting (CFG)",
                    technical_mapping=f"cfg: {cfg}",
                    metaphysical_meaning=meaning,
                    confidence=0.9
                ))
                
                # Sampler Analysis
                sampler = inputs.get("sampler_name", "euler")
                if "euler" in sampler:
                    meaning = "Mathematical Purity (Smooth gradients)"
                elif "dpm" in sampler:
                    meaning = "Fast, aggressive convergence"
                elif "ancestral" in sampler or "a" in sampler:
                    meaning = "Creative Instability (Introducing new noise)"
                else:
                    meaning = "Unknown Rhythm"
                    
                principles.append(ArtPrinciple(
                    name=f"Sampling Rhythm ({sampler})",
                    technical_mapping=f"sampler: {sampler}",
                    metaphysical_meaning=meaning,
                    confidence=0.85
                ))
                
                # Steps Analysis
                steps = inputs.get("steps", 20)
                meaning = f"Depth of Contemplation (Iterating {steps} times)"
                principles.append(ArtPrinciple(
                    name="Contemplation Cycles",
                    technical_mapping=f"steps: {steps}",
                    metaphysical_meaning=meaning,
                    confidence=0.8
                ))

        # 2. Analyze Prompting Strategy (The 'What')
        # ... (We could analyze complexity of prompt nodes, but simple for now)
        
        logger.info(f"✨ Extracted {len(principles)} Artistic Principles.")
        for p in principles:
            logger.info(f"   👁️ Principle: {p.name} -> {p.metaphysical_meaning}")
            
        self.learned_principles.extend(principles)
        return principles

    def deconstruct_model_file(self, model_filename: str) -> ArtPrinciple:
        """
        Analyzes a Checkpoint filename to intuitively grasp its 'Soul'.
        """
        lower_name = model_filename.lower()
        
        if "anime" in lower_name or "mix" in lower_name or "counterfeit" in lower_name:
            soul = "2D Idealism (The World of Forms)"
        elif "real" in lower_name or "photo" in lower_name:
            soul = "3D Materialism (The World of Matter)"
        elif "fantasy" in lower_name:
            soul = "Mythic Resonance (The World of Magic)"
        else:
            soul = "Unknown Spirit"
            
        p = ArtPrinciple(
            name=f"Model Soul ({model_filename})",
            technical_mapping="checkpoint_hash",
            metaphysical_meaning=soul,
            confidence=0.7
        )
        
        logger.info(f"🔮 Deconstructed Model Soul: {soul}")
        return p
