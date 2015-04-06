import unittest
from boarding_simulator import *


class BoardingTests(unittest.TestCase):
    """Test!"""
    def test_plane_instantiation_small(self):
        num_rows = 10
        plane = instantiate_plane(num_rows)
        self.assertEqual(len(plane), num_rows + 1)

    def test_plane_instantiation_large(self):
        num_rows = 100
        plane = instantiate_plane(num_rows)
        self.assertEqual(len(plane), num_rows + 1)

    def test_really_small_queue(self):
        queue = [Passenger(2, 0)]
        plane = instantiate_plane(2)
        self.assertEqual(simulation(queue, plane), 3)

    def test_kinda_small_queue(self):
        queue = [Passenger(1, 0), Passenger(2, 0)]
        plane = instantiate_plane(2)
        self.assertEqual(simulation(queue, plane), 4)

    def test_other_kinda_small_queue(self):
        queue = [Passenger(2, 0), Passenger(1, 0)]
        plane = instantiate_plane(2)
        self.assertEqual(simulation(queue, plane), 3)

    def test_small_queue_with_luggage_time(self):
        queue = [Passenger(2, 1), Passenger(2, 1)]
        plane = instantiate_plane(2)
        self.assertEqual(simulation(queue, plane), 6)

    def test_large_queue_with_luggage_time(self):
        queue = [[Passenger(i, 1) for _ in range(6)] for i in range(1, 101)]
        # Flattening the passenger queue
        queue = [passenger for chunk in queue for passenger in chunk]
        queue.reverse()
        plane = instantiate_plane(100)
        self.assertEqual(simulation(queue, plane), 100)

    def test_big_queue_big_plane_all_same_row(self):
        queue = [Passenger(100, 1) for _ in range(600)]
        plane = instantiate_plane(100)
        self.assertEqual(simulation(queue, plane), 1300)

    def test_big_queue_small_plane_all_same_row(self):
        queue = [Passenger(3, 1) for _ in range(600)]
        plane = instantiate_plane(3)
        self.assertEqual(simulation(queue, plane), 1203)

if __name__ == '__main__':
    unittest.main()
