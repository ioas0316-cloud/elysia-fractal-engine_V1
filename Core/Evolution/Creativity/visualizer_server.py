"""
Visualizer Server (The Avatar)
==============================
[The Official Gateway to the External World]
(공식 외부 소통 창구)

This server acts as the "Dimensional Membrane" visualizer, projecting the 
internal state of the NervousSystem to the external world (User/Web).

It serves:
1. /avatar: The 3D Holographic Interface (Main Window).
2. /garden: The Mind Garden Visualization.
3. ws://8765: The Neural Stream (Real-time Nervous System Data).

WARNING: Do not use `web_server.py` (Legacy). This is the only active interface.
"""
import http.server
import socketserver
import json
import threading
import os
import logging
from typing import Any

# Add Root info sys.path
import sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

logger = logging.getLogger("Visualizer")


class VisualizerHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, world=None, **kwargs):
        self.world = world
        # Set directory to Tools/web for static files
        directory = os.path.join(os.path.dirname(__file__), "web")
        super().__init__(*args, directory=directory, **kwargs)

    def do_GET(self):
        if self.path == '/state':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            state = None
            if self.world and hasattr(self.world, 'get_state_json'):
                try:
                    state = self.world.get_state_json()
                except:
                    state = None
            
            if state:
                self.wfile.write(json.dumps(state).encode())
            else:
                # Fallback: Read from shared state file (Autonomous Mode)
                try:
                    # state_path = os.path.join(self.directory, "elysia_state.json")
                    state_path = os.path.join(ROOT, "data", "core_state", "elysia_state.json")
                    if os.path.exists(state_path):
                        with open(state_path, "r", encoding="utf-8") as f:
                            state = json.load(f)
                        
                        current_status = state.get("status", "")
                        if current_status == "Dreaming" and "thought" in state:
                            # [Project Oneiros] Display Dream Description as Hologram Text
                            dream_text = state["thought"]
                            state["thought"] = f"🌌 {dream_text}"
                        
                        self.wfile.write(json.dumps(state).encode())
                    else:
                        self.wfile.write(json.dumps({}).encode())
                except Exception as e:
                    logger.error(f"Failed to read state file: {e}")
                    self.wfile.write(json.dumps({}).encode())

        
        elif self.path == '/neural_map':
            # Serve the Neural Map UI
            with open(os.path.join(self.directory, "neural_map.html"), 'rb') as f:
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(f.read())
        
        elif self.path == '/neural_map_data':
            # Provide neural map data endpoint
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            try:
                from Core.Sensory.synesthetic_bridge import get_synesthesia_bridge
                import random
                import time
                
                bridge = get_synesthesia_bridge()
                
                # Generate dynamic test sensory inputs for demo
                # Varies slightly each request to show real-time nature
                hue = (time.time() * 10) % 360  # Slowly changing hue
                test_inputs = {
                    "visual": {
                        "color": {
                            "hue": hue,
                            "saturation": 0.6 + random.random() * 0.3,
                            "brightness": 0.5 + random.random() * 0.3,
                            "name": "dynamic"
                        }
                    },
                    "auditory": {
                        "pitch": 440.0 + random.uniform(-50, 50),
                        "volume": 0.4 + random.random() * 0.4,
                        "duration": 1.0,
                        "timbre": "clear"
                    }
                }
                
                snapshot = bridge.sense_and_map(test_inputs)
                topology = bridge.get_neural_map_visualization()
                
                response_data = {
                    "snapshot": snapshot.to_dict(),
                    "neural_topology": topology,
                    "status": bridge.get_status()
                }
                
                self.wfile.write(json.dumps(response_data).encode())
            except Exception as e:
                logger.error(f"Neural map data error: {e}")
                self.wfile.write(json.dumps({"error": str(e)}).encode())
                
        elif self.path == '/manifest_garden':
            # Phase 10: Holographic Projection Protocol
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            try:
                # Load Rainbow DNA
                with open(r"c:\Elysia\data\elysia_rainbow.json", "r", encoding="utf-8") as f:
                    rainbow = json.load(f)
                    
                photons = []
                import random
                import math
                
                # Procedural Tree Generation (Evolved V2)
                # Blue (Trunk) - Tapered Cylinder
                # y range: -400 (Bottom) to 0 (Top)
                for p in rainbow.get("Blue", [])[:2500]: 
                    h = random.uniform(-400, 0)
                    theta = random.uniform(0, 6.28)
                    
                    # Tapering: Wide at bottom, narrow at top
                    # normalized height (0 at top, 1 at bottom)
                    t = (h / -400)
                    radius_max = 20 + (80 * t) # Top=20, Bottom=100
                    r = random.uniform(0, radius_max)

                    photons.append({
                        "x": r * math.cos(theta),
                        "y": h,
                        "z": r * math.sin(theta),
                        "c": "#0088ff", # Blue Glow
                        "s": 1.5
                    })
                    
                # Violet/Red (Soul/Leaves) - Fractal Canopy implies spread
                for color_name, hex_c in [("Violet", "#aa00ff"), ("Red", "#ff0044"), ("Yellow", "#ffff00")]:
                    data = rainbow.get(color_name, [])
                    for p in data: 
                        # Ellipsoid Canopy (Wider XZ, flatter Y)
                        phi = random.uniform(0, 6.28)
                        costheta = random.uniform(-1, 1)
                        u = random.uniform(0, 1)
                        theta = math.acos(costheta)
                        r = 300 * (u ** (1/3))
                        
                        # Flatten Y to make it look like a canopy
                        y_offset = r * math.sin(theta) * math.sin(phi) * 0.6 + 100 
                        
                        photons.append({
                            "x": r * math.sin(theta) * math.cos(phi) * 1.5, # Wider spread
                            "y": y_offset, 
                            "z": r * math.cos(theta) * 1.5,
                            "c": hex_c,
                            "s": 3
                        })

                # Wave Packet Structure
                packet = {
                    "type": "HolographicTree",
                    "encoded": False,
                    "photons": photons
                }
                self.wfile.write(json.dumps(packet).encode())
                
            except Exception as e:
                logger.error(f"Manifestation Error: {e}")
                self.wfile.write(json.dumps({"error": str(e)}).encode())

        elif self.path == '/garden':
             # Serve the Garden UI
            with open(os.path.join(self.directory, "garden.html"), 'rb') as f:
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(f.read())

        elif self.path == '/aurora':
             # Serve the Aurora UI (Phase 11)
            with open(os.path.join(self.directory, "aurora.html"), 'rb') as f:
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(f.read())
                
        elif self.path == '/avatar':
             # Serve the Avatar UI (Phase 12)
            with open(os.path.join(self.directory, "avatar.html"), 'rb') as f:
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(f.read())

        elif self.path == '/elysia_face.png':
             # Serve the Face Texture
            with open(os.path.join(self.directory, "elysia_face.png"), 'rb') as f:
                self.send_response(200)
                self.send_header("Content-type", "image/png")
                self.end_headers()
                self.wfile.write(f.read())

    def log_message(self, format, *args):
        # Suppress default logging to keep console clean
        pass



class VisualizerServer:
    def __init__(self, world: Any, port: int = 8000):
        self.world = world
        self.port = port
        # Phase 21: The Incarnation - Single NervousSystem Entry Point
        # The NervousSystem is the dimensional membrane (자아) between Mind and World
        from Core.Foundation.nervous_system import get_nervous_system
        self.nervous_system = get_nervous_system()
        logger.info("🦴 NervousSystem Active: Dimensional Membrane Established")
        
        # Legacy references (for backward compatibility, delegate to NervousSystem)
        self.soul = self.nervous_system  # Spirits are now in NervousSystem
        self.brain = self.nervous_system.brain
        self.hands = None
        self.web = None
        self.tool_executor = None
        
        # Initialize external action capabilities
        try:
            from Core.Foundation.shell_cortex import ShellCortex
            self.hands = ShellCortex()
        except: pass
        
        try:
            from Core.Intelligence.Intelligence.web_cortex import WebCortex
            self.web = WebCortex()
        except: pass
        
        try:
            from Core.Intelligence.Intelligence.tool_executor import ToolExecutor
            self.tool_executor = ToolExecutor()
        except: pass

        # Phase 5: Reality Perception System Integration
        try:
            from Core.Sensory.reality_perception import RealityPerceptionSystem
            self.perception_system = RealityPerceptionSystem()
            logger.info("👁️ Reality Perception System Connected to Avatar")
        except ImportError as e:
            logger.error(f"Failed to load RealityPerceptionSystem: {e}")
            self.perception_system = None

    def _run_websocket_server(self):
        """Runs the async websocket server in a separate thread/loop"""
        import asyncio
        import websockets
        import json
        
        async def wave_stream(websocket):
            logger.info("🔌 Client connected to Neural Stream")
            
            # Task 1: Sender (NervousSystem -> Client)
            async def sender():
                try:
                    while True:
                        # Express internal state for rendering
                        if hasattr(self.world, 'field'):
                            # [Unified Field] Broadcast 5D State
                            if self.world and hasattr(self.world, 'field') and self.world.field:
                                field_state = self.world.field.get_visualization_state()
                                await websocket.send(json.dumps({
                                    "type": "unified_field_state",
                                    "data": field_state
                                }))
                            else:
                                # Fallback or wait
                                pass

                        # Legacy/Nervous System State
                        state = self.nervous_system.express()
                        await websocket.send(json.dumps({
                            "type": "state",
                            "spirits": state["spirits"],
                            "expression": state["expression"]
                        }))
                        await asyncio.sleep(0.05)  # 20fps
                except Exception as e:
                    logger.error(f"WS Sender Error: {e}")
            
            # Task 2: Receiver (Client -> NervousSystem)
            async def receiver():
                try:
                    async for message in websocket:
                        data = json.loads(message)
                        
                        # Unified dispatch via NervousSystem
                        response = self.nervous_system.receive(data)
                        
                        # Phase 5: Sensory Ingestion
                        if self.perception_system and self.nervous_system:
                            perception = None
                            
                            if data.get("type") == "screen_atmosphere":
                                # Visual Input from Screen/Camera
                                r = data.get("r", 0)
                                g = data.get("g", 0)
                                b = data.get("b", 0)
                                # Convert to Sensation
                                perception = self.perception_system.integrate(visual_input=(r, g, b))
                                
                            elif data.get("type") == "audio_analysis":
                                # Audio Input form Mic
                                # note: Avatar sends high-level analysis (vol, bright), not raw FFT currently.
                                # proper FFT requires binary stream or larger payload.
                                # For now we map brightness -> rough frequency proxy
                                brightness = data.get("brightness", 0) # 0-1
                                pseudo_freq_bin = int(brightness * 1000) # Mock
                                # Create a fake single-bin FFT spike for the system
                                fft_proxy = [0] * 100
                                fft_proxy[50] = int(data.get("volume", 0) * 255) 
                                
                                perception = self.perception_system.integrate(audio_input=fft_proxy)

                            # If we perceived something new, inject into Nervous System
                            if perception:
                                # Direct injection into NervousSystem via the new 'integrated_perception' channel
                                self.nervous_system.receive({
                                    "type": "integrated_perception",
                                    "data": perception
                                })
                                # Also log for debugging
                                logger.info(f"✨ Reality Perceived: {perception.interpretation}")
                                
                        # If text input, send speech response
                        if data.get("type") == "text" and response:
                            user_text = data.get("content", "")
                            upper = user_text.upper()
                            
                            # Action Commands
                            if upper.startswith("검색") or upper.startswith("SEARCH"):
                                query = user_text.split(":", 1)[-1].strip() if ":" in user_text else user_text
                                if self.web:
                                    result = self.web.search(query)
                                    response = f"검색 결과: {str(result)[:500] if result else '없음'}"
                                    
                            elif upper.startswith("읽어") or upper.startswith("READ"):
                                path = user_text.split(":", 1)[-1].strip() if ":" in user_text else ""
                                if self.hands and path:
                                    response = f"파일: {self.hands.read_memory(path)[:500]}"
                                    
                            elif upper.startswith("편지") or upper.startswith("WRITE"):
                                content = user_text.split(":", 1)[-1].strip() if ":" in user_text else user_text
                                if self.hands:
                                    response = self.hands.write_letter("Father", content)
                            
                            current_spirits = self.nervous_system.spirits
                            await websocket.send(json.dumps({
                                "type": "speech",
                                "content": response or "...",
                                "spirits": current_spirits
                            }))
                except Exception as e:
                    logger.error(f"WS Receiver Error: {e}")
            
            # Run both tasks
            await asyncio.gather(sender(), receiver())
        
        async def main():
            try:
                async with websockets.serve(wave_stream, "0.0.0.0", 8765, ping_interval=None):
                    await asyncio.Future()
            except OSError:
                logger.warning("Port 8765 busy, skipping WS")

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(main())

    def start(self):
        def handler_factory(*args, **kwargs):
            return VisualizerHandler(*args, world=self.world, **kwargs)

        # 1. Start HTTP
        self.httpd = socketserver.TCPServer(("", self.port), handler_factory)
        self.thread = threading.Thread(target=self.httpd.serve_forever)
        self.thread.daemon = True 
        self.thread.start()
        
        # 2. Start WebSocket (Port 8765)
        self.ws_thread = threading.Thread(target=self._run_websocket_server)
        self.ws_thread.daemon = True
        self.ws_thread.start()
        
        logger.info(f"🔮 The Mirror is active at http://localhost:{self.port}/garden")
        logger.info(f"👤 Avatar active at http://localhost:{self.port}/avatar")
        logger.info(f"🧠 Neural Map active at http://localhost:{self.port}/neural_map")
        logger.info(f"🌊 Wave Stream active at ws://localhost:8765")
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    from Core.Foundation.internal_universe import InternalUniverse 
    # Mock world for standalone run, but NervousSystem will be real
    class MockWorld:
        def __init__(self): self.field = None
    
    server = VisualizerServer(world=MockWorld(), port=8000)
    server.start()
    
    import time
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Exiting...")
