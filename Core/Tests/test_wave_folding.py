import unittest
import sys
import os

# Add project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Core.Foundation.Wave.wave_folding import SpaceUnfolder

class TestWaveFolding(unittest.TestCase):
    def setUp(self):
        self.L = 10.0
        self.unfolder = SpaceUnfolder(self.L)

    def test_fold_simple(self):
        """Test basic folding (0 to L)."""
        # x=5 (Inside) -> 5
        self.assertAlmostEqual(self.unfolder.fold(5.0), 5.0)
        
    def test_fold_reflection(self):
        """Test first reflection (L to 2L)."""
        # x=12 (2 units past L=10) -> Should bounce back to 8
        self.assertAlmostEqual(self.unfolder.fold(12.0), 8.0)
        
    def test_fold_multi(self):
        """Test multiple reflections."""
        # x=25 (2 reflections: 10->20, 20->30)
        # 0-10: normal
        # 10-20: mirrored (x-10 -> 10-(x-10) = 20-x)
        # 20-30: normal (20-30 -> x-20)
        # x=25 -> 5
        self.assertAlmostEqual(self.unfolder.fold(25.0), 5.0)

    def test_straight_path_calculation(self):
        """Test the logic of calculating distance in mirror world."""
        # Start=2, Target=8
        # Direct: 8-2 = 6
        self.assertAlmostEqual(self.unfolder.calculate_straight_path(2, 8, 0), 6.0)
        
        # 1st Reflection (Bounce off Right Wall):
        # Target at 8. Bounce off wall at 10.
        # Path: 2 -> 10 -> 8
        # Distance: (10-2) + (10-8) = 8 + 2 = 10
        # Formula: (1*L + (L-Target)) - Start ?? No, check logic.
        # Mirror 1 Formula (Odd): ((n+1)L - Target) - Start
        # ((0+1)*10 - 8) - 2 = (20 - 8) - 2 ??? No.
        # My formula in code:
        # if odd: ((n+1)L) - target
        # n=1 (1 reflection, right wall)
        # ((2)10) - 8 = 12.
        # 12 - 2 (start) = 10. Correct.
        self.assertAlmostEqual(self.unfolder.calculate_straight_path(2, 8, 1), 10.0)

if __name__ == '__main__':
    unittest.main()
