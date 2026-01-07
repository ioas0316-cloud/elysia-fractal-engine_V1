import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Core.Orchestra.conductor import Conductor, Instrument, Tempo, Mode

class TestSovereigntyUnified(unittest.TestCase):
    def test_refusal_logic(self):
        c = Conductor()
        c.register_instrument(Instrument("Logic", "Brain", lambda **k: "OK"))

        # Minor + Allegro = Refusal
        c.set_intent(mode=Mode.MINOR, tempo=Tempo.ALLEGRO)
        res = c.conduct_solo("Logic")

        self.assertIsInstance(res, dict)
        self.assertEqual(res["status"], "refused")

if __name__ == '__main__':
    unittest.main()
