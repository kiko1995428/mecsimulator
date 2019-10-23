"""
test/utility/cloudlets.py
coding          : utf-8
Author          : Kouhei Osaki
Created         : 2017/07/14
Last-Modified   : 2017/07/14
Version         : 1.0.0
Description     : utility/cloudletsのテストプログラム 
"""
from simulator.oldmodels import Cloudlet, Cloudlets, Point
from simulator.utility import cloudlet
import unittest


class CloudletUtilityTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_create_all_time_cloudlets(self):
        from typing import List
        from simulator.oldmodels import Cloudlet
        atcs = cloudlet.create_all_time_cloudlets(3, 4, 5, 10)
        self.assertTrue(isinstance(atcs, List))
        self.assertTrue(isinstance(atcs[0], List))
        self.assertTrue(isinstance(atcs[0][0], List))
        self.assertTrue(isinstance(atcs[0][0][0], Cloudlet))
        self.assertEqual(len(atcs), 3)
        self.assertEqual(len(atcs[0]), 5)
        self.assertEqual(len(atcs[0][0]), 4)

    def test_create_blank_allocation_plan(self):
        from simulator.oldmodels import Device
        atcs = cloudlet.create_all_time_cloudlets(3, 3, 3)
        ds = [Device(name="d1"), Device(name="d2"), Device(name="d3")]
        ap = cloudlet.create_blank_allocation_plan(atcs, ds)
        kys = ap.keys()
        if ds is not None or len(ds) == 0:
            for d in ds:
                self.assertTrue(d.name in kys)
        else:
            self.fail("AllocationPlanが生成されませんでした。")

    def test_is_valid_point(self):
        from simulator.oldmodels import Cloudlet
        cs = [
            [Cloudlet(), Cloudlet(), Cloudlet()],
            [Cloudlet(), Cloudlet(), Cloudlet()],
            [Cloudlet(), Cloudlet(), Cloudlet()],
        ]
        self.assertTrue(cloudlet.is_valid_point(cs, Point(0, 0)), msg="x=0, y=0")
        self.assertTrue(cloudlet.is_valid_point(cs, Point(2, 2)), msg="x=2, y=2")
        self.assertFalse(cloudlet.is_valid_point(cs, Point(-1, -1)), msg="x=-1, y=-1")
        self.assertFalse(cloudlet.is_valid_point(cs, Point(3, 3)), msg="x=3, y=3")

    def test_near_cloudlets_01(self):
        from simulator.oldmodels import Cloudlet
        cs = [
            [Cloudlet(name="d1"), Cloudlet(name="d2"), Cloudlet(name="d3"), Cloudlet(name="d4")],
            [Cloudlet(name="d5"), Cloudlet(name="d6"), Cloudlet(name="d7"), Cloudlet(name="d8")],
            [Cloudlet(name="d9"), Cloudlet(name="d10"), Cloudlet(name="d11"), Cloudlet(name="d12")],
            [Cloudlet(name="d13"), Cloudlet(name="d14"), Cloudlet(name="d15"), Cloudlet(name="d16")]
        ]
        ncs = cloudlet.near_cloudlets(cs, Point(0, 0), 2, 0)
        self.assertEqual(len(ncs), 6, msg=[c.name for c in ncs])
        names = [c.name for c in ncs]
        self.assertTrue("d1" in names, msg=[c.name for c in ncs])
        self.assertTrue("d2" in names, msg=[c.name for c in ncs])
        self.assertTrue("d3" in names, msg=[c.name for c in ncs])
        self.assertTrue("d6" in names, msg=[c.name for c in ncs])
        self.assertTrue("d5" in names, msg=[c.name for c in ncs])
        self.assertTrue("d9" in names, msg=[c.name for c in ncs])

    def test_near_cloudlets_02(self):
        from simulator.oldmodels import Cloudlet
        cs = [
            [Cloudlet(name="d1"), Cloudlet(name="d2"), Cloudlet(name="d3"), Cloudlet(name="d4")],
            [Cloudlet(name="d5"), Cloudlet(name="d6"), Cloudlet(name="d7"), Cloudlet(name="d8")],
            [Cloudlet(name="d9"), Cloudlet(name="d10"), Cloudlet(name="d11"), Cloudlet(name="d12")],
            [Cloudlet(name="d13"), Cloudlet(name="d14"), Cloudlet(name="d15"), Cloudlet(name="d16")]
        ]
        ncs = cloudlet.near_cloudlets(cs, Point(0, 0), 2, 2)
        self.assertEqual(len(ncs), 3, msg=[c.name for c in ncs])
        names = [c.name for c in ncs]
        self.assertTrue("d3" in names, msg=[c.name for c in ncs])
        self.assertTrue("d6" in names, msg=[c.name for c in ncs])
        self.assertTrue("d9" in names, msg=[c.name for c in ncs])

    def test_near_cloudlets_03(self):
        from simulator.oldmodels import Cloudlet
        cs = [
            [Cloudlet(name="d1"), Cloudlet(name="d2"), Cloudlet(name="d3"), Cloudlet(name="d4")],
            [Cloudlet(name="d5"), Cloudlet(name="d6"), Cloudlet(name="d7"), Cloudlet(name="d8")],
            [Cloudlet(name="d9"), Cloudlet(name="d10"), Cloudlet(name="d11"), Cloudlet(name="d12")],
            [Cloudlet(name="d13"), Cloudlet(name="d14"), Cloudlet(name="d15"), Cloudlet(name="d16")]
        ]
        ncs = cloudlet.near_cloudlets(cs, Point(1, 1), 3, 1)
        self.assertEqual(len(ncs), 14, msg=[c.name for c in ncs])
        names = [c.name for c in ncs]
        self.assertTrue("d1" in names, msg=[c.name for c in ncs])
        self.assertTrue("d2" in names, msg=[c.name for c in ncs])
        self.assertTrue("d3" in names, msg=[c.name for c in ncs])
        self.assertTrue("d4" in names, msg=[c.name for c in ncs])
        self.assertTrue("d5" in names, msg=[c.name for c in ncs])
        self.assertTrue("d7" in names, msg=[c.name for c in ncs])
        self.assertTrue("d8" in names, msg=[c.name for c in ncs])
        self.assertTrue("d9" in names, msg=[c.name for c in ncs])
        self.assertTrue("d10" in names, msg=[c.name for c in ncs])
        self.assertTrue("d11" in names, msg=[c.name for c in ncs])
        self.assertTrue("d12" in names, msg=[c.name for c in ncs])
        self.assertTrue("d13" in names, msg=[c.name for c in ncs])
        self.assertTrue("d14" in names, msg=[c.name for c in ncs])
        self.assertTrue("d15" in names, msg=[c.name for c in ncs])

    def test_near_cloudlets_04(self):
        from simulator.oldmodels import Cloudlet
        cs = [
            [Cloudlet(name="d1"), Cloudlet(name="d2"), Cloudlet(name="d3"), Cloudlet(name="d4")],
            [Cloudlet(name="d5"), Cloudlet(name="d6"), Cloudlet(name="d7"), Cloudlet(name="d8")],
            [Cloudlet(name="d9"), Cloudlet(name="d10"), Cloudlet(name="d11"), Cloudlet(name="d12")],
            [Cloudlet(name="d13"), Cloudlet(name="d14"), Cloudlet(name="d15"), Cloudlet(name="d16")]
        ]
        ncs = cloudlet.near_cloudlets(cs, Point(1, 1), 3, 3)
        self.assertEqual(len(ncs), 4, msg=[c.name for c in ncs])
        names = [c.name for c in ncs]
        self.assertTrue("d4" in names, msg=[c.name for c in ncs])
        self.assertTrue("d12" in names, msg=[c.name for c in ncs])
        self.assertTrue("d13" in names, msg=[c.name for c in ncs])
        self.assertTrue("d15" in names, msg=[c.name for c in ncs])
