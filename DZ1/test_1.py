import unittest
from algorithmizationDZ1 import test  


class TestDictDelete(unittest.TestCase):

    def test_time_positive(self):
        t = test(1000)
        self.assertTrue(t > 0)

    def test_time_type(self):
        t = test(1000)
        self.assertEqual(type(t), int)

    def test_key_error(self):
        d = {1: 1}
        with self.assertRaises(KeyError):
            del d[2]

if __name__ == "__main__":
    unittest.main()
