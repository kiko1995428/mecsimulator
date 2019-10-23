"""
test/utility/points.py
coding          : utf-8
Author          : Kouhei Osaki
Created         : 2017/07/14
Last-Modified   : 2017/07/14
Version         : 1.0.1
Description     : utilyty/pointのテストプログラム 
"""
from simulator.oldmodels import Point
from simulator.utility import point
import unittest


class PointUtilityTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_adjacency_01(self):
        p1 = Point(0, 0)
        p2 = Point(0, 1)
        self.assertTrue(point.adjacency(p1, p2))

    def test_adjacency_02(self):
        p1 = Point(0, 0)
        p2 = Point(1, 0)
        self.assertTrue(point.adjacency(p1, p2))

    def test_adjacency_03(self):
        p1 = Point(0, 0)
        p2 = Point(0, -1)
        self.assertTrue(point.adjacency(p1, p2))

    def test_adjacency_04(self):
        p1 = Point(0, 0)
        p2 = Point(-1, 0)
        self.assertTrue(point.adjacency(p1, p2))

    def test_adjacency_05(self):
        p1 = Point(0, 0)
        p2 = Point(1, 1)
        self.assertFalse(point.adjacency(p1, p2))

    def test_continuity_01(self):
        p1 = Point(0, 0)
        p2 = Point(0, 1)
        p3 = Point(1, 1)
        p4 = Point(2, 1)
        p5 = Point(2, 0)
        p6 = Point(1, 0)
        p_list = [p1, p2, p3, p4, p5, p6]
        self.assertTrue(point.continuity(p_list))

    def test_continuity_02(self):
        p1 = Point(0, 0)
        p2 = Point(1, 1)
        p3 = Point(2, 1)
        p4 = Point(3, 1)
        p5 = Point(2, 0)
        p6 = Point(1, 0)
        p_list = [p1, p2, p3, p4, p5, p6]
        self.assertFalse(point.continuity(p_list))

    def test_distance_01(self):
        p1 = Point(0, 0)
        p2 = Point(5, 3)
        self.assertEqual(8, point.distance(p1, p2))

    def test_distance_02(self):
        p1 = Point(0, 0)
        p2 = Point(-3, -5)
        self.assertEqual(8, point.distance(p1, p2))

    def test_distance_03(self):
        p1 = Point(0, 0)
        p2 = Point(0, 0)
        self.assertEqual(0, point.distance(p1, p2))

    def test_extract_01(self):
        p = Point(0, 0)
        p_list = point.extract(p, 1)
        exp = [Point(0, 0), Point(-1, 0), Point(0, -1), Point(1, 0), Point(0, 1)]
        self.assertEqual(5, len(p_list))
        for ep in exp:
            self.assertTrue(ep in p_list)

    def test_extract_02(self):
        p = Point(0, 0)
        p_list = point.extract(p, 1, d_min=1)
        exp = [Point(-1, 0), Point(0, -1), Point(1, 0), Point(0, 1)]
        self.assertEqual(4, len(p_list))
        for ep in exp:
            self.assertTrue(ep in p_list)

    def test_extract_03(self):
        p = Point(0, 0)
        p_list = point.extract(p, 3, d_min=3)
        exp = [Point(3, 0), Point(2, 1), Point(1, 2), Point(0, 3),
               Point(-3, 0), Point(-2, -1), Point(-1, -2), Point(0, -3),
               Point(-2, 1), Point(-1, 2), Point(2, -1), Point(1, -2)]
        self.assertEqual(12, len(p_list), msg=p_list)
        for ep in exp:
            self.assertTrue(ep in p_list)

    def test_random_two_points_01(self):
        p1, p2 = point.random_two_point(3, Point(0, 0), Point(5, 5))
        self.assertEqual(3, point.distance(p1, p2))

    def test_random_two_points_02(self):
        self.assertRaises(Exception, lambda: point.random_two_point(3, Point(0, 0), Point(0, 0)))

    def test_route_01(self):
        p1 = Point(0, 0)
        p2 = Point(2, 2)
        r = point.route(p1, p2)
        self.assertTrue(point.continuity(r))
        self.assertEqual(5, len(r))
