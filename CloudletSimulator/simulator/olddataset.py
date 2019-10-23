# coding:utf-8
"""
olddataset.py
Author          : Koki Fukunaga, Kouhei Osaki
Created         : 2017/06/11
Last-Modified   : 2017/07/17
Version         : 3.1.0
Description     : Device の移動計画の作成

"""

from simulator.oldmodels import *
from simulator import setting
from simulator.utility.point import random_two_point, route
import random
"""
初期値の設定
（ｘ、ｙ）の範囲指定、開始時間を設定
スタート地点をランダムに作成
ゴール地点をランダムに作成
スタート地点とゴール地点の最短距離を求め
移動経路をリストにして出力
"""


def create_devices(max_time: int, x_length: int, y_length: int, low_limit: int, high_limit: int,
                   min_coincident: int, max_coincident: int, min_use_resource: int, max_use_resource: int,
                   num: int=None) -> Devices:
    """
    端末群を生成する
    :param max_time: 最大時間
    :param x_length: x座標の最大値
    :param y_length: y座標の最大値
    :param low_limit: 移動時間の下限
    :param high_limit: 移動時間の上限
    :param min_coincident: 最少同時発生数
    :param max_coincident: 最大同時発生数
    :param min_use_resource: 最小消費リソース
    :param max_use_resource: 最大消費リソース
    :param num: 端末数
    :return: 端末群
    """
    if num is None:
        num = max_coincident * max_time
    devices = []    # type:Devices
    count = 0   # type:int
    for t in range(max_time):
        create_num = random.randint(min_coincident, max_coincident)
        for i in range(create_num):
            device = Device()
            device.startup_time = t
            move = random.randint(low_limit, high_limit)
            start, goal = random_two_point(move, Point(0, 0), Point(x_length-1, y_length-1))
            device.plan = route(start, goal)
            device.use_resource = random.randint(min_use_resource, max_use_resource)
            devices.append(device)
            count += 1
            if count == num:
                return devices
    return devices


def create_random_plan(x_length: int, y_length: int, low_limit: int, high_limit: int) -> (int, MovementPlan):
    """
    移動経路の作成
    :param x_length: x座標の最大値
    :param y_length: y座標の最大値
    :param low_limit: 移動時間の下限
    :param high_limit: 移動時間の上限
    :return: 
    """
    plan = []   # type: MovementPlan
    start_time = random.randint(0, setting.t_length)
    current_time = start_time   # type: int
    " ランダムで始点、終点を定める。その際、距離が下限より下回っていた場合やり直し"
    flag = -1
    x_current = 0
    y_current = 0
    x_end = 0
    y_end = 0
    distance = 0
    while flag < 0:
        x_current = random.randint(0, x_length - 1)
        y_current = random.randint(0, y_length - 1)
        x_end = random.randint(0, x_length - 1)
        y_end = random.randint(0, y_length - 1)
        x_dis = x_end - x_current
        y_dis = y_end - y_current
        if x_dis < 0:
            if y_dis < 0:
                distance = (x_dis + y_dis) * -1  # type: int
            else:
                distance = - x_dis + y_dis
        else:
            if y_dis < 0:
                distance = x_dis - y_dis
            else:
                distance = x_dis + y_dis
        if distance == low_limit:
            continue
        else:
            flag += 1
    # origin position
    plan.append(Point(x_current, y_current))
    for i in range(0, distance):
        x_flag = x_end - x_current
        y_flag = y_end - y_current
        if current_time < high_limit:
            current_time += 1
            direction = random.randint(0, 1)    # direction = 0 -> x , direction = 1 -> y
            if x_flag > 0:
                if y_flag > 0:  # x > 0, y > 0 の時
                    if direction == 0:
                        x_current += 1
                        plan.append(Point(x_current, y_current))
                    else:
                        y_current += 1
                        plan.append(Point(x_current, y_current))
                elif y_flag < 0:    # x > 0, y < 0 の時
                    if direction == 0:
                        x_current += 1
                        plan.append(Point(x_current, y_current))
                    else:
                        y_current -= 1
                        plan.append(Point(x_current, y_current))
                else:  # x > 0, y = 0
                    x_current += 1
                    plan.append(Point(x_current, y_current))
            elif x_flag < 0:
                if y_flag > 0:
                    # x < 0, y > 0 の時
                    if direction == 0:
                        x_current -= 1
                        plan.append(Point(x_current, y_current))
                    else:
                        y_current += 1
                        plan.append(Point(x_current, y_current))
                elif y_flag < 0:    # x < 0 , y < 0 の時
                    if direction == 0:
                        x_current -= 1
                        plan.append(Point(x_current, y_current))
                    else:
                        y_current -= 1
                        plan.append(Point(x_current, y_current))
                else:
                    # x < 0, y = 0
                    x_current -= 1
                    plan.append(Point(x_current, y_current))
            else:
                # x = 0 の時
                if y_flag > 0:
                    # x = 0, y > 0 の時
                    y_current += 1
                    plan.append(Point(x_current, y_current))
                elif y_flag < 0:
                    # x = 0, y < 0
                    y_current -= 1
                    plan.append(Point(x_current, y_current))
                else:  # x = 0 , y = 0
                    break
        else:
            break
    return start_time, plan
