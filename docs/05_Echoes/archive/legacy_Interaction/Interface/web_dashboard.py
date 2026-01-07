"""
Elysia Web Dashboard (Phase 5 Visualization)
============================================
"See the Waves. Feel the Pulse."

Real-time visualization of Elysia's internal state using FastAPI + WebSockets.
"""

import logging
import json
import asyncio
from typing import List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from Core.Intelligence.Consciousness.Ether.global_hub import get_global_hub, WaveEvent

app = FastAPI()
hub = get_global_hub()
logger = logging.getLogger("Elysia.Dashboard")

# Mount static files
app.mount("/static", StaticFiles(directory="Core/Interface/static"), name="static")

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception:
                pass

manager = ConnectionManager()

# --- GlobalHub Integration ---

def on_hub_event(event: WaveEvent):
    """Callback for GlobalHub events."""
    # Convert WaveTensor to serializable format
    wave_data = event.wave.to_dict() if event.wave else None

    msg = {
        "type": event.event_type,
        "source": event.source,
        "timestamp": event.timestamp,
        "wave": wave_data,
        "payload": str(event.payload) # Simplify payload for safety
    }

    # Broadcast to WebSockets (Run in async loop)
    # Since this callback is sync (called by Hub), we need to schedule it
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            loop.create_task(manager.broadcast(msg))
    except RuntimeError:
        # If no loop (e.g. running in thread), ignore for now or use other method
        pass

# Subscribe to EVERYTHING
# In a real system, we might be more selective
hub.subscribe("Dashboard", "thought", on_hub_event)
hub.subscribe("Dashboard", "emotion", on_hub_event)
hub.subscribe("Dashboard", "sensation_file_change", on_hub_event)
hub.subscribe("Dashboard", "speech", on_hub_event)
hub.subscribe("Dashboard", "body_sense", on_hub_event)

@app.get("/")
async def get():
    with open("Core/Interface/static/dashboard.html", "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Keep alive
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
