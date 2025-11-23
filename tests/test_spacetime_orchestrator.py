import math

from elysia_engine.physics import PhysicsWorld, HolographicBoundary, Attractor
from elysia_engine.world import World
from elysia_engine.entities import Entity
from elysia_engine.tensor import SoulTensor
from elysia_engine.systems.spacetime import SpacetimeOrchestrator
from elysia_engine.consciousness import GlobalConsciousness
from elysia_engine.math_utils import Vector3


def test_holographic_boundary_influences_potential():
    boundary = HolographicBoundary.spherical_shell(radius=5.0, resolution=4, base_potential=-10.0)
    phys = PhysicsWorld()
    phys.configure_holographic_boundary(boundary)

    center_potential = phys.calculate_potential(Vector3(0, 0, 0))
    assert center_potential < -5.0

    phys.add_attractor(Attractor(id="core", position=Vector3(2, 0, 0), mass=50))
    boosted = phys.calculate_potential(Vector3(0, 0, 0))
    assert boosted < center_potential


def test_spacetime_orchestrator_adjusts_constants():
    world = World()
    phys = PhysicsWorld()
    world.physics = phys

    gc = GlobalConsciousness(physics=phys)
    orchestrator = SpacetimeOrchestrator(physics=phys, entropy_threshold=0.1, cooldown=1)

    world.add_system(gc)
    world.add_system(orchestrator)

    e1 = Entity(id="a", soul=SoulTensor(amplitude=10, frequency=10, phase=0.0))
    e2 = Entity(id="b", soul=SoulTensor(amplitude=10, frequency=10, phase=math.pi))
    world.add_entity(e1)
    world.add_entity(e2)

    # Run a few ticks to trigger orchestration
    initial_g = phys.gravity_constant
    initial_time_scale = phys.time_scale
    for _ in range(3):
        world.step()

    assert phys.gravity_constant > initial_g
    assert phys.time_scale < initial_time_scale
