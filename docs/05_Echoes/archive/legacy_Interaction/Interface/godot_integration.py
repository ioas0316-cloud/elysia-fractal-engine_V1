from __future__ import annotations

from typing import Any, Dict, Optional

from godot_bridge_server import BridgeConfig, GodotBridge


class GodotIntegration:
    """
    Lightweight bridge for Godot that exposes the same frame/input semantics
    without running a standalone WebSocket server.
    """

    def __init__(self, cfg: Optional[BridgeConfig] = None) -> None:
        self.bridge = GodotBridge(cfg or BridgeConfig())

    def get_initial_frame(self) -> Dict[str, Any]:
        return self.bridge._build_init()

    def next_frame(self) -> Dict[str, Any]:
        return self.bridge._build_frame()

    def process_input(self, data: Dict[str, Any]) -> None:
        self.bridge._handle_input(data)

    @property
    def world(self):
        return self.bridge.world

    def read_latest_soul_state(self) -> Dict[str, Any]:
        return self.bridge._read_latest_soul_state()
