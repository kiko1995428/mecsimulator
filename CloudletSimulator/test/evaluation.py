"""
test/evaluation.py
coding          : utf-8
Author          : Kouhei Osaki
Created         : 2017/06/22
Last-Modified   : 2017/06/22
Version         : 1.0.0
Description     : evaluation.pyのテストモジュール
"""
import unittest
from simulator.oldmodels import AllocationPlan, Allocation
from simulator.evaluation import avg_hops, max_hops


class EvaluationTestCase(unittest.TestCase):
    def setUp(self):
        self.allocation_plan = {
            "d1": [Allocation(1, 1, 3), Allocation(1, 1, 3), Allocation(1, 1, 3)],
            "d2": [Allocation(1, 1, 1), Allocation(1, 1, 3), Allocation(1, 1, 5)],
            "d3": [Allocation(1, 1, 1), Allocation(1, 1, 1), Allocation(1, 1, 1)]
        }

    def test_avg_hops(self):
        result = avg_hops(self.allocation_plan)
        self.assertEqual(result["d1"], 3)
        self.assertEqual(result["d2"], 3)
        self.assertEqual(result["d3"], 1)

    def test_max_hops(self):
        result = max_hops(self.allocation_plan)
        self.assertEqual(result["d1"], 3)
        self.assertEqual(result["d2"], 5)
        self.assertEqual(result["d3"], 1)
