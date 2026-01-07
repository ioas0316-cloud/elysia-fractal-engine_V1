"""
CosmicStudio (우주 스튜디오)
===========================

"The Studio is where the Dream becomes Reality."

This module orchestrates the creation process. It receives 'Desires' (HyperWavePackets)
from the ReasoningEngine and uses the RealitySculptor to manifest them into the RealityCanvas.
"""

import os
import logging
from typing import Optional, List
from Core.Foundation.hyper_quaternion import HyperWavePacket
from Core.Foundation.reality_sculptor import RealitySculptor

logger = logging.getLogger("CosmicStudio")

class CosmicStudio:
    def __init__(self, canvas_path: str = "c:/Elysia/RealityCanvas"):
        self.canvas_path = canvas_path
        self.sculptor = RealitySculptor()
        
        if not os.path.exists(self.canvas_path):
            os.makedirs(self.canvas_path)
            logger.info(f"🎨 Reality Canvas initialized at {self.canvas_path}")
            
    def manifest(self, desire_packet: HyperWavePacket, intent: str) -> str:
        """
        Manifests a desire into reality using Wave Synthesis.
        
        Args:
            desire_packet: The 4D thought form to manifest.
            intent: A description of what to create (e.g., "A poem about gravity").
            
        Returns:
            The path to the created artifact.
        """
        logger.info(f"🎨 Manifesting intent: '{intent}' (Energy: {desire_packet.energy:.2f})")
        
        # 1. Determine the form (File Extension/Type) based on intent
        file_ext = ".txt"
        if "code" in intent.lower() or "python" in intent.lower():
            file_ext = ".py"
            
        # 2. Simulate CodeWave from Intent (Energy -> Frequency/Amplitude)
        # Higher Energy = Higher Complexity (Frequency)
        # Higher Confidence (Packet Magnitude) = Higher Importance (Amplitude)
        simulated_frequency = min(100.0, desire_packet.energy * 0.8) 
        simulated_amplitude = min(1.0, desire_packet.energy / 120.0)
        
        # Import dynamically to avoid circular issues
        from Core.Intelligence.Intelligence.wave_coding_system import CodeWave, CodePhase, CodeDimension, Quaternion
        
        wave = CodeWave(
            source_file="manifestation_seed",
            code_snippet="", # Empty seed
            frequency=simulated_frequency,
            amplitude=simulated_amplitude,
            phase=CodePhase.ALGORITHM if file_ext == ".py" else CodePhase.DECLARATION,
            dimension=CodeDimension.SYSTEM,
            orientation=Quaternion(1, 0, 0, 0) # Base orientation
        )
        
        # 3. Sculpt the content using Wave Synthesis
        if file_ext == ".py":
            logger.info("   🌊 Synthesizing Code Wave...")
            content = self.sculptor.sculpt_from_code_wave(wave, intent)
        else:
            content = self.sculptor.sculpt_from_wave(intent, desire_packet.energy)
        
        # 4. Save to Canvas
        filename = f"{intent.replace(' ', '_')}_{int(desire_packet.time_loc)}{file_ext}"
        file_path = os.path.join(self.canvas_path, filename)
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
            
        logger.info(f"✨ Created artifact: {file_path}")
        return file_path
