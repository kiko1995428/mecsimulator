import unittest


class DatasetTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_cross(self):
        # 表示用
        from simulator.oldmodels import Point
        from simulator.dataset import devices
        ds = devices.cross(Point(0, 0), Point(30, 30), 30, r_num=4, density=2)
        print([d.plan[0] for d in ds])
        print([d.use_resource for d in ds])
        print([d.startup_time for d in ds])
