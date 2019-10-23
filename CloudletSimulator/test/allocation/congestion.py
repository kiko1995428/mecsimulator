import unittest
from simulator.allocation import congestion
from simulator.model.device import Device
from simulator.model.point import Point


class TestAllocationCongestion(unittest.TestCase):
    def setUp(self):
        self.devices = [Device("d1", plan=[Point(0, 0)]), Device("d2", plan=[Point(2, 1)])]
        self.devices[0].use_resource = 2
        self.devices[1].use_resource = 3
        pass

    def test_create_congestion_map_01(self):
        map = congestion.create_congestion_map(0, 3, 3, self.devices, 2)
        self.assertEqual(map[0][0], 2, msg="(0, 0)")
        self.assertEqual(map[0][1], 5, msg="(1, 0)")
        self.assertEqual(map[0][2], 5, msg="(2, 0)")
        self.assertEqual(map[1][0], 5, msg="(0, 1)")
        self.assertEqual(map[1][1], 5, msg="(1, 1)")
        self.assertEqual(map[1][2], 3, msg="(2, 1)")
        self.assertEqual(map[2][0], 2, msg="(0, 2)")
        self.assertEqual(map[2][1], 3, msg="(1, 2)")
        self.assertEqual(map[2][2], 3, msg="(2, 2)")
