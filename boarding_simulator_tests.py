import unittest
from boarding_simulator import *


class BoardingTests(unittest.TestCase):
    """Test!"""
    def test_plane_instantiation(self):
        num_rows = 10
        plane = instantiate_plane(num_rows)
        self.assertEqual(len(plane), num_rows)

    

if __name__ == '__main__':
    unittest.main()
