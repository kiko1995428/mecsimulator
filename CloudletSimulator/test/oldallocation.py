"""
test/allocation.py
coding          : utf-8
Author          : Kouhei Osaki
Created         : 2017/07/04
Last-Modified   : 2017/07/11
Version         : 1.0.1
Description     : simulator/allocation.pyのテストプログラム
"""
import unittest
from simulator import oldutility, olddataset, oldallocation
from simulator.oldmodels import Device, Point, Allocation


class AllocationTestCase(unittest.TestCase):
    def setUp(self):
        self.all_time_cloudlets = oldutility.create_all_time_cloudlets(t_len=5, x_len=5, y_len=5, max_resource=5)
        d1 = Device(name="d1", startup_time=0, plan=[Point(0, 0), Point(0, 1), Point(0, 2)])
        d1.use_resource = 5
        d2 = Device(name="d2", startup_time=1, plan=[Point(0, 0), Point(0, 1), Point(0, 2)])
        d2.use_resource = 5
        d3 = Device(name="d3", startup_time=1, plan=[Point(1, 0), Point(2, 0), Point(3, 0)])
        d3.use_resource = 5
        d4 = Device(name="d4", startup_time=1, plan=[Point(0, 0), Point(0, 1), Point(0, 2)])
        d4.use_resource = 5
        self.devices = [d1, d2, d3, d4]

    def test_simple_ffd(self):
        ap = oldallocation.decreasing(self.all_time_cloudlets, self.devices)
        self.assertEqual(ap["d1"][0], Allocation(0, 0, 0))
        self.assertEqual(ap["d1"][1], Allocation(0, 1, 0))
        self.assertEqual(ap["d1"][2], Allocation(0, 2, 0))
        self.assertEqual(ap["d2"][0], None)
        self.assertEqual(ap["d2"][1], Allocation(0, 0, 0))
        self.assertEqual(ap["d2"][2], Allocation(0, 1, 0))
        self.assertEqual(ap["d2"][3], Allocation(0, 2, 0))
        self.assertEqual(ap["d4"][0], None)
        self.assertEqual(ap["d4"][1], Allocation(0, 0, -1))
        self.assertEqual(ap["d4"][2], Allocation(0, 1, -1))
        self.assertEqual(ap["d4"][3], Allocation(0, 2, -1))

    def test_nearby_searchable_ffd(self):
        for cloudlets in self.all_time_cloudlets:
            for row in cloudlets:
                for index, c in enumerate(row):
                    c.resource = 5 + index
        ap = oldallocation.ffd(self.all_time_cloudlets, self.devices)
        self.assertEqual(self.all_time_cloudlets[0][0][0].empty_resource, 0)
        self.assertEqual(self.all_time_cloudlets[1][1][0].empty_resource, 0)
        self.assertEqual(self.all_time_cloudlets[2][2][0].empty_resource, 0)
        self.assertEqual(self.all_time_cloudlets[1][0][0].empty_resource, 0)
        self.assertEqual(self.all_time_cloudlets[2][1][0].empty_resource, 0)
        self.assertEqual(self.all_time_cloudlets[3][2][0].empty_resource, 0)
        self.assertEqual(self.all_time_cloudlets[1][0][1].empty_resource, 1)
        self.assertEqual(self.all_time_cloudlets[2][0][2].empty_resource, 2)
        self.assertEqual(self.all_time_cloudlets[3][0][3].empty_resource, 3)
        self.assertEqual(self.all_time_cloudlets[1][0][2].empty_resource, 2)
        self.assertEqual(self.all_time_cloudlets[2][1][1].empty_resource, 1)
        self.assertEqual(self.all_time_cloudlets[3][2][1].empty_resource, 1)
        self.assertEqual(ap["d1"][0], Allocation(0, 0, 0))
        self.assertEqual(ap["d1"][1], Allocation(0, 1, 0))
        self.assertEqual(ap["d1"][2], Allocation(0, 2, 0))
        self.assertEqual(ap["d2"][0], None)
        self.assertEqual(ap["d2"][1], Allocation(0, 0, 0))
        self.assertEqual(ap["d2"][2], Allocation(0, 1, 0))
        self.assertEqual(ap["d2"][3], Allocation(0, 2, 0))
        self.assertEqual(ap["d3"][0], None)
        self.assertEqual(ap["d3"][1], Allocation(1, 0, 0))
        self.assertEqual(ap["d3"][2], Allocation(2, 0, 0))
        self.assertEqual(ap["d3"][3], Allocation(3, 0, 0))
        self.assertEqual(ap["d4"][0], None)
        self.assertEqual(ap["d4"][1], Allocation(2, 0, 2))
        self.assertEqual(ap["d4"][2], Allocation(1, 1, 1))
        self.assertEqual(ap["d4"][3], Allocation(1, 2, 1))
