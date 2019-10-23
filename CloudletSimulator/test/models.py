"""
test/models.py
coding          : utf-8
Author          : Kouhei Osaki
Created         : 2017/06/22
Last-Modified   : 2017/06/28
Version         : 1.2.0
Description     : models.pyのテストモジュール
"""
import unittest
from simulator import oldmodels


class ApplicationTestCase(unittest.TestCase):
    def setUp(self):
        self.init_name = "test"
        self.init_use_resource = 5
        self.app = oldmodels.Application(name=self.init_name, use_resource=self.init_use_resource)

    def test_name_property(self):
        self.assertEqual(self.app.name, self.init_name)

    def test_name_setter(self):
        set_name = "after"
        self.app.name = set_name
        self.assertEqual(self.app.name, set_name)

    def test_use_resource_property(self):
        self.assertEqual(self.app.use_resource, self.init_use_resource)

    def test_use_resource_setter(self):
        set_use_resource = 10
        self.app.use_resource = set_use_resource
        self.assertEqual(self.app.use_resource, set_use_resource)

    def test_num(self):
        self.assertEqual(oldmodels.Application().name, "a1")
        self.assertEqual(oldmodels.Application().name, "a2")
        self.assertEqual(oldmodels.Application().name, "a3")


class DeviceTestCase(unittest.TestCase):
    def setUp(self):
        self.init_name = "d1"
        self.init_a1_name = "a1"
        self.init_a1_use_resource = 5
        self.init_a1 = oldmodels.Application(name=self.init_a1_name, use_resource=self.init_a1_use_resource)
        self.init_apps = [self.init_a1]
        self.device = oldmodels.Device(name=self.init_name, apps=self.init_apps)

    def test_name_property(self):
        self.assertEqual(self.device.name, self.init_name)

    def test_name_setter(self):
        set_name = "d2"
        self.device.name = set_name
        self.assertEqual(self.device.name, set_name)

    def test_use_resource_property(self):
        self.assertEqual(self.device.use_resource, self.init_a1_use_resource)

    def test_apps_property(self):
        self.assertEqual(self.device.apps, self.init_apps)

    def test_append_app(self):
        new_app = oldmodels.Application(name="a2")
        after_apps = self.device.apps
        after_apps.append(new_app)
        self.device.append_app(new_app)
        self.assertEqual(self.device.apps, after_apps)

    def test_remove_app(self):
        remove_app = self.init_a1
        self.device.remove_app(remove_app)
        self.assertEqual(self.device.apps, [])

    def test_num(self):
        self.assertEqual(oldmodels.Device().name, "d1")
        self.assertEqual(oldmodels.Device().name, "d2")
        self.assertEqual(oldmodels.Device().name, "d3")


class CloudletTestCase(unittest.TestCase):
    def setUp(self):
        oldmodels.Cloudlet.num = 0
        self.init_d1_name = "d1"
        self.init_a1_name = "a1"
        self.init_a1_use_resource = 5
        self.init_a1 = oldmodels.Application(name=self.init_a1_name, use_resource=self.init_a1_use_resource)
        self.init_apps = [self.init_a1]
        self.init_d1 = oldmodels.Device(name=self.init_d1_name, apps=self.init_apps)
        self.init_devices = [self.init_d1]
        self.init_max_resource = 10
        self.cloudlet = oldmodels.Cloudlet(r=self.init_max_resource, devices=self.init_devices)

    def test_max_resource_property(self):
        self.assertEqual(self.cloudlet.resource, self.init_max_resource)

    def test_max_resource_setter(self):
        set_max_resource = 8
        self.cloudlet.resource = set_max_resource
        self.assertEqual(self.cloudlet.resource, set_max_resource)

    def test_devices_property(self):
        self.assertEqual(self.cloudlet.devices, self.init_devices)

    def test_empty_resource_property(self):
        self.assertEqual(self.cloudlet.empty_resource, self.init_max_resource - self.init_a1_use_resource)

    def test_can_append_device_01(self):
        append_app = oldmodels.Application(name="a2", use_resource=self.init_max_resource - self.init_a1_use_resource)
        a2_apps = [append_app]
        append_device = oldmodels.Device(name="d2", apps=a2_apps)
        self.assertTrue(self.cloudlet.can_append_device(append_device))

    def test_can_append_device_02(self):
        append_app = oldmodels.Application(name="a2", use_resource=self.init_max_resource - self.init_a1_use_resource + 1)
        a2_apps = [append_app]
        append_device = oldmodels.Device(name="d2", apps=a2_apps)
        self.assertFalse(self.cloudlet.can_append_device(append_device))

    def test_append_device_01(self):
        append_app = oldmodels.Application(name="a2", use_resource=self.init_max_resource - self.init_a1_use_resource)
        a2_apps = [append_app]
        append_device = oldmodels.Device(name="d2", apps=a2_apps)
        self.cloudlet.append_device(append_device)
        self.init_devices.append(append_device)
        self.assertEqual(self.cloudlet.devices, self.init_devices)

    def test_append_device_02(self):
        append_app = oldmodels.Application(name="a2", use_resource=self.init_max_resource - self.init_a1_use_resource)
        a2_apps = [append_app]
        append_device = oldmodels.Device(name="d2", apps=a2_apps)
        self.cloudlet.append_device(self.init_d1)
        self.assertRaises(Exception, lambda: self.cloudlet.append_device(append_device))

    def test_name_property(self):
        self.assertEqual(self.cloudlet.name, "c1")

    def test_num(self):
        oldmodels.Cloudlet.num = 0
        self.assertEqual(oldmodels.Cloudlet(r=1).name, "c1")
        self.assertEqual(oldmodels.Cloudlet(r=1).name, "c2")
        self.assertEqual(oldmodels.Cloudlet(r=1).name, "c3")
