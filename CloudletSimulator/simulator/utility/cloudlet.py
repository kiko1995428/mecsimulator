"""
simulator/utility/cloudlet.py
Author          : Kouhei Osaki
Created         : 2017/07/12
Last-Modified   : 2017/07/12
Version         : 1.0.0
Description     : cloudletsに関する有用な関数などを定義している（適当
"""
from simulator.oldmodels import AllTimeCloudlets, Cloudlet, Cloudlets, AllocationPlan, Point, Devices
from simulator.utility.point import adjacency, distance
from typing import List


def create_all_time_cloudlets(t_len: int, x_len: int, y_len: int, r: int=5) -> AllTimeCloudlets:
    """
    時間軸、横軸、縦軸の最大長を指定してCloudletの三次元リストを生成する。
    :param t_len: 時間軸の最大長
    :param x_len: 横軸の最大長
    :param y_len: 縦軸の最大長
    :param r: 各クラウドレットの所有リソース
    :return: 
    """
    all_time_cloudlets = [[[Cloudlet(r=r) for i in range(x_len)]
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


def is_valid_point(cloudlets: Cloudlets, p: Point) -> bool:
    if not (0 <= p.y < len(cloudlets)):
        return False
    if not (0 <= p.x < len(cloudlets[p.y])):
        return False
    return True


def near_cloudlets(cloudlets: Cloudlets, p: Point, d_max: int, d_min: int) -> List[Cloudlet]:
    """
    近隣のCloudletを取得する。
    pからの距離がd_min以上でd_max以下のCloudletを取得する。
    :param cloudlets: 検索するCloudlets 
    :param p: 中心座標
    :param d_max: 最大距離
    :param d_min: 最小距離
    :return: 条件を満たす近隣Cloudletのリスト
    """
    near = []   # type: List[Cloudlet]
    for y in range(p.y-d_max, p.y+d_max+1):
        for x in range(p.x-d_max, p.x+d_max+1):
            if d_min <= distance(Point(x, y), p) <= d_max and is_valid_point(cloudlets, Point(x, y)):
                near.append(cloudlets[y][x])
    return near
