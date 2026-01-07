## Godot Integration (In-process Bridge)

When a standalone WebSocket server is too heavy, `Project_Elysia/high_engine/godot_integration.py` exposes the same observation pipeline inside the Python process so Godot can call it directly.

### API
- `GodotIntegration(cfg: Optional[BridgeConfig])`: instantiate the shared world + ToddlerChat state.
- `get_initial_frame()`: returns the initial `{"type":"init"}` payload.
- `next_frame()`: step the simulation and return the frame payload (cells, overlays, `frame["elysia"]` data, etc.).
- `process_input(data)`: accept the same input dictionary that the WebSocket bridge expects (e.g. `{type:"input", input_type:"chat", text:"..."}` or vision/disaster knobs).
- `read_latest_soul_state()`: helper for getting the most recent mood/thought/vision log.

### Integration Strategy
1. Embed a Python interpreter inside Godot (e.g., via `godot-python` plugin) or expose a lightweight RPC that can call these methods.
2. On startup, call `get_initial_frame()` to configure the UI, then every tick call `next_frame()` for updated world + Elysia data.
3. When the user interacts (clicks a cell, types text, sends vision data), translate that into the input dictionary and pass it to `process_input`. The integration will update the world + Elysia state immediately.
4. Since `GodotIntegration` reuses the same `GodotBridge` logic, you still get all the new `focus_area`, `thought_trail`, `meta_observation`, and vision logging fields without running a separate server.

This lets you treat Godot as the UI layer and keep Python as the single authority, removing the need for a persistent WebSocket server.
