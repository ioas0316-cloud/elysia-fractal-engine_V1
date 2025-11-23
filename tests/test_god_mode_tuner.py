from elysia_engine.world import World
from examples.god_mode_tuner import apply_settings  # type: ignore


def test_apply_settings_sets_constants():
    world = World()
    apply_settings(world, gravity=2.5, time_scale=0.5, torsion_angle=1.0, torsion_axis="x")
    assert world.physics is not None
    assert world.physics.gravity_constant == 2.5
    assert world.physics.time_scale == 0.5
    assert world.physics.spacetime_torsion is not None


def test_apply_settings_unsets_torsion():
    world = World()
    apply_settings(world, gravity=None, time_scale=None, torsion_angle=0.0, torsion_axis="y")
    assert world.physics is not None
    assert world.physics.spacetime_torsion is None
