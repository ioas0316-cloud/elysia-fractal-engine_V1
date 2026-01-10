from .math_utils import Vector3, Vector4, Quaternion, Rotor
from .tensor import SoulTensor
from .field import FieldSystem, FieldNode
from .entities import Entity, Persona, PhysicsState
from .physics import PhysicsWorld
from .world import World
from .identity import ElysiaIdentity
from .adapter import ElysiaBridge
from .hypersphere import HypersphereMemory, TesseractCoord, HypersphericalCoord, HyperCosmos
from .consciousness import GlobalConsciousness

__all__ = [
    "Vector3", "Vector4", "Quaternion", "Rotor",
    "SoulTensor",
    "FieldSystem", "FieldNode",
    "PhysicsWorld", "PhysicsState",
    "Entity", "Persona",
    "World",
    "ElysiaIdentity",
    "ElysiaBridge",
    "HypersphereMemory", "TesseractCoord", "HypersphericalCoord", "HyperCosmos",
    "GlobalConsciousness"
]
