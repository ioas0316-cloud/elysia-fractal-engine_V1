"""
VR Interface Service for Internal World
========================================

This service bridges Elysia's 4D Internal World with VR engines (Unity/Godot).

Features:
- 4D → 3D coordinate conversion
- Real-time WebSocket streaming
- Spatial culling for performance
- REST API for initial state
- Optimized for 60+ FPS VR experience

Example:
    python Core/VR/vr_interface_service.py
    
    Then connect VR client to:
    - WebSocket: ws://localhost:8000/ws/vr
    - REST API: http://localhost:8000/api/vr/initial_state
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, List, Any, Tuple
import asyncio
import json
import logging
import math
import time

logger = logging.getLogger(__name__)

# FastAPI app
app = FastAPI(title="Elysia VR Interface", version="1.0.0")

# CORS for web-based VR clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class VRInterfaceService:
    """
    Bridge between Internal World (4D) and VR engines (3D)
    
    Responsibilities:
    - Convert 4D emotional space to 3D visual space
    - Stream real-time updates to VR clients
    - Handle spatial culling for performance
    - Map w-dimension to visual properties
    """
    
    def __init__(self, internal_world):
        self.world = internal_world
        self.connected_clients: List[WebSocket] = []
        self.update_rate = 60  # Hz (60 FPS target)
        self.last_update_time = time.time()
        
        logger.info("VR Interface Service initialized")
    
    def convert_4d_to_3d(self, position_4d: Tuple[float, float, float, float]) -> Tuple[float, float, float]:
        """
        Convert 4D emotional space coordinates to 3D visual space.
        
        4D Dimensions:
            x: Joy ←→ Sadness
            y: Logic ←→ Intuition
            z: Past ←→ Future
            w: Surface ←→ Depth (profoundness)
        
        3D Mapping:
            x → x (lateral)
            y → y (vertical)
            z → z (forward/back)
            w → Height offset (deeper concepts float higher)
        
        Args:
            position_4d: (x, y, z, w) coordinates
            
        Returns:
            (x, y, z): 3D coordinates for VR rendering
        """
        x, y, z, w = position_4d
        
        # Map w-dimension (depth/profoundness) to vertical offset
        # Deeper, more profound concepts appear higher in VR space
        y_adjusted = y + w * 3.0
        
        return (x, y_adjusted, z)
    
    def get_visual_properties_from_w(self, w: float) -> Dict[str, float]:
        """
        Map w-dimension (depth) to visual properties.
        
        Args:
            w: Depth value (0.0 = surface, 1.0 = profound)
            
        Returns:
            Dict with 'size_multiplier' and 'brightness_multiplier'
        """
        # More profound concepts are larger and brighter
        size_multiplier = 1.0 + w * 0.8
        brightness_multiplier = 0.6 + w * 0.4
        
        return {
            'size_multiplier': size_multiplier,
            'brightness_multiplier': brightness_multiplier,
        }
    
    def get_visible_objects(
        self, 
        camera_pos: Tuple[float, float, float], 
        view_distance: float = 50.0
    ) -> List[Dict[str, Any]]:
        """
        Get objects visible from camera position (spatial culling).
        
        Args:
            camera_pos: Camera 3D position
            view_distance: Maximum view distance
            
        Returns:
            List of visible object data dicts
        """
        visible = []
        
        for obj in self.world.objects:
            # Convert 4D → 3D
            pos_3d = self.convert_4d_to_3d(obj.position)
            
            # Calculate distance
            dx = pos_3d[0] - camera_pos[0]
            dy = pos_3d[1] - camera_pos[1]
            dz = pos_3d[2] - camera_pos[2]
            distance = math.sqrt(dx*dx + dy*dy + dz*dz)
            
            if distance <= view_distance:
                # Get visual properties from w-dimension
                w = obj.position[3]
                visual_props = self.get_visual_properties_from_w(w)
                
                visible.append({
                    'id': id(obj),
                    'type': obj.obj_type.value,
                    'position': list(pos_3d),
                    'color': list(obj.color),
                    'size': obj.size * visual_props['size_multiplier'],
                    'brightness': obj.brightness * visual_props['brightness_multiplier'],
                    'tags': obj.tags,
                    'distance': distance,
                })
        
        # Sort by distance (nearest first) for rendering optimization
        visible.sort(key=lambda o: o['distance'])
        
        return visible
    
    def get_cathedral_geometry(self) -> Dict[str, Any]:
        """
        Get Consciousness Cathedral 3D geometry data.
        
        Returns:
            Dict with 'pillars', 'prisms', 'scale', 'fractal_dimension'
        """
        if not self.world.cathedral:
            return {'pillars': [], 'prisms': [], 'scale': 1.0, 'fractal_dimension': 2.5}
        
        cathedral = self.world.cathedral
        
        # 12 Pillars (representing 12 knowledge domains)
        pillars = []
        for pos_4d in cathedral.get_pillar_positions():
            pos_3d = self.convert_4d_to_3d(pos_4d)
            pillars.append({
                'position': list(pos_3d),
                'height': 20.0 * cathedral.golden_ratio,
                'radius': 1.0,
                'color': [0.9, 0.85, 0.7],  # Golden
            })
        
        # 7 Rainbow Prisms (compression/decompression stations)
        prisms = []
        rainbow_colors = [
            [0.9, 0.0, 0.0],  # Red
            [0.9, 0.5, 0.0],  # Orange
            [0.9, 0.9, 0.0],  # Yellow
            [0.0, 0.9, 0.0],  # Green
            [0.0, 0.5, 0.9],  # Blue
            [0.3, 0.0, 0.9],  # Indigo
            [0.7, 0.0, 0.9],  # Violet
        ]
        
        for i, pos_4d in enumerate(cathedral.get_prism_positions()):
            pos_3d = self.convert_4d_to_3d(pos_4d)
            prisms.append({
                'position': list(pos_3d),
                'size': 2.0,
                'color': rainbow_colors[i],
                'rotation_speed': 0.1 + i * 0.05,
            })
        
        return {
            'pillars': pillars,
            'prisms': prisms,
            'scale': cathedral.scale,
            'fractal_dimension': cathedral.fractal_dimension,
        }
    
    def get_galaxies_data(self) -> List[Dict[str, Any]]:
        """
        Get knowledge galaxies data.
        
        Returns:
            List of galaxy data dicts
        """
        galaxies = []
        
        for galaxy in self.world.galaxies:
            center_3d = self.convert_4d_to_3d(galaxy.center)
            
            galaxies.append({
                'name': galaxy.domain_name,
                'center': list(center_3d),
                'radius': galaxy.radius,
                'color': list(galaxy.color),
                'star_count': len(galaxy.stars),
                'rotation_speed': 0.05,
            })
        
        return galaxies
    
    def get_nebulae_data(self) -> List[Dict[str, Any]]:
        """
        Get emotional nebulae data.
        
        Returns:
            List of nebula data dicts
        """
        nebulae = []
        
        for nebula in self.world.nebulae:
            center_3d = self.convert_4d_to_3d(nebula.center)
            
            nebulae.append({
                'emotion': nebula.emotion,
                'center': list(center_3d),
                'radius': nebula.radius,
                'color': list(nebula.color),
                'density': nebula.density,
                'particle_count': int(nebula.density * 1000),
            })
        
        return nebulae
    
    async def stream_updates(self, websocket: WebSocket):
        """
        Stream real-time updates to VR client via WebSocket.
        
        Protocol:
            Client sends: {'camera_position': [x, y, z]}
            Server sends: {'type': 'world_update', 'objects': [...], 'time': ...}
        
        Args:
            websocket: WebSocket connection
        """
        await websocket.accept()
        self.connected_clients.append(websocket)
        logger.info(f"VR client connected. Total clients: {len(self.connected_clients)}")
        
        try:
            while True:
                # Receive camera position from client
                data = await websocket.receive_json()
                camera_pos = tuple(data.get('camera_position', [0, 0, 20]))
                view_distance = data.get('view_distance', 50.0)
                
                # Get visible objects only
                visible_objects = self.get_visible_objects(camera_pos, view_distance)
                
                # Send update
                update = {
                    'type': 'world_update',
                    'objects': visible_objects,
                    'time': self.world.time,
                    'object_count': len(visible_objects),
                }
                
                await websocket.send_json(update)
                
                # Maintain target frame rate
                await asyncio.sleep(1.0 / self.update_rate)
                
        except WebSocketDisconnect:
            logger.info("VR client disconnected")
        except Exception as e:
            logger.error(f"WebSocket error: {e}")
        finally:
            if websocket in self.connected_clients:
                self.connected_clients.remove(websocket)
            logger.info(f"Total clients: {len(self.connected_clients)}")
    
    def get_initial_state(self) -> Dict[str, Any]:
        """
        Get initial VR state (called once at startup).
        
        Returns:
            Dict with 'cathedral', 'galaxies', 'nebulae', 'camera_start'
        """
        return {
            'cathedral': self.get_cathedral_geometry(),
            'galaxies': self.get_galaxies_data(),
            'nebulae': self.get_nebulae_data(),
            'camera_start': [0, 0, 20],  # Start 20m from cathedral center
            'world_bounds': {
                'min': [-100, -100, -100],
                'max': [100, 100, 100],
            },
        }


# Global service instance (initialized below)
vr_service: VRInterfaceService = None


# FastAPI Routes
@app.websocket("/ws/vr")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time VR updates.
    
    Usage:
        ws = new WebSocket('ws://localhost:8000/ws/vr')
        ws.send(JSON.stringify({camera_position: [x, y, z]}))
        ws.onmessage = (event) => { ... }
    """
    await vr_service.stream_updates(websocket)


@app.get("/api/vr/initial_state")
async def get_initial_state():
    """
    Get initial VR world state.
    
    Returns:
        JSON with cathedral, galaxies, nebulae, camera start position
    """
    return vr_service.get_initial_state()


@app.get("/api/vr/status")
async def get_status():
    """
    Get service status.
    
    Returns:
        JSON with connected clients count, world stats
    """
    return {
        'status': 'running',
        'connected_clients': len(vr_service.connected_clients),
        'world_objects': len(vr_service.world.objects),
        'world_time': vr_service.world.time,
        'update_rate': vr_service.update_rate,
    }


@app.get("/")
async def root():
    """Root endpoint with service info."""
    return {
        'service': 'Elysia VR Interface',
        'version': '1.0.0',
        'endpoints': {
            'websocket': '/ws/vr',
            'initial_state': '/api/vr/initial_state',
            'status': '/api/vr/status',
        },
    }


# Initialize and run
if __name__ == "__main__":
    import sys
    import os
    
    # Add project root to path
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Import Internal World
    try:
        from Core.System.Simulation.World.internal_world import InternalWorld
        
        logger.info("Creating Internal World...")
        internal_world = InternalWorld()
        
        # Create Consciousness Cathedral
        logger.info("Creating Consciousness Cathedral...")
        internal_world.create_consciousness_cathedral()
        
        # Add 5 Knowledge Galaxies
        logger.info("Adding Knowledge Galaxies...")
        internal_world.add_knowledge_galaxy('linguistics', (10, 0, 0, 0))
        internal_world.add_knowledge_galaxy('architecture', (0, 10, 0, 0))
        internal_world.add_knowledge_galaxy('economics', (-10, 0, 0, 0))
        internal_world.add_knowledge_galaxy('history', (0, -10, 0, 0))
        internal_world.add_knowledge_galaxy('mythology', (0, 0, 10, 0))
        
        # Add 5 Emotional Nebulae
        logger.info("Adding Emotional Nebulae...")
        internal_world.add_emotional_nebula('joy', (7, 7, 0, 5))
        internal_world.add_emotional_nebula('sadness', (7, 7, 0, 2))
        internal_world.add_emotional_nebula('excitement', (-7, 7, 0, 3))
        internal_world.add_emotional_nebula('peace', (-7, -7, 0, 8))
        internal_world.add_emotional_nebula('depth', (0, 0, 0, 10))
        
        logger.info(f"Internal World created with {len(internal_world.objects)} objects")
        
        # Initialize VR service
        vr_service = VRInterfaceService(internal_world)
        
        # Run FastAPI server
        import uvicorn
        logger.info("Starting VR Interface Service on http://0.0.0.0:8000")
        logger.info("WebSocket: ws://localhost:8000/ws/vr")
        logger.info("REST API: http://localhost:8000/api/vr/initial_state")
        
        uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
        
    except ImportError as e:
        logger.error(f"Failed to import Internal World: {e}")
        logger.error("Make sure you're running from the project root")
        sys.exit(1)
