"""
test/utility/points.py
coding          : utf-8
Author          : Kouhei Osaki
Created         : 2017/07/17
Last-Modified   : 2017/07/17
Version         : 1.0.0
Description     : utilyty/dataのテストプログラム 
"""
import unittest
from simulator.oldmodels import Device, Allocation
from simulator.utility import data
from simulator.utility.cloudlet import create_all_time_cloudlets


class DataUtilityTestCase(unittest.TestCase):
    def setUp(self):
        self.inputdata_file_name = "test/utility/test_data/test_devices_for_json_file.inputdata"
        self.csv_file_name = "test/utility/test_data/test_allocation_plan_to_csv.csv"
        self.all_time_cloudlets = create_all_time_cloudlets(10, 10, 10)
        self.devices = [Device(name="d1"), Device(name="d2"), Device(name="d3")]
        self.allocation_plan = {
            "d1": [Allocation(0, 0, 0), Allocation(0, 0, 1), Allocation(0, 0, 3)],
            "d2": [Allocation(0, 0, 1), Allocation(0, 0, 1), Allocation(0, 0, 3)],
            "d3": [Allocation(0, 0, 3), Allocation(0, 0, 2), Allocation(0, 0, 2)],
            "d4": [Allocation(0, 0, 0), Allocation(0, 0, 4), Allocation(0, 0, 4)]
        }
        data.input_data_to_file(self.all_time_cloudlets, self.devices, self.inputdata_file_name)

    def test_allocation_plan_to_csv_01(self):
        data.allocation_plan_to_csv(self.allocation_plan, self.csv_file_name)

    def test_input_devices_01(self):
        atcs, ds = data.input_data_from_file(self.inputdata_file_name)
        self.assertEqual(10, len(atcs))
        self.assertEqual(10, len(atcs[0]))
        self.assertEqual(10, len(atcs[0][0]))
        self.assertEqual(self.devices[0].name, ds[0].name)
        self.assertEqual(self.devices[1].name, ds[1].name)
        self.assertEqual(self.devices[2].name, ds[2].name)
