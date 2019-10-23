"""
test/oldutility.py
coding          : utf-8
Author          : Kouhei Osaki
Created         : 2017/07/04
Last-Modified   : 2017/07/11
Version         : 1.1.0
Description     : リソースの割当処理を行うメソッドを定義している。 
"""
import unittest
from simulator import oldutility


class UtilityTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_is_udrl_01(self):
        self.assertTrue(oldutility.is_udrl(0, 0, 0, 1))

    def test_is_udrl_02(self):
        self.assertTrue(oldutility.is_udrl(0, 0, 1, 0))

    def test_is_udrl_03(self):
        self.assertTrue(oldutility.is_udrl(0, 1, 0, 0))

    def test_is_udrl_04(self):
        self.assertTrue(oldutility.is_udrl(0, 1, 0, 2))

    def test_is_udrl_05(self):
        self.assertFalse(oldutility.is_udrl(0, 0, 1, 1))

    def test_is_udrl_06(self):
        self.assertFalse(oldutility.is_udrl(0, 0, 0, 0))

    def test_range2d_01(self):
        tlist = [0, 1, 2]
        n1, n2 = oldutility.range2d(0, 3)
        self.assertEquals(tlist[0], n1[0])
        self.assertEquals(tlist[1], n1[1])
        self.assertEquals(tlist[2], n1[2])

    # def test_create_input_data_01(self):
    #     from simulator.model import Device
    #     devices = oldutility.create_input_data()
    #     for d in devices:
    #         self.assertTrue(isinstance(d, Device))

    # def test_load_input_data_01(self):
    #     from simulator.model import Device
    #     cds = oldutility.create_input_data(file_save=True, output_file="test.json")
    #     lds = oldutility.load_input_data(input_file="test.json")
    #     for cd, ld in zip(cds, lds):
    #         self.assertTrue(isinstance(ld, Device))
    #         self.assertEqual(cd.name, ld.name)

    def test_create_all_time_cloudlets(self):
        from typing import List
        from simulator.oldmodels import Cloudlet
        atcs = oldutility.create_all_time_cloudlets(3, 4, 5, 10)
        self.assertTrue(isinstance(atcs, List))
        self.assertTrue(isinstance(atcs[0], List))
        self.assertTrue(isinstance(atcs[0][0], List))
        self.assertTrue(isinstance(atcs[0][0][0], Cloudlet))
        self.assertEqual(len(atcs), 3)
        self.assertEqual(len(atcs[0]), 5)
        self.assertEqual(len(atcs[0][0]), 4)

    def test_create_blank_allocation_plan(self):
        from simulator.oldmodels import Device
        atcs = oldutility.create_all_time_cloudlets(3, 3, 3)
        ds = [Device(name="d1"), Device(name="d2"), Device(name="d3")]
        ap = oldutility.create_blank_allocation_plan(atcs, ds)
        kys = ap.keys()
        if ds is not None or len(ds) == 0:
            for d in ds:
                self.assertTrue(d.name in kys)
        else:
            self.fail("AllocationPlanが生成されませんでした。")

    def test_is_valid_cell(self):
        from simulator.oldmodels import Cloudlet
        cs = [
            [Cloudlet(), Cloudlet(), Cloudlet()],
            [Cloudlet(), Cloudlet(), Cloudlet()],
            [Cloudlet(), Cloudlet(), Cloudlet()],
        ]
        self.assertTrue(oldutility.is_valid_cell(cs, 0, 0), msg="x=0, y=0")
        self.assertTrue(oldutility.is_valid_cell(cs, 2, 2), msg="x=2, y=2")
        self.assertFalse(oldutility.is_valid_cell(cs, -1, -1), msg="x=-1, y=-1")
        self.assertFalse(oldutility.is_valid_cell(cs, 3, 3), msg="x=3, y=3")

    def test_get_udrl_cloudlet_01(self):
        from simulator.oldmodels import Cloudlet
        cs = [
            [Cloudlet(name="d1"), Cloudlet(name="d2"), Cloudlet(name="d3")],
            [Cloudlet(name="d4"), Cloudlet(name="d5"), Cloudlet(name="d6")],
            [Cloudlet(name="d7"), Cloudlet(name="d8"), Cloudlet(name="d9")],
        ]
        ncs = oldutility.get_udrl_cloudlet(cs, 1, 1)
        self.assertEqual(len(ncs), 4, msg=[c.name for c in ncs])
        names = [c.name for c in ncs]
        self.assertTrue("d2" in names)
        self.assertTrue("d4" in names)
        self.assertTrue("d8" in names)
        self.assertTrue("d6" in names)

    def test_get_udrl_cloudlet_02(self):
        from simulator.oldmodels import Cloudlet
        cs = [
            [Cloudlet(name="d1"), Cloudlet(name="d2"), Cloudlet(name="d3")],
            [Cloudlet(name="d4"), Cloudlet(name="d5"), Cloudlet(name="d6")],
            [Cloudlet(name="d7"), Cloudlet(name="d8"), Cloudlet(name="d9")],
        ]
        ncs = oldutility.get_udrl_cloudlet(cs, 0, 0)
        self.assertEqual(len(ncs), 2, msg=[c.name for c in ncs])
        names = [c.name for c in ncs]
        self.assertTrue("d2" in names)
        self.assertTrue("d4" in names)

    def test_get_udrl_cloudlet_03(self):
        from simulator.oldmodels import Cloudlet
        cs = [
            [Cloudlet(name="d1"), Cloudlet(name="d2"), Cloudlet(name="d3")],
            [Cloudlet(name="d4"), Cloudlet(name="d5"), Cloudlet(name="d6")],
            [Cloudlet(name="d7"), Cloudlet(name="d8"), Cloudlet(name="d9")],
        ]
        ncs = oldutility.get_udrl_cloudlet(cs, 2, 2)
        self.assertEqual(len(ncs), 2, msg=[c.name for c in ncs])
        names = [c.name for c in ncs]
        self.assertTrue("d8" in names)
        self.assertTrue("d6" in names)

    def test_get_near_cloudlet_01(self):
        from simulator.oldmodels import Cloudlet
        cs = [
            [Cloudlet(name="d1"), Cloudlet(name="d2"), Cloudlet(name="d3"), Cloudlet(name="d4")],
            [Cloudlet(name="d5"), Cloudlet(name="d6"), Cloudlet(name="d7"), Cloudlet(name="d8")],
            [Cloudlet(name="d9"), Cloudlet(name="d10"), Cloudlet(name="d11"), Cloudlet(name="d12")],
            [Cloudlet(name="d13"), Cloudlet(name="d14"), Cloudlet(name="d15"), Cloudlet(name="d16")]
        ]
        ncs = oldutility.get_near_cloudlet(cs, 0, 0, 2)
        self.assertEqual(len(ncs), 5, msg=[c.name for c in ncs])
        names = [c.name for c in ncs]
        self.assertTrue("d2" in names, msg=[c.name for c in ncs])
        self.assertTrue("d3" in names, msg=[c.name for c in ncs])
        self.assertTrue("d6" in names, msg=[c.name for c in ncs])
        self.assertTrue("d5" in names, msg=[c.name for c in ncs])
        self.assertTrue("d9" in names, msg=[c.name for c in ncs])

    def test_get_near_cloudlet_02(self):
        from simulator.oldmodels import Cloudlet
        cs = [
            [Cloudlet(name="d1"), Cloudlet(name="d2"), Cloudlet(name="d3"), Cloudlet(name="d4")],
            [Cloudlet(name="d5"), Cloudlet(name="d6"), Cloudlet(name="d7"), Cloudlet(name="d8")],
            [Cloudlet(name="d9"), Cloudlet(name="d10"), Cloudlet(name="d11"), Cloudlet(name="d12")],
            [Cloudlet(name="d13"), Cloudlet(name="d14"), Cloudlet(name="d15"), Cloudlet(name="d16")]
        ]
        ncs = oldutility.get_near_cloudlet(cs, 0, 0, 2, invalid_distance=1)
        self.assertEqual(len(ncs), 3, msg=[c.name for c in ncs])
        names = [c.name for c in ncs]
        self.assertTrue("d3" in names, msg=[c.name for c in ncs])
        self.assertTrue("d6" in names, msg=[c.name for c in ncs])
        self.assertTrue("d9" in names, msg=[c.name for c in ncs])

    def test_get_near_cloudlet_03(self):
        from simulator.oldmodels import Cloudlet
        cs = [
            [Cloudlet(name="d1"), Cloudlet(name="d2"), Cloudlet(name="d3"), Cloudlet(name="d4")],
            [Cloudlet(name="d5"), Cloudlet(name="d6"), Cloudlet(name="d7"), Cloudlet(name="d8")],
            [Cloudlet(name="d9"), Cloudlet(name="d10"), Cloudlet(name="d11"), Cloudlet(name="d12")],
            [Cloudlet(name="d13"), Cloudlet(name="d14"), Cloudlet(name="d15"), Cloudlet(name="d16")]
        ]
        ncs = oldutility.get_near_cloudlet(cs, 1, 1, 3)
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

    def test_get_near_cloudlet_04(self):
        from simulator.oldmodels import Cloudlet
        cs = [
            [Cloudlet(name="d1"), Cloudlet(name="d2"), Cloudlet(name="d3"), Cloudlet(name="d4")],
            [Cloudlet(name="d5"), Cloudlet(name="d6"), Cloudlet(name="d7"), Cloudlet(name="d8")],
            [Cloudlet(name="d9"), Cloudlet(name="d10"), Cloudlet(name="d11"), Cloudlet(name="d12")],
            [Cloudlet(name="d13"), Cloudlet(name="d14"), Cloudlet(name="d15"), Cloudlet(name="d16")]
        ]
        ncs = oldutility.get_near_cloudlet(cs, 1, 1, 3, invalid_distance=2)
        self.assertEqual(len(ncs), 4, msg=[c.name for c in ncs])
        names = [c.name for c in ncs]
        self.assertTrue("d4" in names, msg=[c.name for c in ncs])
        self.assertTrue("d12" in names, msg=[c.name for c in ncs])
        self.assertTrue("d13" in names, msg=[c.name for c in ncs])
        self.assertTrue("d15" in names, msg=[c.name for c in ncs])

    def test_continuity_01(self):
        from simulator.oldmodels import Point
        target = [Point(0, 0), Point(0, 1), Point(1, 1)]
        self.assertTrue(oldutility.continuity(target))

    def test_continuity_02(self):
        from simulator.oldmodels import Point
        target = [Point(0, 0), Point(1, 1), Point(1, 2)]
        self.assertFalse(oldutility.continuity(target))

    def test_scope_01(self):
        from simulator.oldmodels import Point
        p1 = Point(2, 2)
        scp = oldutility.scope(p1, distance_min=0, distance_max=0, x_max=100, x_min=-100, y_max=100, y_min=-100)
        self.assertEqual(1, len(scp), msg=scp)
        self.assertTrue(Point(2, 2) in scp)

    def test_scope_02(self):
        from simulator.oldmodels import Point
        p1 = Point(2, 2)
        scp = oldutility.scope(p1, distance_min=0, distance_max=1, x_max=100, x_min=-100, y_max=100, y_min=-100)
        self.assertEqual(5, len(scp), msg=scp)
        self.assertTrue(Point(2, 2) in scp)
        self.assertTrue(Point(2, 1) in scp)
        self.assertTrue(Point(2, 3) in scp)
        self.assertTrue(Point(1, 2) in scp)
        self.assertTrue(Point(3, 2) in scp)

    def test_scope_03(self):
        from simulator.oldmodels import Point
        p1 = Point(2, 2)
        scp = oldutility.scope(p1, distance_min=0, distance_max=2, x_max=100, x_min=-100, y_max=100, y_min=-100)
        self.assertEqual(13, len(scp), msg=scp)
        self.assertTrue(Point(2, 2) in scp)
        self.assertTrue(Point(2, 1) in scp)
        self.assertTrue(Point(2, 3) in scp)
        self.assertTrue(Point(1, 2) in scp)
        self.assertTrue(Point(3, 2) in scp)
        self.assertTrue(Point(2, 4) in scp)
        self.assertTrue(Point(2, 0) in scp)
        self.assertTrue(Point(4, 2) in scp)
        self.assertTrue(Point(0, 2) in scp)
        self.assertTrue(Point(3, 3) in scp)
        self.assertTrue(Point(1, 1) in scp)
        self.assertTrue(Point(1, 3) in scp)
        self.assertTrue(Point(3, 1) in scp)

    def test_scope_04(self):
        from simulator.oldmodels import Point
        p1 = Point(0, 0)
        scp = oldutility.scope(p1, distance_min=2, distance_max=2, x_max=100, x_min=-100, y_max=100, y_min=-100)
        self.assertEqual(8, len(scp), msg=scp)
        self.assertTrue(Point(2, 0) in scp)
        self.assertTrue(Point(1, 1) in scp)
        self.assertTrue(Point(0, 2) in scp)
        self.assertTrue(Point(-1, 1) in scp)
        self.assertTrue(Point(-2, 0) in scp)
        self.assertTrue(Point(-1, -1) in scp)
        self.assertTrue(Point(0, 2) in scp)
        self.assertTrue(Point(1, -1) in scp)
