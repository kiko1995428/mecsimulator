from simulator.model.cloudlet import Cloudlet, AllTimeCloudlets
from simulator.model.device import Device, Devices
from simulator.model.allocation import Allocation, AllocationPlan, create_blank_allocation_plan
from simulator.model.point import Point, distance, near_points
from simulator.utility.search import search
from typing import List, Dict
from tqdm import tqdm
import random
import time as itime


def create_congestion_map(t: int, x_len: int, y_len: int, devices: Devices, scope: int) -> List[List[int]]:
    """
    混雑度マップを生成する
    :param t: 混雑度マップを生成する時間
    :param x_len: xの長さ？
    :param y_len: yの長さ？
    :param devices: デバイス集合
    :param scope: 端末位置からどの程度はなれた範囲まで混雑度を加算するかを示す値
    :return: 
    """
    ret = [[0 for x in range(x_len)] for y in range(y_len)]
    ds = list(filter(lambda d: d.is_poweron(t), devices))
    for d in ds:
        pts = near_points(d.get_pos(t), scope, Point(x_len - 1, y_len - 1), Point(0, 0))
        for p in pts:
            ret[p.y][p.x] += d.use_resource
    return ret


def congestion_priority(kwards) -> AllocationPlan:
    """
    混雑Cloudletの直轄地にあるデバイスを優先して割り当てる方式
    :param atcs: すべての時間のCloudlet集合
    :param devices: すべてのデバイス集合
    :return: 
    """
    atcs = kwards["atcs"]
    devices = kwards["ds"]

    t_len = len(atcs)
    y_len = len(atcs[0])
    x_len = len(atcs[0][0])
    allocation_plan = create_blank_allocation_plan(atcs, devices)
    for time, cloudlets in enumerate(tqdm(atcs)):
        ds = list(filter(lambda d: d.is_poweron(time), devices))
        requests = create_congestion_map(time, len(cloudlets[0]), len(cloudlets), ds, 3)
        ds = sorted(ds, key=lambda d: requests[d.get_pos(time).y][d.get_pos(time).x], reverse=True)
        for d in ds:
            pos = d.get_pos(time)
            for hop in range(0, 30):
                nps = near_points(pos, hop, Point(x_len - 1, y_len - 1), Point(0, 0))
                tp, index = search(nps, True, key=lambda p: cloudlets[p.y][p.x].can_append_device(d))
                if index == -1:
                    continue
                cloudlets[tp.y][tp.x].append_device(d)
                allocation = Allocation(tp.x, tp.y, distance(pos, tp))
                allocation_plan[d.name][time] = allocation
                d.set_allocation_point(time, Point(allocation.x, allocation.y))
                break
            else:
                # どこにも割当られなかった場合
                allocation = Allocation(pos.x, pos.y, -1)
                allocation_plan[d.name][time] = allocation
                d.set_allocation_point(time, Point(allocation.x, allocation.y))
    return allocation_plan
