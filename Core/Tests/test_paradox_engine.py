
import unittest
import sys
import os

# Ensure the root directory is in the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from Core.Intelligence.Reasoning.paradox_engine import ParadoxEngine, ResolutionStrategy, ParadoxState

class TestParadoxEngine(unittest.TestCase):
    def setUp(self):
        self.engine = ParadoxEngine()

    def test_paradox_lifecycle(self):
        # 1. Inject Paradox
        paradox = self.engine.introduce_paradox("I want to be free", "I need to be safe")
        self.assertIsInstance(paradox, ParadoxState)
        self.assertEqual(paradox.tension, 0.8) # Default tension

        # 2. Resolve Paradox
        resolved = self.engine.resolve(paradox.id)

        # 3. Verify Resolution
        self.assertIsNotNone(resolved.synthesis_result)
        self.assertTrue(resolved.strategy in [ResolutionStrategy.SYNTHESIS, ResolutionStrategy.ACCEPTANCE])

        # 4. Check History
        self.assertEqual(len(self.engine.active_paradoxes), 0)
        self.assertEqual(len(self.engine.resolved_history), 1)

    def test_synthesis_logic(self):
        # Test specific synthesis archetype
        result = self.engine._synthesize("freedom", "structure")
        self.assertIn("Creative Discipline", result)

if __name__ == '__main__':
    unittest.main()
