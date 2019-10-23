import unittest
from simulator.model.cloudlet import Cloudlet
from simulator.model.device import Device
from simulator.model.application import Application
from simulator.model.point import Point3D


class TestModelCloudletCloudlet(unittest.TestCase):
    def setUp(self):
        self.cloudlet = Cloudlet(5, Point3D(0, 0, 0), name="d1")
        self.d01 = Device(name="d1")
        self.app01 = Application(name="a1")
        self.app02 = Application(name="a2")
        self.dapp01 = Application(name="a1", use_resource=1)
        self.d01.apps = [self.dapp01]
        self.cloudlet.apps_append(self.app02)
        self.cloudlet.apps_append(self.app01)
    def test_is_app_num_return(self):
        list = ["a1", "a2", "a3"]
        self.assertTrue(self.cloudlet.app_num_return())
    def test_is_operatable_app_01(self):
        self.assertTrue(self.cloudlet.is_operatable_application("a1"))

    def test_is_operatable_app_02(self):
        self.assertFalse(self.cloudlet.is_operatable_application("a0"))

    def test_can_append_device_01(self):
        self.assertTrue(self.cloudlet.can_append_device(self.d01))

    def test_can_append_device_02(self):
        d2 = Device(name="d2")
        d2.append_app(Application(name="a2", use_resource=6))
        self.assertFalse(self.cloudlet.can_append_device(d2))

    def test_can_append_device_03(self):
        d2 = Device(name="d2")
        d2.append_app(Application(name="a2", use_resource=1))
        self.assertTrue(self.cloudlet.can_append_device(d2))

    def test_can_append_device_04(self):
        d2 = Device(name="d2")
        d2.append_app(Application(name="a2", use_resource=1))
        self.assertFalse(self.cloudlet.can_append_device(d2, app_check=True))
