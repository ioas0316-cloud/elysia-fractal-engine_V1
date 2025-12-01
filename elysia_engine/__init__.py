from .entities import Entity
from .physics import PhysicsWorld, PhysicsState
from .tensor import SoulTensor
from .world import World
from .config import ElysiaConfig, get_config, set_config
from .exceptions import (
    ElysiaError,
    TensorError,
    PhysicsError,
    EntityError,
    ConfigurationError,
    ConsciousnessError,
)
from .logging_config import get_logger, configure_root_logger

# Core Structure from Original Elysia
from .yggdrasil import Yggdrasil, Realm, YggdrasilNode, get_yggdrasil
from .ether import Ether, Wave, WavePhase, Frequency, get_ether, emit_wave

__all__ = [
    # Core classes
    "Entity",
    "PhysicsWorld",
    "PhysicsState",
    "SoulTensor",
    "World",
    # Configuration
    "ElysiaConfig",
    "get_config",
    "set_config",
    # Exceptions
    "ElysiaError",
    "TensorError",
    "PhysicsError",
    "EntityError",
    "ConfigurationError",
    "ConsciousnessError",
    # Logging
    "get_logger",
    "configure_root_logger",
    # Core Structure (from Original Elysia)
    "Yggdrasil",
    "Realm",
    "YggdrasilNode",
    "get_yggdrasil",
    "Ether",
    "Wave",
    "WavePhase",
    "Frequency",
    "get_ether",
    "emit_wave",
]
