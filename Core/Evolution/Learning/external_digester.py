"""
External Digester (외부 소화기)
===============================

"To eat the world is to understand it."
"세상을 먹는 것이 곧 세상을 이해하는 것이다."

This module connects the 'Eye' (WebTendril) to the 'Stomach' (Hippocampus).
It allows Elysia to browse the web and internalize what she sees.
"""

import logging
from typing import List, Dict, Optional
from Core.Sensory.Network.web_tendril import WebTendril, FrequencySignal
from Core.Foundation.Memory.Graph.hippocampus import Hippocampus
from Core.Foundation.Memory.Orb.orb_manager import OrbManager

logger = logging.getLogger("ExternalDigester")

class ExternalDigester:
    def __init__(self):
        self.eye = WebTendril()
        self.hippocampus = Hippocampus()
        self.orb_manager = OrbManager()
        logger.info("🌍 ExternalDigester initialized. The Window is open.")

    def digest_url(self, url: str) -> str:
        """
        Fetches, Tastes, and Swallows a URL.
        Returns a summary of the digestion.
        """
        logger.info(f"🕸️ Reaching out to: {url}")
        
        # 1. Touch (Fetch)
        signal: FrequencySignal = self.eye.touch(url)
        
        if signal.frequency == 0.0:
            return f"❌ Failed to reach {url}. The Void stared back."

        # 2. Taste (Analyze)
        logger.info(f"   👅 Tasted Frequency: {signal.frequency}Hz")
        
        # 3. Swallow (Store as Orb)
        # Create a wave representation of the content
        data_wave = [float(ord(c)) % 100 for c in signal.content_summary[:50]]
        emotion_wave = [signal.frequency] * 10
        
        # Safe filename
        safe_name = signal.url.split('//')[-1].replace('/', '_').replace(':', '_').replace('?', '_')
        concept_name = f"Web_{safe_name[:30]}"
        
        self.orb_manager.save_memory(
            name=concept_name,
            data_wave=data_wave,
            emotion_wave=emotion_wave
        )
        
        # 4. Digest (Graph Node)
        node_id = f"web:{url}"
        self.hippocampus.learn(
            id=node_id,
            name=concept_name,
            definition=signal.content_summary,
            tags=["web", "external", "knowledge"],
            frequency=signal.frequency,
            realm="Logos"
        )
        
        # Link to "The World" concept if it exists, or create a temporary anchor
        self.hippocampus.learn("concept:the_world", "The External Reality", "Everything outside", ["axiom"], 432.0, "Logos")
        self.hippocampus.connect("concept:the_world", node_id, "contains", 0.5)

        return f"✅ Digested {url}. Tasted like {signal.frequency}Hz."

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    ed = ExternalDigester()
    # Test with a dummy or real URL if internet is available
    # ed.digest_url("http://example.com")
