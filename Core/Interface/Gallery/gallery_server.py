"""
Gallery Server: The Mirror of Mind
----------------------------------
"To see is to know. To know is to change."

This module provides the API endpoints for the 'Gallery of Soul' visualization.
It exposes the internal state of the `OrbManager` to the web interface.
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import logging
import os
import sys

# Adjust path to access Core
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from Core.Foundation.Memory.Orb.orb_manager import OrbManager
from Core.Foundation.Protocols.pulse_protocol import WavePacket, PulseType

# Initialize Logger
logger = logging.getLogger("GalleryServer")

app = FastAPI(title="Elysia Gallery", description="Visualization of the Crystalline Memory")

# Setup Templates
base_dir = os.path.dirname(__file__)
templates_dir = os.path.join(base_dir, "templates")
templates = Jinja2Templates(directory=templates_dir)

# Global Manager Instance (In a real app, this would be injected)
_orb_manager = None

def get_orb_manager():
    global _orb_manager
    if _orb_manager is None:
        # Initialize with default path
        _orb_manager = OrbManager()
    return _orb_manager

@app.get("/", response_class=HTMLResponse)
async def read_gallery(request: Request):
    """Serves the main visualization page."""
    return templates.TemplateResponse("mirror_gallery.html", {"request": request})

@app.get("/mind/state")
async def get_mind_state():
    """
    Returns the current constellation of memories (Orbs).
    Format: List of {id, name, x, y, z, color, size}
    """
    manager = get_orb_manager()
    orbs_data = []

    for name, orb in manager.orbs.items():
        # Map 4D Quaternion to 3D Space
        # We project W, X, Y, Z -> X, Y, Z
        # This is a simplification. Ideally we use T-SNE.
        # But for 'Soul Visualization', raw quaternion components are meaningful axes.

        # Color: Map Frequency (400-800Hz) to RGB or HSL
        # 400Hz (Red) -> 600Hz (Green) -> 800Hz (Blue)
        normalized_freq = (orb.frequency - 400.0) / 400.0 # 0.0 to 1.0
        normalized_freq = max(0.0, min(1.0, normalized_freq))

        # Size: Mass
        size = max(0.5, math.log(orb.mass + 1.0) * 2.0)

        # Position:
        # X = Quaternion X * 10
        # Y = Quaternion Y * 10
        # Z = Quaternion Z * 10
        pos = orb.get_3d_position()

        orbs_data.append({
            "id": name,
            "name": name,
            "x": pos[0],
            "y": pos[1],
            "z": pos[2],
            "frequency": orb.frequency,
            "mass": orb.mass,
            "active": orb.state.is_active
        })

    return {"orbs": orbs_data, "count": len(orbs_data)}

@app.post("/mind/focus/{orb_name}")
async def focus_orb(orb_name: str):
    """
    Triggers a recall (Focus) on a specific orb.
    """
    manager = get_orb_manager()
    orb = manager.get_orb(orb_name)
    if not orb:
        raise HTTPException(status_code=404, detail="Orb not found")

    # Simulate a Recall Pulse
    # In a full system, this would be broadcasted by the Conductor.
    # Here we just 'touch' the orb.
    orb.melt() # Wake it up

    return {"status": "focused", "name": orb.name, "intensity": orb.state.amplitude}

# Helper for mass calculation in API logic
import math

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
