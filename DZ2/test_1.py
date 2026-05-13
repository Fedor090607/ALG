import unittest
import numpy as np
from algorithmizationDZ2 import simpson_rule, f

class TestSimpsonMethod(unittest.TestCase):

    def test_simpson_n10(self):
        result = simpson_rule(f, 2, 4, 10)
        self.assertAlmostEqual(result, 2.0, places=7)

    def test_simpson_n20(self):
        result = simpson_rule(f, 2, 4, 20)
        self.assertAlmostEqual(result, 2.0, places=7)

    def test_simpson_n50(self):
        result = simpson_rule(f, 2, 4, 50)
        self.assertAlmostEqual(result, 2.0, places=7)


if __name__ == "__main__":
    unittest.main()
