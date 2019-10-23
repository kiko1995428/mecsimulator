"""
test/dataset.py
coding          : utf-8
Author          : Kouhei Osaki
Created         : 2017/07/04
Last-Modified   : 2017/07/07
Version         : 1.1.0
Description     : simulator/dataset.pyのテストプログラム
"""
import unittest
from simulator import olddataset


class DatasetTestCase(unittest.TestCase):
    def setUp(self):
        """
        初期化メソッド
        :return: 
        """
        pass

    # def test_create_random_plan_01(self):
    #     """
    #     create_random_planの実行によって生成されるMovementPlanのサイズが、
    #     指定した範囲におさまっていることを確認する
    #     :return:
    #     """
    #     st, mp = dataset.create_random_plan(1, 10)
    #     self.assertTrue(1 <= len(mp) <= 10, msg="mp length is "+str(len(mp)))
    #
    # def test_create_random_plan_02(self):
    #     """
    #     create_random_planの実行の返り値の型が正しいことを確認する
    #     :return:
    #     """
    #     from simulator.model import Point
    #     from typing import List
    #     st, mp = dataset.create_random_plan(1, 10)
    #     self.assertTrue(isinstance(mp, List))
    #     self.assertTrue(isinstance(mp[0], Point))
    #
    # def test_create_random_plan_03(self):
    #     """
    #     create_random_planが返す座標群が制約を満たしているか確認する。
    #     次の座標は必ず上下左右のいずれかであること、など。
    #     ※utility.is_udrlを使用しているため注意が必要
    #     :return:
    #     """
    #     from simulator.utility import is_udrl
    #     from simulator.model import Point
    #     mp = dataset.create_random_plan(1, 10)
    #     prev = None  # type:Point
    #     for p in mp:
    #         if prev is not None:
    #             self.assertTrue(is_udrl(p.x, p.y, prev.x, prev.y))
    #
    # def test_create_random_plan_04(self):
    #     """
    #     create_random_planの実行によって生成されるMovementPlanのサイズが、
    #     指定した範囲におさまっていることを確認する
    #     :return:
    #     """
    #     st, mp = dataset.create_random_plan(1, 1)
    #     self.assertTrue(1 <= len(mp) <= 1, msg="mp length is "+str(len(mp)))
    #
    # def test_create_random_plan_05(self):
    #     """
    #     create_random_planの実行によって生成されるMovementPlanのx座標、y座標の最大値が
    #     setting.pyの内容に従っているか
    #     :return:
    #     """
    #     from simulator.setting import x_length, y_length
    #     st, mp = dataset.create_random_plan(1, 100)
    #     for i in range(10000):
    #         for p in mp:
    #             self.assertTrue(0 <= p.x < x_length, msg="x={} but x_len is {}".format(p.x, x_length))
    #             self.assertTrue(0 <= p.y < y_length, msg="y={} but y_len is {}".format(p.y, y_length))

    def test_create_devices(self):
        devices = olddataset.create_devices(max_time=10, x_length=100, y_length=100, low_limit=10, high_limit=10,
                                            min_coincident=10, max_coincident=10, min_use_resource=5, max_use_resource=5,
                                            num=100)
        self.assertEqual(devices[0].name, "d1")
        self.assertEqual(devices[1].name, "d2")
        self.assertEqual(len(devices), 100)

