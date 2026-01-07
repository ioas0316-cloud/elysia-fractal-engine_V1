"""
Console HUD ( The Visor )
=========================
"To see the pulse is to know the life."

Provides a text-based dashboard for Elysia's internal state.
"""

import sys
import time

# [Lazy Load] Torch is optional for HUD
try:
    import torch
    TORCH_AVAILABLE = True
except ImportError:
    torch = None
    TORCH_AVAILABLE = False

class ConsoleHUD:
    def __init__(self, graph):
        self.graph = graph
        self.start_time = time.time()
        self.frame_count = 0
        self.last_update_time = time.time()
        
        # Initialize Mass Tracking
        nodes = self.graph.pos_tensor.shape[0]
        self.last_mass = self.graph.mass_tensor.sum().item() if nodes > 0 else 0
        
    def render(self, current_action: str = "Dreaming"):
        """
        Prints a 1-line status bar (overwriting previous line).
        """
        now = time.time()
        self.frame_count += 1
        
        # Calculate Stats
        uptime = int(now - self.start_time)
        nodes = self.graph.pos_tensor.shape[0]
        links = self.graph.logic_links.shape[0]
        mass = self.graph.mass_tensor.sum().item() if nodes > 0 else 0
        
        # Rate Calculation
        delta_time = now - self.last_update_time
        if delta_time < 0.1: delta_time = 0.1 # Avoid div by zero
        
        mass_diff = mass - self.last_mass
        rate = mass_diff / delta_time
        
        self.last_update_time = now
        self.last_mass = mass
        
        # Wisdom (Metadata / Nodes)
        wisdom_count = len(self.graph.node_metadata)
        wisdom_sat = (wisdom_count / nodes * 100) if nodes > 0 else 0
        
        # Format
        # [0123s] 🧠 1205 | 🔗 3500 | ⚖️  150.2 (+1.2/s) | 🔮 5.2% | ACTION: ...
        status = (
            f"\r[{uptime:04d}s] "
            f"🧠 {nodes} "
            f"🔗 {links} "
            f"⚖️  {mass:.1f} ({rate:+.1f}/s) "
            f"🔮 {wisdom_sat:.1f}% "
            f"ACTION: {current_action:<20}"
        )
        
        # Use sys.stdout.write + flush for dynamic update
        sys.stdout.write(status)
        sys.stdout.flush()

# Factory
_hud = None
def get_console_hud(graph):
    global _hud
    if _hud is None:
        _hud = ConsoleHUD(graph)
    return _hud
