from typing import Dict, List, Any, Callable
import logging

logger = logging.getLogger("VirtualReality")

class VirtualEntity:
    """
    An object within the Simulated Reality.
    Does not strictly follow standard physics unless the Space aims for it.
    """
    def __init__(self, name: str, mass: float = 1.0, x: float = 0.0, y: float = 0.0):
        self.name = name
        self.mass = mass
        self.position = {'x': x, 'y': y}
        self.velocity = {'x': 0.0, 'y': 0.0}
        self.properties: Dict[str, Any] = {} # e.g., 'charge', 'spirit', 'color'

    def __repr__(self):
        return f"[{self.name}] Pos({self.position['x']:.2f}, {self.position['y']:.2f}) Vel({self.velocity['x']:.2f}, {self.velocity['y']:.2f})"

class VirtualSpace:
    """
    [Simulated Reality]
    "The Sandbox of God"
    
    A space where laws are mutable variables.
    Elysia can say "Gravity is Up" and it becomes so.
    """
    
    def __init__(self, space_name: str = "Genesis_01"):
        self.name = space_name
        self.laws: Dict[str, float] = {}
        self.entities: List[VirtualEntity] = []
        self.time_step = 0
        
        # Default Laws (can be overridden)
        self.declare_law("GRAVITY_Y", -9.8) # Earth-like standard
        self.declare_law("FRICTION", 0.0)   # Vacuum
        
        logger.info(f"🌌 VirtualSpace '{space_name}' created.")

    def declare_law(self, law_name: str, value: float):
        """Redefines a fundamental constant of this universe."""
        self.laws[law_name] = value
        logger.info(f"📜 Law Declared: {law_name} = {value}")

    def spawn(self, entity: VirtualEntity):
        """Brings an entity into existence."""
        self.entities.append(entity)
        logger.info(f"✨ Spawned: {entity.name}")

    def tick(self, dt: float = 1.0):
        """Advances the simulation by delta_time (dt)."""
        self.time_step += 1
        
        gravity_y = self.laws.get("GRAVITY_Y", 0.0)
        friction = self.laws.get("FRICTION", 0.0)
        
        for entity in self.entities:
            # 1. Apply Forces (F = ma -> a = F/m)
            # For simplicity in this v1, Gravity is an acceleration, not a force.
            accel_x = 0.0
            accel_y = gravity_y 
            
            # 2. Update Velocity (v = u + at)
            entity.velocity['x'] += accel_x * dt
            entity.velocity['y'] += accel_y * dt
            
            # Apply Friction (Damping)
            if friction > 0:
                entity.velocity['x'] *= (1.0 - friction)
                entity.velocity['y'] *= (1.0 - friction)
            
            # 3. Update Position (s = s + vt)
            entity.position['x'] += entity.velocity['x'] * dt
            entity.position['y'] += entity.velocity['y'] * dt
            
        logger.debug(f"⏳ Tick {self.time_step}: {self.entities}")

    def get_entity_state(self, name: str) -> str:
        for e in self.entities:
            if e.name == name:
                return str(e)
        return "Entity Not Found"
