"""
Elysia Avatar Server (엘리시아 아바타 서버)
===========================================

WebSocket server that provides real-time avatar control and visualization.
Integrates with Elysia's emotional, spirit, and cognitive systems.

Features:
- Real-time expression control (facial animations)
- Spirit/elemental energy broadcasting (fire, water, earth, air, light, dark, aether)
- Emotion-driven facial expressions
- Chat integration with ReasoningEngine
- VRM model support
- Synesthesia data streaming (vision, audio, screen)

Architecture:
    Client (avatar.html) <--WebSocket--> avatar_server.py <--> Elysia Core Systems
                                              |
                                              +-> EmotionalEngine
                                              +-> SpiritEmotionMapper
                                              +-> ReasoningEngine (for chat)
                                              +-> VoiceOfElysia (for speech)

Usage:
    python Core/Interface/avatar_server.py --port 8765
    
Then open Core/Creativity/web/avatar.html in a browser.
"""

import asyncio
import json
import logging
import os
import sys
import time
from pathlib import Path
from typing import Dict, Any, Optional, Set, List, TYPE_CHECKING
from dataclasses import dataclass, asdict

if TYPE_CHECKING:
    from websockets.server import WebSocketServerProtocol

# Setup path
REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("AvatarServer")

# Import Elysia systems (with graceful degradation)
try:
    from Core.Foundation.emotional_engine import EmotionalEngine, EmotionalState
    from Core.Foundation.spirit_emotion import SpiritEmotionMapper
    logger.info("✅ Emotional and Spirit systems loaded")
    EMOTIONS_AVAILABLE = True
except ImportError as e:
    logger.warning(f"⚠️ Could not load emotional systems: {e}")
    logger.info("ℹ️ Running in standalone mode without emotion integration")
    EmotionalEngine = None
    EmotionalState = None
    SpiritEmotionMapper = None
    EMOTIONS_AVAILABLE = False

try:
    # [BRIDGE] Try New Core first
    from Core.Intelligence.Intelligence.reasoning_engine import ReasoningEngine
    logger.info("✅ ReasoningEngine (Soul) loaded")
    REASONING_AVAILABLE = True
except ImportError as e:
    try:
        # Legacy path
        from Core.Intelligence.Intelligence.Reasoning.reasoning_engine import ReasoningEngine
        logger.info("✅ ReasoningEngine loaded (Legacy)")
        REASONING_AVAILABLE = True
        REASONING_AVAILABLE = True
    except ImportError as e:
        logger.warning(f"⚠️ Could not load ReasoningEngine: {e}")
        logger.info("ℹ️ Running without reasoning engine - using simple responses")
        ReasoningEngine = None
        REASONING_AVAILABLE = False
        
try:
    from Core.Foundation.free_will_engine import FreeWillEngine
    logger.info("✅ FreeWillEngine (Will) loaded")
except ImportError:
    FreeWillEngine = None

try:
    import websockets
    if not TYPE_CHECKING:
        from websockets.server import WebSocketServerProtocol
    WEBSOCKETS_AVAILABLE = True
except ImportError:
    logger.error("❌ websockets package not installed. Run: pip install websockets")
    WEBSOCKETS_AVAILABLE = False
    WebSocketServerProtocol = type(None)  # Fallback for runtime
    # Don't exit here - allow importing for testing
    if __name__ == "__main__":
        sys.exit(1)

# Avatar Physics Engine (Phase 4)
try:
    from Core.Foundation.avatar_physics import AvatarPhysicsEngine, Vector3D
    logger.info("✅ Avatar Physics Engine loaded")
    PHYSICS_AVAILABLE = True
except ImportError as e:
    logger.warning(f"⚠️ Could not load Avatar Physics Engine: {e}")
    logger.info("ℹ️ Running without physics engine")
    AvatarPhysicsEngine = None
    Vector3D = None
    PHYSICS_AVAILABLE = False


@dataclass
class Expression:
    """Facial expression parameters"""
    mouth_curve: float = 0.0  # -1.0 (sad) to 1.0 (smile)
    eye_open: float = 1.0     # 0.0 (closed) to 1.0 (open)
    brow_furrow: float = 0.0  # 0.0 (relaxed) to 1.0 (furrowed)
    beat: float = 0.0         # Heartbeat animation
    mouth_width: float = 0.0  # For phoneme/viseme


@dataclass
class Spirits:
    """Seven elemental spirits/energies"""
    fire: float = 0.1      # Passion, creativity, energy
    water: float = 0.1     # Calm, flow, memory
    earth: float = 0.3     # Stability, grounding
    air: float = 0.2       # Communication, connection
    light: float = 0.2     # Clarity, intelligence
    dark: float = 0.1      # Mystery, introspection
    aether: float = 0.1    # Ethereal, transcendent


class ElysiaAvatarCore:
    """
    Core logic for avatar state management.
    Bridges Elysia's internal systems with visual representation.
    """
    
    def __init__(self):
        self.expression = Expression()
        self.spirits = Spirits()
        self.beat_phase = 0.0
        
        # Delta update tracking
        self.last_state = None
        self.delta_threshold = 0.01  # Minimum change to trigger update
        
        # Initialize emotional system
        if EmotionalEngine:
            self.emotional_engine = EmotionalEngine()
            logger.info("✅ Emotional engine initialized")
        else:
            self.emotional_engine = None
            logger.warning("⚠️ Running without emotional engine")
        
        # Initialize spirit mapper
        if SpiritEmotionMapper:
            self.spirit_mapper = SpiritEmotionMapper()
            logger.info("✅ Spirit mapper initialized")
        else:
            self.spirit_mapper = None
            logger.warning("⚠️ Running without spirit mapper")
        
        # Initialize reasoning engine for chat
        if ReasoningEngine:
            try:
                self.reasoning_engine = ReasoningEngine()
                logger.info("✅ Reasoning engine initialized")
            except Exception as e:
                logger.warning(f"⚠️ Could not initialize reasoning engine: {e}")
                self.reasoning_engine = None
        else:
            self.reasoning_engine = None
            logger.warning("⚠️ Running without reasoning engine")
        
        # Initialize synesthesia-enhanced voice TTS
        try:
            from Core.Interaction.Interface.avatar_voice_tts import AvatarVoiceTTS
            self.voice_tts = AvatarVoiceTTS()
            logger.info("🎤 Synesthesia voice TTS initialized")
        except Exception as e:
            logger.warning(f"⚠️ Could not initialize voice TTS: {e}")
            self.voice_tts = None
        
        # Initialize lip-sync engine
        try:
            from Core.Interaction.Interface.avatar_lipsync import LipSyncEngine
            self.lipsync_engine = LipSyncEngine()
            logger.info("👄 Lip-sync engine initialized")
        except Exception as e:
            logger.warning(f"⚠️ Could not initialize lip-sync engine: {e}")
            self.lipsync_engine = None
        
        # Initialize physics engine (Phase 4)
        if PHYSICS_AVAILABLE and AvatarPhysicsEngine:
            self.physics_engine = AvatarPhysicsEngine()
            # Initialize with default hair bones (5 nodes from head to tip)
            default_bones = [
                Vector3D(0, 2.0, 0),
                Vector3D(0, 1.8, -0.2),
                Vector3D(0, 1.6, -0.4),
                Vector3D(0, 1.4, -0.6),
                Vector3D(0, 1.2, -0.8)
            ]
            self.physics_engine.initialize_hair_springs(default_bones)
            logger.info("⚡ Physics engine initialized (hair dynamics)")
        else:
            self.physics_engine = None
            logger.warning("⚠️ Running without physics engine")
    
    def update_expression_from_emotion(self, emotion_name: str = None):
        """
        Update facial expression based on emotional state.
        Maps emotions to facial parameters.
        """
        if not self.emotional_engine:
            return
        
        state = self.emotional_engine.current_state
        
        # Map valence to mouth curve (smile/frown)
        self.expression.mouth_curve = max(-1.0, min(1.0, state.valence))
        
        # Map arousal to eye openness (alertness)
        # High arousal = wide eyes, low arousal = relaxed/closed
        self.expression.eye_open = max(0.3, min(1.0, 0.5 + state.arousal * 0.5))
        
        # Map dominance/tension to brow
        if state.arousal > 0.7:
            self.expression.brow_furrow = 0.3  # Alert/focused
        elif state.valence < -0.5:
            self.expression.brow_furrow = 0.5  # Concerned
        else:
            self.expression.brow_furrow = 0.0  # Relaxed
    
    def update_spirits_from_emotion(self):
        """
        Update spirit energies based on emotional state.
        """
        if not self.emotional_engine or not self.spirit_mapper:
            return
        
        state = self.emotional_engine.current_state
        
        # Map emotional dimensions to spirit energies
        # Fire: Passion, high arousal + positive valence
        self.spirits.fire = max(0.0, min(1.0, 
            0.1 + (state.arousal * 0.4) + (state.valence * 0.4 if state.valence > 0 else 0)
        ))
        
        # Water: Calm, melancholy, low arousal
        self.spirits.water = max(0.0, min(1.0,
            0.1 + ((1.0 - state.arousal) * 0.4) + (abs(state.valence) * 0.3 if state.valence < 0 else 0)
        ))
        
        # Earth: Stability, grounding, low dominance
        self.spirits.earth = max(0.0, min(1.0,
            0.3 + ((1.0 - abs(state.dominance)) * 0.4)
        ))
        
        # Air: Communication, openness, positive dominance
        self.spirits.air = max(0.0, min(1.0,
            0.2 + (state.dominance * 0.3 if state.dominance > 0 else 0) + (state.arousal * 0.2)
        ))
        
        # Light: Clarity, high positive valence
        self.spirits.light = max(0.0, min(1.0,
            0.2 + (state.valence * 0.5 if state.valence > 0 else 0)
        ))
        
        # Dark: Introspection, negative valence or very low arousal
        self.spirits.dark = max(0.0, min(1.0,
            0.1 + (abs(state.valence) * 0.3 if state.valence < -0.3 else 0) + 
            (0.3 if state.arousal < 0.2 else 0)
        ))
        
        # Aether: Transcendent, extreme states
        extremity = (abs(state.valence) + abs(state.dominance)) / 2.0
        self.spirits.aether = max(0.0, min(1.0, 
            0.1 + (extremity * 0.4 if extremity > 0.7 else 0)
        ))
    
    def update_physics_from_emotion(self):
        """
        Update physics engine based on emotional state.
        
        Maps emotions to physical parameters:
        - Valence → gravity direction
        - Arousal → wind strength/turbulence
        - Dominance → wave frequency
        """
        if not self.physics_engine or not self.emotional_engine:
            return
        
        state = self.emotional_engine.current_state
        
        # Update physics with emotional state
        self.physics_engine.update_from_emotion(
            valence=state.valence,
            arousal=state.arousal,
            dominance=state.dominance
        )
    
    def update_beat(self, delta_time: float):
        """Update heartbeat animation"""
        import math
        
        # Heartbeat frequency based on arousal
        if self.emotional_engine:
            arousal = self.emotional_engine.current_state.arousal
            # Clamp arousal to safe range
            arousal = max(0.0, min(1.0, arousal))
            freq = 1.0 + arousal * 1.5  # 1-2.5 Hz
        else:
            freq = 1.2  # Default
        
        if not math.isfinite(delta_time) or not math.isfinite(self.beat_phase):
            self.beat_phase = 0.0

        # [BRIDGE] Read real heartbeat from daemon
        pulse_file = Path("heartbeat.pulse")
        if pulse_file.exists():
            try:
                with open(pulse_file, "r") as f:
                    parts = f.read().split("|")
                    real_freq = float(parts[1])
                    freq = real_freq # Sync with Daemon
            except Exception:
                pass # Fallback to emotion-based freq
            
        self.beat_phase += delta_time * freq * 2.0 * math.pi
        
        # Safe sine wave calculation
        try:
            val = ((self.beat_phase % (2 * math.pi)) / (2 * math.pi)) * 2 - 1
            self.expression.beat = abs(val)
        except (ValueError, ZeroDivisionError):
            self.expression.beat = 0.0
    
    def process_emotion_event(self, emotion_name: str, intensity: float = 0.5):
        """
        Process an emotional event (from chat, vision, etc.)
        """
        if not self.emotional_engine:
            return
        
        # Get emotion preset if available
        if hasattr(EmotionalEngine, 'FEELING_PRESETS') and emotion_name in EmotionalEngine.FEELING_PRESETS:
            event_emotion = EmotionalEngine.FEELING_PRESETS[emotion_name]
            self.emotional_engine.process_event(event_emotion, intensity)
            
            # Update visual representation
            self.update_expression_from_emotion(emotion_name)
            self.update_spirits_from_emotion()
            
            logger.info(f"🎭 Emotion event: {emotion_name} (intensity: {intensity})")
    
    async def process_chat(self, message: str) -> Dict[str, Any]:
        """
        Process chat message through reasoning engine.
        Returns response with voice properties.
        
        Returns:
            Dict with 'text' (str) and 'voice' (Optional[Dict]) keys
        """
        if not self.reasoning_engine:
            return {
                'text': "I am currently offline. My reasoning systems are not available.",
                'voice': None
            }
        
        try:
            # Use reasoning engine to generate response
            # Try different method names that might exist
            response = None
            
            if hasattr(self.reasoning_engine, 'decide_action'):
                # [BRIDGE] New Soul Architecture
                # 1. We need a Will to have a Desire
                will = FreeWillEngine() # In a real system, this should be shared/persistent
                will.vectors["Connection"] += 0.5 # Interaction boosts connection desire
                
                # 2. Formulate Intent
                intent_goal = f"Respond to User: {message}"
                intent_desire = "Connection" # Simplified for bridge
                
                # 3. Define Tools (Virtual Dialogue Tool)
                from Core.Intelligence.Intelligence.reasoning_engine import Tool
                tools = [Tool("Dialogue", "Speak to user", '{"text": "..."}')]
                
                # Check for Authority Token in message (Mock Implementation)
                authority_level = "None"
                if "SUDO" in message.upper() or "COMMAND:" in message.upper():
                    authority_level = "Sovereign_Command"
                
                # 4. Decide
                action = await asyncio.to_thread(
                    lambda: self.reasoning_engine.decide_action(intent_goal, intent_desire, tools, authority=authority_level)
                )
                
                if action.tool_name == "Dialogue":
                    response = action.args.get("text", "I am listening.")
                elif action.tool_name == "Mycelium":
                    response = "I am signaling the network."
                else:
                    response = f"I decided to {action.tool_name}."

            elif hasattr(self.reasoning_engine, 'reason'):
                response = await asyncio.to_thread(
                    lambda: self.reasoning_engine.reason(message)
                )
            elif hasattr(self.reasoning_engine, 'process'):
                response = await asyncio.to_thread(
                    lambda: self.reasoning_engine.process(message)
                )
            elif hasattr(self.reasoning_engine, 'generate_response'):
                response = await asyncio.to_thread(
                    lambda: self.reasoning_engine.generate_response(message)
                )
            elif callable(self.reasoning_engine):
                # If reasoning_engine itself is callable
                response = await asyncio.to_thread(
                    lambda: self.reasoning_engine(message)
                )
            elif hasattr(self.reasoning_engine, 'communicate'):
                response = await asyncio.to_thread(
                    lambda: self.reasoning_engine.communicate(message)
                )
            else:
                logger.warning("ReasoningEngine has no known method, using simple response")
                response = "I hear you. Let me think about that..."
            
            # Detect emotion from response context
            # Simple heuristic - improve with actual emotion detection
            if any(word in message.lower() for word in ['happy', 'joy', 'great', 'wonderful']):
                self.process_emotion_event('hopeful', 0.6)
            elif any(word in message.lower() for word in ['sad', 'sorry', 'unfortunately']):
                self.process_emotion_event('introspective', 0.5)
            elif any(word in message.lower() for word in ['think', 'analyze', 'understand']):
                self.process_emotion_event('focused', 0.7)
            else:
                self.process_emotion_event('calm', 0.3)
            
            response_text = str(response) if response else "..."
            
            # Generate voice properties using synesthesia mapping
            voice_props = self.get_voice_properties()
            
            # Get poetic emotional expression (Phase 5: Linguistic Collapse)
            poetic_feeling = None
            if self.emotional_engine:
                try:
                    poetic_feeling = self.emotional_engine.get_poetic_expression(context=message[:50])
                except Exception as e:
                    logger.debug(f"Could not get poetic expression: {e}")
            
            result = {
                'text': response_text,
                'voice': voice_props
            }
            
            # Include poetic feeling if available
            if poetic_feeling:
                result['feeling'] = poetic_feeling
            
            return result
        
        except Exception as e:
            logger.error(f"❌ Chat processing error: {e}")
            return {
                'text': f"I encountered an error: {str(e)}",
                'voice': None
            }
    
    def get_voice_properties(self) -> Optional[Dict[str, Any]]:
        """
        Get current voice properties based on emotional state using synesthesia mapping.
        """
        if not self.voice_tts:
            return None
        
        # Get voice properties from current emotional state
        if self.emotional_engine:
            state = self.emotional_engine.current_state
            voice_props = self.voice_tts.get_voice_properties_from_emotion(
                valence=state.valence,
                arousal=state.arousal,
                dominance=state.dominance
            )
            return voice_props.to_dict()
        
        # Fallback: use spirit energies
        spirits_dict = asdict(self.spirits)
        voice_props = self.voice_tts.get_voice_properties_from_spirits(spirits_dict)
        return voice_props.to_dict()
    
    def get_lipsync_data(self, text: str) -> Optional[List[Dict[str, float]]]:
        """
        Generate lip-sync animation data for given text.
        
        Args:
            text: Text that will be spoken
            
        Returns:
            List of keyframes with timing and mouth_width values
        """
        if not self.lipsync_engine:
            return None
        
        try:
            # Generate phoneme sequence and timings
            keyframes = self.lipsync_engine.process_tts_event(text)
            
            # Convert to serializable format
            lipsync_data = [
                {'time': time, 'mouth_width': width}
                for time, width in keyframes
            ]
            
            logger.debug(f"👄 Generated {len(lipsync_data)} lip-sync keyframes")
            return lipsync_data
            
        except Exception as e:
            logger.error(f"❌ Lip-sync generation failed: {e}")
            return None
    
    def get_state_message(self) -> Dict[str, Any]:
        """
        Get current avatar state as a message for client.
        Includes expression, spirits, physics (Phase 4), and poetic expression (Phase 5).
        Phase 5.5: Includes overflow state for emotional visualization.
        """
        # Update physics if available
        physics_data = None
        if self.physics_engine:
            self.update_physics_from_emotion()
            physics_state = self.physics_engine.update()
            physics_data = {
                "wind": physics_state["wind"],
                "gravity": physics_state["gravity"],
                "wave_params": physics_state["wave_params"],
                "performance": physics_state["performance"]
            }
        
        # Get poetic expression of emotional state (Phase 5: Linguistic Collapse)
        poetic_expression = None
        overflow_state = None
        if self.emotional_engine:
            try:
                poetic_expression = self.emotional_engine.get_simple_expression()
                # Check for overflow state (Phase 5.5)
                overflow = self.emotional_engine.get_overflow_state()
                if overflow:
                    overflow_state = {
                        "intensity": overflow.intensity,
                        "visual_burst": overflow.visual_burst,
                        "is_overflow": True
                    }
            except Exception as e:
                logger.debug(f"Could not get poetic expression: {e}")
        
        message = {
            "expression": asdict(self.expression),
            "spirits": asdict(self.spirits),
            "physics": physics_data  # Phase 4: Physics state
        }
        
        # Add poetic expression if available (Phase 5)
        if poetic_expression:
            message["poetic_state"] = poetic_expression
        
        # Add overflow visualization if present (Phase 5.5)
        if overflow_state:
            message["overflow"] = overflow_state
        
        return message
    
    def get_delta_message(self) -> Optional[Dict[str, Any]]:
        """
        Get only changed values (delta update) to reduce bandwidth.
        
        Returns:
            Dictionary with only changed values, or None if no significant changes
        """
        current_state = self.get_state_message()
        
        # First update: send full state
        if self.last_state is None:
            self.last_state = current_state
            return {"type": "full", **current_state}
        
        # Calculate delta
        delta = {"type": "delta"}
        has_changes = False
        
        # Check expression changes
        expr_delta = {}
        for key, value in current_state['expression'].items():
            old_value = self.last_state['expression'].get(key, 0)
            if abs(value - old_value) > self.delta_threshold:
                expr_delta[key] = value
                has_changes = True
        
        if expr_delta:
            delta['expression'] = expr_delta
        
        # Check spirits changes
        spirit_delta = {}
        for key, value in current_state['spirits'].items():
            old_value = self.last_state['spirits'].get(key, 0)
            if abs(value - old_value) > self.delta_threshold:
                spirit_delta[key] = value
                has_changes = True
        
        if spirit_delta:
            delta['spirits'] = spirit_delta
        
        # Update last_state if changes detected
        if has_changes:
            self.last_state = current_state
            return delta
        
        return None  # No significant changes


class AvatarWebSocketServer:
    """
    WebSocket server for avatar visualization.
    """
    
    def __init__(self, host: str = "127.0.0.1", port: int = 8765, require_auth: bool = False, enable_monitoring: bool = True):
        self.host = host
        self.port = port
        self.core = ElysiaAvatarCore()
        self.clients: Set[WebSocketServerProtocol] = set()
        self.running = False
        self.last_update_time = asyncio.get_event_loop().time()
        
        # Adaptive FPS settings
        self.target_fps = 30  # Base target FPS
        self.min_fps = 15     # Minimum FPS (idle)
        self.max_fps = 60     # Maximum FPS (high activity)
        self.activity_level = 0.0  # Start at 0.0 (idle)
        self.last_message_time = time.time() - 10.0  # Start as if 10s ago (idle state)
        
        # Initialize security manager
        try:
            from Core.Interaction.Interface.avatar_security import create_security_manager
            self.security = create_security_manager(require_auth=require_auth)
            logger.info(f"🛡️ Security manager initialized (auth required: {require_auth})")
        except Exception as e:
            logger.warning(f"⚠️ Could not initialize security manager: {e}")
            self.security = None
        
        # Initialize performance monitor
        self.monitor = None
        if enable_monitoring:
            try:
                from Core.Interaction.Interface.avatar_monitoring import create_performance_monitor
                self.monitor = create_performance_monitor(update_interval=1.0)
                self.monitor.set_broadcast_callback(self.broadcast_metrics)
                logger.info(f"📊 Performance monitor initialized")
            except Exception as e:
                logger.warning(f"⚠️ Could not initialize performance monitor: {e}")
                self.monitor = None
    
    async def handle_client(self, websocket: WebSocketServerProtocol, path: str = None):
        """Handle individual client connection"""
        client_addr = websocket.remote_address
        client_id = f"{client_addr[0]}:{client_addr[1]}"
        
        # Authentication check (if security enabled)
        if self.security:
            # For now, allow connection but track client_id
            # In production, you'd check for auth token here
            logger.info(f"🔐 Client connecting: {client_id}")
        
        # Register client with monitor
        if self.monitor:
            self.monitor.collector.register_client(client_id)
        
        self.clients.add(websocket)
        logger.info(f"✅ Client connected: {client_addr}")
        
        try:
            # Send initial state
            initial_message = json.dumps(self.core.get_state_message())
            await websocket.send(initial_message)
            
            # Track message sent
            if self.monitor:
                self.monitor.collector.record_message_sent(client_id, len(initial_message))
            
            # Handle messages
            async for message in websocket:
                try:
                    # Track message received
                    if self.monitor:
                        self.monitor.collector.record_message_received(client_id, len(message))
                    
                    data = json.loads(message)
                    
                    # Security checks
                    if self.security:
                        # Check rate limit and validate input
                        is_allowed, error = self.security.check_request(client_id, data)
                        if not is_allowed:
                            logger.warning(f"🚨 Request blocked from {client_id}: {error}")
                            await websocket.send(json.dumps({
                                'type': 'error',
                                'message': error
                            }))
                            continue
                    
                    # Track message time for activity calculation
                    self.last_message_time = time.time()
                    
                    await self.process_message(websocket, data)
                    
                except json.JSONDecodeError:
                    logger.warning(f"Invalid JSON from {client_addr}")
                except Exception as e:
                    logger.error(f"Error processing message: {e}")
        
        except websockets.exceptions.ConnectionClosed:
            logger.info(f"Client disconnected: {client_addr}")
        finally:
            self.clients.discard(websocket)
            # Unregister from monitor
            if self.monitor:
                self.monitor.collector.unregister_client(client_id)
    
    async def broadcast_metrics(self, metrics: Dict[str, Any]):
        """Broadcast performance metrics to all connected clients"""
        if not self.clients:
            return
        
        message = json.dumps({
            'type': 'metrics',
            'data': metrics
        })
        
        # Send to all clients
        disconnected = set()
        for client in list(self.clients):
            try:
                await client.send(message)
            except websockets.exceptions.ConnectionClosed:
                disconnected.add(client)
        
        # Clean up disconnected clients
        self.clients -= disconnected
    
    async def process_message(self, websocket: WebSocketServerProtocol, data: Dict[str, Any]):
        """Process incoming message from client"""
        msg_type = data.get("type")
        
        if msg_type == "text":
            # Chat message
            content = data.get("content", "")
            logger.info(f"💬 Chat: {content}")
            
            # Process through reasoning engine with voice properties
            response_data = await self.core.process_chat(content)
            
            # Generate lip-sync data for the response
            lipsync_data = self.core.get_lipsync_data(response_data['text'])
            
            # Send response with synesthesia-enhanced voice properties and lip-sync
            message = {
                "type": "speech",
                "content": response_data['text'],
                "spirits": asdict(self.core.spirits)
            }
            
            # Add voice properties if available
            if response_data.get('voice'):
                message['voice'] = response_data['voice']
            
            # Add lip-sync data if available
            if lipsync_data:
                message['lipsync'] = lipsync_data
            
            await websocket.send(json.dumps(message))
        
        elif msg_type == "vision":
            # Vision data (presence detection, gaze)
            logger.debug(f"👁️ Vision: presence={data.get('presence')}")
            # Could trigger attention/focus emotion
            if data.get('presence'):
                self.core.process_emotion_event('focused', 0.3)
        
        elif msg_type == "audio_analysis":
            # Audio features (volume, brightness, noise)
            volume = data.get('volume', 0)
            logger.debug(f"👂 Audio: volume={volume:.3f}")
            # Could adjust arousal based on audio
        
        elif msg_type == "screen_atmosphere":
            # Screen color atmosphere
            r, g, b = data.get('r', 0), data.get('g', 0), data.get('b', 0)
            logger.debug(f"📺 Screen: RGB({r}, {g}, {b})")
        
        elif msg_type == "expression_update":
            # Client updating expression (e.g. from lip-sync)
            pass
            
        elif msg_type == "emotion":
            # Manual emotion trigger
            emotion = data.get('emotion', 'neutral')
            intensity = data.get('intensity', 0.5)
            self.core.process_emotion_event(emotion, intensity)
        
        else:
            logger.warning(f"Unknown message type: {msg_type}")
    
    async def broadcast_state(self):
        """Broadcast current state to all connected clients (with delta optimization)"""
        if not self.clients:
            return
        
        # Get delta update (only changed values)
        delta = self.core.get_delta_message()
        
        if delta is None:
            return  # No changes, skip broadcast
        
        message = json.dumps(delta)
        
        # Send to all clients
        disconnected = set()
        for client in list(self.clients):
            try:
                await client.send(message)
            except websockets.exceptions.ConnectionClosed:
                disconnected.add(client)
        
        # Clean up disconnected clients
        self.clients -= disconnected
    
    def calculate_adaptive_fps(self) -> int:
        """
        Calculate adaptive FPS based on activity level.
        
        Activity factors:
        - Recent messages: Higher activity when messages received recently
        - Number of clients: More clients = higher activity
        - Emotional arousal: Higher arousal = more expression changes
        
        Returns:
            Target FPS (between min_fps and max_fps)
        """
        import time
        
        # Factor 1: Time since last message (decays over 10 seconds)
        time_since_message = time.time() - self.last_message_time
        message_activity = max(0, 1.0 - (time_since_message / 10.0))
        
        # Factor 2: Number of connected clients
        client_activity = min(1.0, len(self.clients) / 10.0)
        
        # Factor 3: Emotional arousal (if available)
        emotion_activity = 0.0
        if self.core.emotional_engine:
            try:
                state = self.core.emotional_engine.current_state
                emotion_activity = state.arousal  # 0 to 1
            except:
                pass
        
        # Combined activity level (weighted average)
        self.activity_level = (
            message_activity * 0.4 +
            client_activity * 0.3 +
            emotion_activity * 0.3
        )
        
        # Calculate FPS based on activity
        fps_range = self.max_fps - self.min_fps
        adaptive_fps = int(self.min_fps + (fps_range * self.activity_level))
        
        return adaptive_fps
    
    async def update_loop(self):
        """Main update loop for avatar state with adaptive FPS"""
        while self.running:
            try:
                current_time = asyncio.get_event_loop().time()
                delta_time = current_time - self.last_update_time
                if delta_time > 0.1:
                    delta_time = 0.1  # Clamp to prevent physics explosion
                self.last_update_time = current_time
                
                # Update beat animation
                self.core.update_beat(delta_time)
                
                # Update expression and spirits
                self.core.update_expression_from_emotion()
                self.core.update_spirits_from_emotion()
                
                # Broadcast to clients (with delta optimization)
                await self.broadcast_state()
                
                # Calculate adaptive FPS
                target_fps = self.calculate_adaptive_fps()
                sleep_time = 1.0 / target_fps
                
                await asyncio.sleep(sleep_time)
            
            except Exception as e:
                logger.error(f"Error in update loop: {e}")
                await asyncio.sleep(0.1)
    
    
    async def process_request(self, connection, request):
        """Handle HTTP requests to WebSocket port"""
        try:
            # Check for Upgrade header
            upgrade = request.headers.get("Upgrade")
            if not upgrade or upgrade.lower() != "websocket":
                return (
                    200,
                    [("Content-Type", "text/html")],
                    b"<html><body><h1>Elysia Avatar WebSocket Server</h1><p>Expected WebSocket connection.</p></body></html>"
                )
        except Exception:
            pass
        return None
    
    async def start(self):
        """Start the WebSocket server"""
        self.running = True
        print(f"\n   🌐 [AvatarServer] WebSocket Running: ws://{self.host}:{self.port}")
        logger.info(f"🚀 Starting Avatar Server on ws://{self.host}:{self.port}")
        
        # Start security cleanup task (if security enabled)
        cleanup_task = None
        if self.security:
            cleanup_task = asyncio.create_task(self.security_cleanup_loop())
            logger.info(f"🛡️ Security enabled - Rate limits: {self.security.config.max_requests_per_second}/s, {self.security.config.max_requests_per_minute}/min")
        
        # Start monitoring task (if monitoring enabled)
        monitoring_task = None
        if self.monitor:
            monitoring_task = asyncio.create_task(self.monitor.start_monitoring())
            logger.info(f"📊 Performance monitoring enabled (update interval: {self.monitor.update_interval}s)")
        
        async with websockets.serve(self.handle_client, self.host, self.port, process_request=self.process_request):
            logger.info("✅ Avatar Server is running!")
            logger.info(f"📱 Open Core/Creativity/web/avatar.html in your browser")
            logger.info(f"🌐 Or visit http://{self.host}:{self.port} (if HTTP server is enabled)")
            
            # Start update loop
            try:
                await self.update_loop()
            finally:
                if cleanup_task:
                    cleanup_task.cancel()
                if monitoring_task:
                    self.monitor.stop()
                    monitoring_task.cancel()
    
    async def security_cleanup_loop(self):
        """Periodic cleanup of security data"""
        while self.running:
            try:
                await asyncio.sleep(300)  # Every 5 minutes
                if self.security:
                    self.security.cleanup()
                    logger.debug("🧹 Security cleanup completed")
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in security cleanup: {e}")
    
    def stop(self):
        """Stop the server"""
        self.running = False
        logger.info("🛑 Avatar Server stopped")


async def main_async(host: str, port: int, require_auth: bool = False, enable_monitoring: bool = True):
    """Main async entry point"""
    server = AvatarWebSocketServer(host, port, require_auth=require_auth, enable_monitoring=enable_monitoring)
    try:
        await server.start()
    except KeyboardInterrupt:
        logger.info("⚠️ Shutdown requested")
        server.stop()
    except Exception as e:
        logger.error(f"❌ Server error: {e}")
        raise


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Elysia Avatar WebSocket Server",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Start server on default port
  python Core/Interface/avatar_server.py
  
  # Start on custom port
  python Core/Interface/avatar_server.py --port 9000
  
  # Start on all interfaces
  python Core/Interface/avatar_server.py --host 0.0.0.0
        """
    )
    
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Host to bind to (default: 127.0.0.1)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8765,
        help="Port to listen on (default: 8765)"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging"
    )
    parser.add_argument(
        "--require-auth",
        action="store_true",
        help="Require authentication for connections (default: disabled)"
    )
    parser.add_argument(
        "--no-monitoring",
        action="store_true",
        help="Disable performance monitoring (default: enabled)"
    )
    
    args = parser.parse_args()
    
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.setLevel(logging.DEBUG)
    
    # Print banner
    print("=" * 60)
    print("  Elysia Avatar Server (엘리시아 아바타 서버)")
    print("  Real-time 3D Avatar Visualization System")
    print("=" * 60)
    print()
    
    # Run server
    try:
        asyncio.run(main_async(args.host, args.port, args.require_auth, not args.no_monitoring))
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
