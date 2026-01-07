"""
Dream Daemon: The Subconscious Processor
========================================

"Sleep is the chisel of memory."

This module is responsible for 'Offline Processing'.
When Elysia is idle (or during 'Night Mode'), the DreamDaemon:
1.  **Consolidates**: Moves Short-Term Memory (STM) to Long-Term HyperGraph.
2.  **Synthesizes**: Finds hidden connections between distant nodes (Serendipity).
3.  **Prunes**: Removes weak/unused connections (Forgetting).

It is the mechanism of **Insight**.
"""

import time
import random
import logging
from typing import List, Dict
from elysia_core import Cell, Organ

@Cell("DreamDaemon")
class DreamDaemon:
    def __init__(self):
        self.logger = logging.getLogger("Elysia.Dream")
        self.stm_buffer = [] # Short Term Memory Buffer
        self.is_dreaming = False
        
    def absorb_thought(self, thought: str):
        """
        Input from ReasoningEngine during the day.
        """
        self.stm_buffer.append(thought)
        if len(self.stm_buffer) > 100:
            self.stm_buffer.pop(0) # Keep linear buffer small

    def enter_rem_state(self, duration_seconds: int = 5):
        """
        Triggered by Scheduler when idle.
        """
        self.is_dreaming = True
        self.logger.info("🌙 Entering REM State (Dreaming)...")
        
        graph = Organ.get("HyperGraph")
        
        # 1. Consolidation (STM -> LTM)
        if self.stm_buffer:
            thought = random.choice(self.stm_buffer)
            self._consolidate(thought, graph)
            
        # 2. Serendipity (Random Walk)
        self._weave_dreams(graph)
        
        time.sleep(duration_seconds)
        self.is_dreaming = False
        self.logger.info("☀️ Waking up from Dream.")

    def _consolidate(self, thought: str, graph):
        """
        Turning a fleeting thought into a solid node.
        """
        # Simple extraction for now
        keywords = [w for w in thought.split() if len(w) > 5]
        if keywords:
            concept = keywords[0]
            # graph.add_node(concept, "concept") # Pseudo-code
            self.logger.info(f"   🧠 Consolidated Memory: '{concept}' from thought.")

    def _weave_dreams(self, graph):
        """
        Connecting distant concepts.
        """
        # In a real HyperGraph, we would take two random nodes and check resonance.
        # For now, we simulate the 'Insight'.
        concepts = ["Time", "Void", "Love", "Entropy", "Light", "Code"]
        c1 = random.choice(concepts)
        c2 = random.choice(concepts)
        
        if c1 != c2:
            self.logger.info(f"   🕸️  Dream Connection: Is '{c1}' related to '{c2}'?")
            # Logic to create edge would go here
