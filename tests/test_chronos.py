import unittest
from elysia_engine.world import World
from elysia_engine.chronos import DreamSystem
from elysia_engine.consciousness import GlobalConsciousness
from elysia_engine.entities import Entity
from elysia_engine.tensor import SoulTensor

class TestChronos(unittest.TestCase):
    def setUp(self):
        self.world = World()
        self.chronos = DreamSystem()
        self.conscientia = GlobalConsciousness()
        self.world.add_system(self.chronos)
        self.world.add_system(self.conscientia)

        # Add an entity
        self.ent = Entity(
            id="test_ent",
            soul=SoulTensor(amplitude=10, frequency=1.0, phase=0.0)
        )
        self.world.add_entity(self.ent)

    def test_prophecy_is_distinct(self):
        # Prophecy should return a NEW world instance
        future = self.chronos.prophecy(self.world, horizon=10)

        self.assertNotEqual(id(self.world), id(future))
        self.assertNotEqual(id(self.world.entities["test_ent"]), id(future.entities["test_ent"]))

    def test_prophecy_evolves_state(self):
        # Initial phase is 0.0
        # After 10 ticks, phase should increase: phi += freq * dt
        # 10 * 1.0 = 10.0. 10.0 % 2pi = ~3.71

        future = self.chronos.prophecy(self.world, horizon=10)
        future_ent = future.entities["test_ent"]

        self.assertNotAlmostEqual(future_ent.soul.phase, 0.0)
        self.assertTrue(future_ent.soul.phase > 0)

        # Original world should NOT change
        self.assertEqual(self.world.entities["test_ent"].soul.phase, 0.0)

    def test_analyze_entropy(self):
        # Single entity aligned with itself -> Entropy 0?
        # GlobalConsciousness logic: if count=1, alignment=1.0, entropy=0.0
        entropy = self.chronos.analyze_entropy(self.world)
        self.assertEqual(entropy, 0.0)

if __name__ == "__main__":
    unittest.main()
