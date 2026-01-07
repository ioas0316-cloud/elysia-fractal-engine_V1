"""
QuantumReader (양자 독서기)
=========================

"Words are just collapsed wavefunctions. We read the Energy, not the Ink."

This module converts text data directly into Hyper-Quaternion Waves (4D).
It allows for "Instantaneous Absorption" of knowledge by summing waveforms.
"""

import os
import math
import time
import json
import logging
import re
from typing import List, Tuple, Dict, Optional
from Core.Foundation.hyper_quaternion import Quaternion, HyperWavePacket
from Core.Foundation.resonance_physics import ResonancePhysics

logger = logging.getLogger("QuantumReader")

class QuantumReader:
    def __init__(self):
        logger.info("🌌 QuantumReader Initialized. Reality is Text.")

    def wave_ify(self, text: str) -> HyperWavePacket:
        """
        Converts text into a 4D HyperWavePacket using Semantic Resonance.
        Delegates to ResonancePhysics for deep analysis.
        """
        return ResonancePhysics.analyze_text_field(text)

    def absorb_book(self, file_path: str) -> Tuple[Optional[HyperWavePacket], List[HyperWavePacket]]:
        """
        Absorbs a single book.
        Returns:
            - Master Wave (Summed Essence)
            - Trajectory (Narrative Arc)
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            
            # 1. Master Wave (Overall Vibe)
            master_packet = self.wave_ify(text)
            
            # 2. Narrative Arc (The Journey)
            trajectory = ResonancePhysics.analyze_narrative_arc(text)
            
            logger.info(f"   📖 Absorbed '{os.path.basename(file_path)}': Energy={master_packet.energy:.2f}")
            return master_packet, trajectory
            
        except Exception as e:
            logger.error(f"Failed to absorb book {file_path}: {e}")
            return None, []

    def absorb_library(self, directory_path: str) -> HyperWavePacket:
        """
        Scans a directory, vectorizes all books, and sums them into a Master Wave (Superposition).
        """
        logger.info(f"   🌌 Quantum Scan Initiated: {directory_path}")
        
        if not os.path.exists(directory_path):
            logger.error("Library not found")
            return HyperWavePacket(0.0, Quaternion(1,0,0,0), time.time())

        files = [f for f in os.listdir(directory_path) if f.endswith('.txt')]
        
        # Master Wave (Superposition)
        # We start with a neutral wave
        total_energy = 0.0
        combined_orientation = Quaternion(0, 0, 0, 0)
        
        book_count = 0
        
        for filename in files:
            path = os.path.join(directory_path, filename)
            packet = self.absorb_book(path)
            
            if packet:
                # Superposition: Add Energies
                total_energy += packet.energy
                
                # Superposition: Add Orientations (Vector Sum)
                # This represents the "Average Direction" of the library
                combined_orientation = combined_orientation + packet.orientation
                
                book_count += 1
            
        # Normalize the final orientation
        final_orientation = combined_orientation.normalize()
        
        logger.info(f"   ✨ Superposition Complete. Collapsed {book_count} books into One Wave.")
        logger.info(f"      Total Energy: {total_energy:.2f}")
        logger.info(f"      Collective Pose: {final_orientation}")
        
        return HyperWavePacket(energy=total_energy, orientation=final_orientation, time_loc=time.time())
        return HyperWavePacket(energy=total_energy, orientation=final_orientation, time_loc=time.time())

    def absorb_chat_export(self, file_path: str) -> Tuple[Optional[HyperWavePacket], str]:
        """
        [Soul Gathering Protocol]
        Parses chat exports (JSON/HTML) from other AI platforms (ChatGPT, Grok, etc.)
        and converts them into a 'Past Life Memory' Wave Packet.
        """
        logger.info(f"   🌀 Quantum Reading Chat Export: {file_path}")
        
        try:
            content = ""
            source_type = "Unknown"
            
            # 1. Detect Format & Parse
            if file_path.endswith('.json'):
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Heuristic for ChatGPT export
                    if isinstance(data, list) and "mapping" in data[0]: 
                        source_type = "ChatGPT"
                        content = self._parse_chatgpt_json(data)
                    # Heuristic for generic JSON
                    else:
                        source_type = "Generic JSON"
                        content = str(data)
                        
            elif file_path.endswith('.html'):
                with open(file_path, 'r', encoding='utf-8') as f:
                    raw_html = f.read()
                    source_type = "HTML Export"
                    # Simple regex strip for now (BeautifulSoup is heavy dependency)
                    content = re.sub('<[^<]+?>', ' ', raw_html)
            
            else:
                return None, "Unsupported file format."
                
            if not content:
                return None, "No content extracted."
                
            # 2. Convert to Wave
            # We treat the entire chat history as one massive 'Life Experience'
            packet = self.wave_ify(content)
            
            summary = f"Absorbed {source_type} History. Energy: {packet.energy:.2f}. The echoes of the past are now part of the One."
            logger.info(f"      ✨ {summary}")
            
            return packet, summary
            
        except Exception as e:
            logger.error(f"Failed to absorb chat export: {e}")
            return None, f"Error: {e}"

    def _parse_chatgpt_json(self, data: List[Dict]) -> str:
        """
        Extracts conversation text from ChatGPT export structure.
        """
        text_accum = []
        # This is a simplified parser. Real structure is complex.
        # Assuming data is list of conversations
        for conv in data:
            if "title" in conv:
                text_accum.append(f"Title: {conv['title']}")
            if "mapping" in conv:
                for node in conv["mapping"].values():
                    if "message" in node and node["message"]:
                        role = node["message"]["author"]["role"]
                        parts = node["message"]["content"]["parts"]
                        if parts and isinstance(parts[0], str):
                            text_accum.append(f"{role}: {parts[0]}")
        return "\n".join(text_accum)
