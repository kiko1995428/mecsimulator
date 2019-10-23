# coding:utf-8
"""
oldutility.py
Author          : Kouhei Osaki
Created         : 2017/06/14
Last-Modified   : 2017/07/07
Version         : 1.4.0
Description     : 有用な関数などを定義している（適当
"""


import math
from typing import Dict, List
from simulator.oldmodels import AllTimeCloudlets, Devices, AllocationPlan, Cloudlet, Cloudlets, Point


def is_udrl(x, y, base_x, base_y):
    """
    x, y座標がbase_x, base_yの上下左右いずれかの座標であるかをチェックする
    :param x: 調査対象のx座標
    :param y: 調査対象のx座標
    :param base_x: 基準となるx座標
    :param base_y: 基準となるy座標
    :return: 上下左右のいずれかであればTrue, そうでなければFalse
    """
    if base_x == x and math.fabs(base_y - y) == 1:
        return True
    if math.fabs(base_x - x) == 1 and base_y == y:
        return True
    return False


def range2d(start, stop):
    """
    rangeから2変数をまとめて取得
    :param start: 
    :param stop: 
    :return: 
    """
    n1 = range(start, stop)
    n2 = range(start, stop)
    return n1, n2


def create_input_data(file_save: bool=False, output_file: str="input_data.json") -> Devices:
    """
    入力データを生成し、file_saveがTrueならファイルにjson形式で書き込む
    :param file_save: 
    :param output_file: 出力先ファイル
    :return: 入力データ
    """
    import json
    from simulator.olddataset import create_devices
    devices = create_devices()
    if file_save is True:
        input_data = {"devices": devices}
        f = open(output_file, "w")
        json.dump(input_data, f)
        f.close()
    return devices


def load_input_data(input_file: str="input_data.json") -> Devices:
    """
    指定されたファイルから入力データを読み込む
    :param input_file: 入力データが保存されたファイル
    :return: 入力データ
    """
    import json
    f = open(input_file, "r")
    input_data = json.load(f)
    return input_data["devices"]


def create_all_time_cloudlets(t_len: int, x_len: int, y_len: int, max_resource: int=5) -> AllTimeCloudlets:
    """
    時間軸、横軸、縦軸の最大長を指定してCloudletの三次元リストを生成する。
    :param t_len: 時間軸の最大長
    :param x_len: 横軸の最大長
    :param y_len: 縦軸の最大長
    :param max_resource: 
    :return: 
    """
    all_time_cloudlets = [[[Cloudlet(r=max_resource) for i in range(x_len)]
                           for j in range(y_len)]
                          for k in range(t_len)]     # type: AllTimeCloudlets
    return all_time_cloudlets


def create_blank_allocation_plan(all_time_cloudlets: AllTimeCloudlets, devices: Devices) -> AllocationPlan:
    """
    空の割当計画表を生成するメソッド
    :param all_time_cloudlets: Cloudletの3次元リスト
    :param devices: Deviceのリスト
    :return: 
    """
    allocation_plan = {}    # type: AllocationPlan
    for device in devices:
        allocation_plan[device.name] = [None for i in range(len(all_time_cloudlets))]
    return allocation_plan


def is_valid_cell(cloudlets: Cloudlets, x: int, y: int) -> bool:
    if not (0 <= y < len(cloudlets)):
        return False
    if not (0 <= x < len(cloudlets[y])):
        return False
    return True


def is_valid_all_time_cell(all_time_cloudlets: AllTimeCloudlets, t: int, x: int, y: int) -> bool:
    """
    指定されたCellがCloudlets中で有効か判定する
    :param all_time_cloudlets: Cloudletの三次元リスト([time][y][x])
    :param t: 時間
    :param x: x軸
    :param y: y軸
    :return: 有効ならTrue，無効ならFalse
    """
    if not (0 <= t < len(all_time_cloudlets)):
        return False
    return is_valid_cell(all_time_cloudlets[t], x, y)


def get_udrl_cloudlet(cloudlets: Cloudlets, x: int, y: int) -> List[Cloudlet]:
    pts = [Point(xx, yy) for xx in [x-1, x, x+1] for yy in [y-1, y, y+1] if is_udrl(xx, yy, x, y)]
    return [cloudlets[p.y][p.x] for p in pts if is_valid_cell(cloudlets, p.x, p.y)]


def get_near_cloudlet(cloudlets: Cloudlets, x: int, y: int,
                      distance: int, invalid_distance: int=0) -> List[Cloudlet]:
    # 既出
    spc = []
    # 近接
    near = []
    spc.append(cloudlets[y][x])
    targets = [cloudlets[y][x]]
    if invalid_distance < 0:
        near.append(cloudlets[y][x])
    for now in range(1, distance + 1):
        new = []
        for t in targets:
            p = get_cloudlet_point_from_cloudlets(t.name, cloudlets)
            udrl = get_udrl_cloudlet(cloudlets, p.x, p.y)
            for c in udrl:
                if c in spc:
                    pass
                else:
                    new.append(c)
                    spc.append(c)
                    if now > invalid_distance:
                        near.append(c)
        targets = new
    return near


def get_cloudlet_point_from_cloudlets(name: str, cloudlets: Cloudlets) -> Point:
    for y, row in enumerate(cloudlets):
        for x, c in enumerate(row):
            if c.name == name:
                return Point(x, y)
    else:
        return None


def continuity(target: List[Point]) -> bool:
    """
    targetが持つ経路が上下左右いずれかで連続しているかを調べる
    :param target: 検査経路
    :return: 連続している場合True，していない場合False
    """
    prev = None  # type:Point
    for point in target:
        if prev is None:
            # 最初の一個目の場合
            prev = point
            continue
        if is_udrl(point.x, point.y, prev.x, prev.y):
            prev = point
        else:
            return False
    return True


def dist(p1: Point, p2: Point) -> int:
    """
    2点間の距離を返す
    :param p1: 
    :param p2: 
    :return: 距離
    """
    return int(math.fabs(p2.x - p1.x)) + int(math.fabs(p2.y - p1.y))


def scope(center: Point, distance_max: int,
          x_max: int, y_max: int, distance_min: int=0, x_min: int=0, y_min: int=0) -> List[Point]:
    ret = []  # type:List[Point]
    for y in range(y_min, y_max + 1):
        for x in range(x_min, x_max + 1):
            point = Point(x, y)
            if distance_min <= dist(center, point) <= distance_max:
                ret.append(point)
    return ret


