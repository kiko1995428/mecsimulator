"""
「プログラムの概要」
リソース割り当てアルゴリズムに関する内容を記述している。
"""
from simulator.model.cloudlet import Cloudlet, AllTimeCloudlets
from simulator.model.device import Device, Devices
from simulator.model.allocation import Allocation, AllocationPlan, create_blank_allocation_plan
from simulator.model.point import Point, distance, near_points
from simulator.utility.search import search
from typing import List, Dict
from tqdm import tqdm
import random
import time as itime
import os
from simulator.model.application import Application
import numpy as np

#混雑度を視覚化
def print_congestion(congestion_map, x_len, y_len):
    print("----------------------------------------------")
    for y in range(0, y_len):
        for x in range(0, x_len):
            OKBLUE = '\033[94m'
            OKGREEN = '\033[92m'
            WARNING = '\033[93m'
            FAIL = '\033[91m'
            ENDC = '\033[0m'
            num = congestion_map[y][x]
            if num < 50:
                print("{0:03}".format(num), end=",")
            elif num < 100:
                print(OKBLUE + "{0:03}".format(num) + ENDC, end=",")
            elif num < 150:
                print(OKGREEN + "{0:03}".format(num) + ENDC, end=",")
            elif num < 200:
                print(WARNING + "{0:03}".format(num) + ENDC, end=",")
            else:
                print(FAIL + "{0:03}".format(num) + ENDC, end=",")
        print("")
    print("----------------------------------------------")

#
def allocate(device: Device, time, allocate_pos: Point, allocation_plan, cloudlets: List[List[Cloudlet]]) -> None:
    cloudlets[allocate_pos.y][allocate_pos.x].append_device(device)
    d_pos = device.get_pos(time) #ある時刻のデバイスの座標を取得
    #distanceは２点間の座標の距離を返す関数, Allocation()で割り当て計画の定義
    allocation = Allocation(allocate_pos.x, allocate_pos.y, distance(d_pos, allocate_pos))
    allocation_plan[device.name][time] = allocation #デバイス名と時間からなる２次元リストに割り当て計画を代入
    device.set_allocation_point(time, Point(allocation.x, allocation.y)) #割り当て


def create_tempallocation(t: int, devices: Devices, max_hop: int=3) -> Dict[str, Point]:
    """
    指定された時間での仮割り当て位置を指定した辞書オブジェクトを生成する
    :param t: 指定時間
    :param devices: 端末集合
    :param max_hop: 許容する最大ホップ数
    :return: 
    """
    tempallocation = {}
    ds = filter(lambda d: d.is_poweron(t), devices)
    for d in ds:
        if d.name == "d23":
            d.name = d.name
        d_now = d.get_pos(t)
        if d.startup_time == t:
            # 起動したばかりの場合
            if d.shutdown_time <= t + max_hop:
                tempallocation[d.name] = d_now
                continue
            else:
                tempnext_c = d.get_pos(t + max_hop)
                tempallocation[d.name] = tempnext_c
                continue

        prev_c = d.get_allocation_point(t - 1)
        if d.shutdown_time <= t + max_hop:
            # シャットダウンが間近な場合
            tempallocation[d.name] = prev_c
            continue

        if distance(d_now, prev_c) >= max_hop:
            tempnext_c = d.get_pos(t + max_hop)
            tempallocation[d.name] = tempnext_c
        else:
            tempallocation[d.name] = prev_c

    return tempallocation


def simple_create_congestion_map(t: int, x_len: int, y_len: int, devices: Devices, scope: int) -> List[List[int]]:
    """
    仮割り当てを用いて混雑度マップを生成する
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
        pos = d.get_pos(t)
        pts = near_points(pos, scope, Point(x_len - 1, y_len - 1), Point(0, 0))
        for p in pts:
            ret[p.y][p.x] += d.use_resource
    return ret

def create_app_cong_map(t: int, x_len: int, y_len: int, devices: Devices, scope: int,
                          tempallocation: Dict[str, Point]) -> List[List[int]]:
    """
    仮割り当てを用いてアプリ用混雑度マップを生成する
    :param t: アプリ用混雑度マップを生成する時間
    :param x_len: xの長さ？
    :param y_len: yの長さ？
    :param devices: デバイス集合
    :param scope: 端末位置からどの程度はなれた範囲まで混雑度を加算するかを示す値
    :return:
    """
    ret = [[0 for x in range(x_len)] for y in range(y_len)]
    ds = list(filter(lambda d: d.is_poweron(t), devices))
    for d in ds:
        pos = tempallocation[d.name]
        pts = near_points(pos, scope, Point(x_len - 1, y_len - 1), Point(0, 0))
        for p in pts:
            ret[p.y][p.x] += d.use_resource

    return ret


def create_congestion_map(t: int, x_len: int, y_len: int, devices: Devices, scope: int,
                          tempallocation: Dict[str, Point]) -> List[List[int]]:
    """
    仮割り当てを用いて混雑度マップを生成する
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
        pos = tempallocation[d.name]
        pts = near_points(pos, scope, Point(x_len - 1, y_len - 1), Point(0, 0))
        for p in pts:
            ret[p.y][p.x] += d.use_resource
    return ret


def create_simple_tempallocationdef(time: int, devices: Devices, max_hop: int=3) -> Dict[str, Point]:
    tempallocation = {}  # type:Dict[str, Point]
    ds = filter(lambda d: d.is_poweron(time), devices)
    for d in ds:
        if d.startup_time == time:
            # 起動直後の端末
            if d.shutdown_time <= time + max_hop:
                # 端末の実行終了が近い場合
                tempallocation[d.name] = d.get_pos(time)
            else:
                tempallocation[d.name] = d.get_pos(time + max_hop)
            continue
        else:
            # 起動後時間が経過した端末
            prev_c = d.get_allocation_point(time - 1)
            if distance(prev_c, d.get_pos(time)) > max_hop:
                # max_hopをオーバーしている場合
                if d.shutdown_time <= time + max_hop:
                    # 端末の実行終了が近い場合
                    tempallocation[d.name] = d.get_pos(time)
                else:
                    tempallocation[d.name] = d.get_pos(time + max_hop)
                continue
            else:
                tempallocation[d.name] = prev_c
                continue
    return tempallocation


def create_simple_congestion_map(t: int, x_len: int, y_len: int, devices: Devices, scope: int,
                          tempallocation: Dict[str, Point]) -> List[List[int]]:
    """
    仮割り当てを用いて混雑度マップを生成する
    :param t: 混雑度マップを生成する時間
    :param x_len: xの長さ？
    :param y_len: yの長さ？
    :param devices: デバイス集合
    :param scope: 端末位置からどの程度はなれた範囲まで混雑度を加算するかを示す値
    :param tempallocation: 
    :return: 
    """
    ret = [[0 for x in range(x_len)] for y in range(y_len)]
    ds = list(filter(lambda d: d.is_poweron(t), devices))
    for d in ds:
        pos = tempallocation[d.name]
        pts = near_points(pos, scope, Point(x_len - 1, y_len - 1), Point(0, 0))
        for p in pts:
            ret[p.y][p.x] += d.use_resource
    return ret


def simple_use_plan(kwargs) -> AllocationPlan:
    atcs = kwargs["atcs"]
    devices = kwargs["ds"]
    max_hop = kwargs["max_hop"]
    congestion_scope = kwargs["congestion_scope"]

    t_len = len(atcs)
    y_len = len(atcs[0])
    x_len = len(atcs[0][0])
    allocation_plan = create_blank_allocation_plan(atcs, devices)
    for time, cloudlets in enumerate(tqdm(atcs)):
        ds = list(filter(lambda d: d.is_poweron(time), devices))
        tempallocation = create_tempallocation(time, ds, max_hop)
        congestion_map = create_congestion_map(time, x_len, y_len, ds, congestion_scope, tempallocation)
        print_congestion(congestion_map, x_len, y_len)
        ds = sorted(ds, key=lambda d: congestion_map[tempallocation[d.name].y][tempallocation[d.name].x], reverse=True)
        for d in ds:
            pos = tempallocation[d.name]
            for hop in range(0, 30):
                nps = near_points(pos, hop, Point(x_len - 1, y_len - 1), Point(0, 0))
                nps = sorted(nps, key=lambda p: distance(p, d.get_pos(time)))
                tp, index = search(nps, True, key=lambda p: cloudlets[p.y][p.x].can_append_device(d))
                if index == -1:
                    continue
                allocate(d, time, tp, allocation_plan, cloudlets)
                break
            else:
                # どこにも割当られなかった場合
                allocation = Allocation(pos.x, pos.y, -1)
                allocation_plan[d.name][time] = allocation
                d.set_allocation_point(time, allocation)
                print("allocation failed", d.name, time)
    return allocation_plan


def simple_use_plan_02(kwargs) -> AllocationPlan:
    atcs = kwargs["atcs"]
    devices = kwargs["ds"]
    max_hop = kwargs["max_hop"]
    congestion_scope = kwargs["congestion_scope"]
    reqapp=["1", "2", "3"]
    t_len = len(atcs)
    y_len = len(atcs[0])
    x_len = len(atcs[0][0])
    # cloudlets の空計画の作成
    allocation_plan = create_blank_allocation_plan(atcs, devices)
    for time, cloudlets in enumerate(tqdm(atcs)):
        # ds 終了していないデバイスを集める
        ds = list(filter(lambda d: d.is_poweron(time), devices))
        #ds = sorted(ds,lambda d: d.app_name,reversed=True)
        dsa1 = list(filter(lambda d: d.appret(reqapp[0]), ds))
        dsa2 = list(filter(lambda d: d.appret(reqapp[1]), ds))
        dsa3 = list(filter(lambda d: d.appret(reqapp[2]), ds))
        a1_len = len(dsa1)
        a2_len = len(dsa2)
        a3_len = len(dsa3)
        # # 混雑度マップの作成
        congestion_mapa1 = simple_create_congestion_map(time, x_len, y_len, dsa1, congestion_scope)
        congestion_mapa2 = simple_create_congestion_map(time, x_len, y_len, dsa2, congestion_scope)
        congestion_mapa3 = simple_create_congestion_map(time, x_len, y_len, dsa3, congestion_scope)
        # # # # print_congestion(congestion_map, x_len, y_len)
        dsa1 = sorted(dsa1, key=lambda d: congestion_mapa1[d.get_pos(time).y][d.get_pos(time).x], reverse=True)
        dsa2 = sorted(dsa2, key=lambda d: congestion_mapa2[d.get_pos(time).y][d.get_pos(time).x], reverse=True)
        dsa3 = sorted(dsa3, key=lambda d: congestion_mapa3[d.get_pos(time).y][d.get_pos(time).x], reverse=True)
        # if(a1_len > a2_len):
        #     if(a1_len > a3_len):
        #         if(a2_len > a3_len):
        #             ds = dsa2 + dsa1 + dsa3
        #         else:
        #             ds = dsa3 + dsa1 + dsa2
        #     else:
        #         ds = dsa1 + dsa3 + dsa2
        # else:
        #     if(a1_len > a3_len):
        #         ds = dsa1 + dsa2 + dsa3
        #     else:
        #         if(a2_len > a3_len):
        #             ds = dsa2 + dsa3 + dsa1
        #         else:
        #             ds = dsa3 + dsa2 + dsa1

        #ds = dsa2 + dsa1 + dsa3
        ds = dsa1 + dsa3 + dsa2
        # congestion_map = simple_create_congestion_map(time, x_len, y_len, ds, congestion_scope)
        # ds_high = list(filter(lambda d: congestion_map[d.get_pos(time).y][d.get_pos(time).x] > 3), ds)
        # ds_low = list(filter(lambda d: congestion_map[d.get_pos(time).y][d.get_pos(time).x] < 3), ds)
        # ds = ds_high + ds_low

        for d in ds:
            # step1 前回と同じ場所に置くことが適切かどうか判定し、適切なら配置を試行する
            now_pos = d.get_pos(time)
            if d.startup_time != time:
                prev_pos = d.get_allocation_point(time - 1)
                if distance(prev_pos, now_pos) <= max_hop:
                    # 前回と同じ場所に置くことを試行する
                    if cloudlets[prev_pos.y][prev_pos.x].can_append_device(d, True):
                        allocate(d, time, prev_pos, allocation_plan, cloudlets)
                        continue
            # step2 
            if d.is_poweron(time + max_hop):
                next_pos = d.get_pos(time + max_hop)
            else:
                next_pos = d.get_pos(d.shutdown_time - 1)
            for hop in range(max_hop, 30):
                nps = near_points(now_pos, hop, Point(x_len - 1, y_len - 1), Point(0, 0))
                nps = sorted(nps, key=lambda p: distance(p, next_pos))
                tp, index = search(nps, True, key=lambda p: cloudlets[p.y][p.x].can_append_device(d, True))
                if index == -1:
                    continue
                allocate(d, time, tp, allocation_plan, cloudlets)
                break
            else:
                # どこにも割当られなかった場合
                allocation = Allocation(now_pos.x, now_pos.y, -1)
                allocation_plan[d.name][time] = allocation
                d.set_allocation_point(time, allocation)
                print("allocation failed", d.name, time)

    return allocation_plan

def simple_use_plan_03(kwargs) -> AllocationPlan:
    atcs = kwargs["atcs"]
    devices = kwargs["ds"]
    max_hop = kwargs["max_hop"]
    congestion_scope = kwargs["congestion_scope"]
    reqapp=["1", "2", "3"]
    t_len = len(atcs)
    y_len = len(atcs[0])
    x_len = len(atcs[0][0])
    # cloudlets の空計画の作成
    allocation_plan = create_blank_allocation_plan(atcs, devices)
    for time, cloudlets in enumerate(tqdm(atcs)):
        # ds 終了していないデバイスを集める
        ds = list(filter(lambda d: d.is_poweron(time), devices))
        congestion_map = simple_create_congestion_map(time, x_len, y_len, ds, congestion_scope)
        cong_app_ds = []
        congestion_map1 = [[1,3,4,5,6,7,10],[2,4,5,12,5,3,11],[2,1,3,1,6,7,8]]
        dsa1 = list(filter(lambda d: d.appret(reqapp[0]), max_congest_ds))
        dsa2 = list(filter(lambda d: d.appret(reqapp[1]), max_congest_ds))
        dsa3 = list(filter(lambda d: d.appret(reqapp[2]), max_congest_ds))
        dsa = dsa2 + dsa1 + dsa3
            #cong_app_ds.extend(dsa)
            #print ("a")
        for d in ds:
            # step1 前回と同じ場所に置くことが適切かどうか判定し、適切なら配置を試行する
            now_pos = d.get_pos(time)
            if d.startup_time != time:
                prev_pos = d.get_allocation_point(time - 1)
                if distance(prev_pos, now_pos) <= max_hop:
                    # 前回と同じ場所に置くことを試行する
                    if cloudlets[prev_pos.y][prev_pos.x].can_append_device(d, True):
                        allocate(d, time, prev_pos, allocation_plan, cloudlets)
                        continue
            # step2
            if d.is_poweron(time + max_hop):
                next_pos = d.get_pos(time + max_hop)
            else:
                next_pos = d.get_pos(d.shutdown_time - 1)
            for hop in range(max_hop, 30):
                nps = near_points(now_pos, hop, Point(x_len - 1, y_len - 1), Point(0, 0))
                nps = sorted(nps, key=lambda p: distance(p, next_pos))
                tp, index = search(nps, True, key=lambda p: cloudlets[p.y][p.x].can_append_device(d, True))
                if index == -1:
                    continue
                allocate(d, time, tp, allocation_plan, cloudlets)
                break
            else:
                # どこにも割当られなかった場合
                allocation = Allocation(now_pos.x, now_pos.y, -1)
                allocation_plan[d.name][time] = allocation
                d.set_allocation_point(time, allocation)
                print("allocation failed", d.name, time)

    return allocation_plan

def set_device_set_pri(atcs: AllTimeCloudlets, cong_map: List[List[int]], t: int, devices: Devices,
                       x_len: int, y_len: int, scope: int):
    ds = list(filter(lambda d: d.is_poweron(t), devices))
    d_num = 0
    for d in ds:
        app_name = d.app_name()
        app_num = 0
        pos = d.get_pos(t)
        pts = near_points(pos, scope, Point(x_len - 1, y_len - 1), Point(0, 0))
        for p in pts:
            cloud = atcs[p.y][p.x][0]
            if cloud.is_operatable_application(app_name):
                app_num += 1
        pri_num = int(cong_map[pos.y][pos.x]) #/ app_num) #+ cong_map[pos.y][pos.x])
        #pri_num = app_num
        d.set_ds_pri(value=pri_num)

def set_device_set_pri2(atcs: AllTimeCloudlets, cong_map: List[List[int]], t: int, devices: Devices,
                       x_len: int, y_len: int, scope: int):
    ds = list(filter(lambda d: d.is_poweron(t), devices))
    d_num = 0
    i=0
    for d in ds:
        app_name = d.app_name()
        app_num = [0,0,0]
        pos = d.get_pos(t)
        pts = near_points(pos, scope, Point(x_len - 1, y_len - 1), Point(0, 0))
        for p in pts:
            cloud = atcs[p.y][p.x][0]
            if cloud.is_operatable_application("1"):
                app_num[0] += 1
                i += 1
            if cloud.is_operatable_application("2"):
                app_num[1] += 1
                i += 1
            if cloud.is_operatable_application("3"):
                app_num[2] += 1
                i += 1

        max_len = [0,0,0]
        for i in range(0,3):
            max_len[i] = str(np.argmax(app_num) + 1)
            app_num[int(max_len[i]) - 1] = 0

        if app_name == max_len[2]:
            pri_num = int(cong_map[pos.y][pos.x] + 2)
        elif app_name == max_len[1]:
            pri_num = int(cong_map[pos.y][pos.x] + 1)
        else:
            pri_num = int(cong_map[pos.y][pos.x])
        #pri_num = app_num
        d.set_ds_pri(value=pri_num)

def set_app_pri(atcs: AllTimeCloudlets, cong_map: List[List[int]], t: int, devices: Devices,
                        x_len: int, y_len: int, req_app: List[int], scope: int):
    ds = list(filter(lambda d: d.is_poweron(t), devices))
    d_num = 0
    for d in ds:
        app_name = d.app_name()
        app_num = 0
        pos = d.get_pos(t)
        pts = near_points(pos, scope, Point(x_len - 1, y_len - 1), Point(0, 0))
        for p in pts:
            cloud = atcs[p.y][p.x][0]
            if cloud.is_operatable_application(app_name):
                app_num += 1
        pri_num = int(app_num)
        if app_name == req_app[1]:
            pri_num += 3
        elif app_name == req_app[0]:
            pri_num += 2
        elif app_name == req_app[2]:
            pri_num += 1
        #pri_num = app_num
        d.set_ds_pri(value=pri_num)


def set_pri_ds(atcs: AllTimeCloudlets, cong_map: List[List[int]], t: int, devices: Devices,
                        x_len: int, y_len: int, req_app: List[int], scope: int):
    ds = list(filter(lambda d: d.is_poweron(t), devices))
    for d in ds:
        app_name = d.app_name()
        app_num = 0
        pos = d.get_pos(t)
        cloud = atcs[pos.y][pos.x][0]
        pri_num = int(cong_map[pos.y][pos.x] / app_num)
        # pri_num = app_num
        d.set_ds_pri(value=pri_num)


def simple_use_plan_04(kwargs) -> AllocationPlan:
    atcs = kwargs["atcs"]
    devices = kwargs["ds"]
    max_hop = kwargs["max_hop"]
    congestion_scope = kwargs["congestion_scope"]

    t_len = len(atcs)
    y_len = len(atcs[0])
    x_len = len(atcs[0][0])
    allocation_plan = create_blank_allocation_plan(atcs, devices)
    for time, cloudlets in enumerate(tqdm(atcs)):
        ds = list(filter(lambda d: d.is_poweron(time), devices))
        reqapp = ["1","2","3"]
        dsa1 = list(filter(lambda d: d.appret(reqapp[0]), ds))
        dsa2 = list(filter(lambda d: d.appret(reqapp[1]), ds))
        dsa3 = list(filter(lambda d: d.appret(reqapp[2]), ds))
        ds_app_len = [
            len(dsa1),
            len(dsa2),
            len(dsa3)
        ]
        max_len = [0,0,0]
        for i in range(0,3):
            max_len[i] = str(np.argmax(ds_app_len) + 1)
            ds_app_len[int(max_len[i]) - 1] = 0

        congestion_map = simple_create_congestion_map(time, x_len, y_len, ds, congestion_scope)
        # print_congestion(congestion_map, x_len, y_len)
        set_device_set_pri2(atcs, congestion_map, time, ds, x_len, y_len,congestion_scope)
        ds = sorted(ds, key=lambda d: d.ds_pri, reverse=True)

        for d in ds:
            # step1 前回と同じ場所に置くことが適切かどうか判定し、適切なら配置を試行する
            now_pos = d.get_pos(time)
            if d.startup_time != time:
                prev_pos = d.get_allocation_point(time - 1)
                if distance(prev_pos, now_pos) <= max_hop:
                    # 前回と同じ場所に置くことを試行する
                    if cloudlets[prev_pos.y][prev_pos.x].can_append_device(d, True):
                        allocate(d, time, prev_pos, allocation_plan, cloudlets)
                        continue
            # step2
            if d.is_poweron(time + max_hop):
                next_pos = d.get_pos(time + max_hop)
            else:
                next_pos = d.get_pos(d.shutdown_time - 1)
            for hop in range(max_hop, 30):
                nps = near_points(now_pos, hop, Point(x_len - 1, y_len - 1), Point(0, 0))
                nps = sorted(nps, key=lambda p: distance(p, next_pos))
                tp, index = search(nps, True, key=lambda p: cloudlets[p.y][p.x].can_append_device(d, True))
                if index == -1:
                    continue
                allocate(d, time, tp, allocation_plan, cloudlets)
                break
            else:
                # どこにも割当られなかった場合
                allocation = Allocation(now_pos.x, now_pos.y, -1)
                allocation_plan[d.name][time] = allocation
                d.set_allocation_point(time, allocation)
                print("allocation failed", d.name, time)
    return allocation_plan

def simple_use_plan_05(kwargs) -> AllocationPlan:
    atcs = kwargs["atcs"]
    devices = kwargs["ds"]
    max_hop = kwargs["max_hop"]
    congestion_scope = kwargs["congestion_scope"]

    t_len = len(atcs)
    y_len = len(atcs[0])
    x_len = len(atcs[0][0])
    allocation_plan = create_blank_allocation_plan(atcs, devices)
    for time, cloudlets in enumerate(tqdm(atcs)):
        ds = list(filter(lambda d: d.is_poweron(time), devices))
        reqapp = ["1","2","3","4","5"]
        #　reqapp ごとにデバイスを分ける
        dsa1 = list(filter(lambda d: d.appret(reqapp[0]), ds))
        dsa2 = list(filter(lambda d: d.appret(reqapp[1]), ds))
        dsa3 = list(filter(lambda d: d.appret(reqapp[2]), ds))
        #app4
        dsa4 = list(filter(lambda d: d.appret(reqapp[3]), ds))
        #app5
        dsa5 = list(filter(lambda d: d.appret(reqapp[4]), ds))
        # 要求数が多い順番を特定
        # ds_app_len = [
        #     len(dsa1),
        #     len(dsa2),
        #     len(dsa3)
        # ]
        # max_len = [0,0,0]
        # for i in range(0,3):
        #     max_len[i] = str(np.argmax(ds_app_len))
        #     ds_app_len[int(max_len[i])] = 0

        # app ごとの混雑度を計測
        congestion_mapa1 = simple_create_congestion_map(time, x_len, y_len, dsa1, congestion_scope)
        congestion_mapa2 = simple_create_congestion_map(time, x_len, y_len, dsa2, congestion_scope)
        congestion_mapa3 = simple_create_congestion_map(time, x_len, y_len, dsa3, congestion_scope)
        #app4
        #congestion_mapa4 = simple_create_congestion_map(time, x_len, y_len, dsa4, congestion_scope)
        #set_device_set_pri(atcs, congestion_mapa4, time, dsa4, x_len, y_len, congestion_scope)
        #app5
        #congestion_mapa5 = simple_create_congestion_map(time, x_len, y_len, dsa5, congestion_scope)
        #set_device_set_pri(atcs, congestion_mapa4, time, dsa5, x_len, y_len, congestion_scope)
        # app ごとの混雑度と近傍の利用可能cloudletの
        set_device_set_pri(atcs, congestion_mapa1, time, dsa1, x_len, y_len, congestion_scope)
        set_device_set_pri(atcs, congestion_mapa2, time, dsa2, x_len, y_len, congestion_scope)
        set_device_set_pri(atcs, congestion_mapa3, time, dsa3, x_len, y_len, congestion_scope)


        ds = sorted(ds, key=lambda d: d.ds_pri, reverse=True)

        for d in ds:
            # step1 前回と同じ場所に置くことが適切かどうか判定し、適切なら配置を試行する
            now_pos = d.get_pos(time)
            if d.startup_time != time:
                prev_pos = d.get_allocation_point(time - 1)
                if distance(prev_pos, now_pos) <= max_hop:
                    # 前回と同じ場所に置くことを試行する
                    if cloudlets[prev_pos.y][prev_pos.x].can_append_device(d, True):
                        allocate(d, time, prev_pos, allocation_plan, cloudlets)
                        continue
            # step2
            if d.is_poweron(time + max_hop):
                next_pos = d.get_pos(time + max_hop)
            else:
                next_pos = d.get_pos(d.shutdown_time - 1)
            for hop in range(max_hop, 30):
                nps = near_points(now_pos, hop, Point(x_len - 1, y_len - 1), Point(0, 0))
                nps = sorted(nps, key=lambda p: distance(p, next_pos))
                tp, index = search(nps, True, key=lambda p: cloudlets[p.y][p.x].can_append_device(d, True))
                if index == -1:
                    continue
                allocate(d, time, tp, allocation_plan, cloudlets)
                break
            else:
                # どこにも割当られなかった場合
                allocation = Allocation(now_pos.x, now_pos.y, -1)
                allocation_plan[d.name][time] = allocation
                d.set_allocation_point(time, allocation)
                print("allocation failed", d.name, time)
    return allocation_plan
def simple_use_plan_06(kwargs) -> AllocationPlan:
    atcs = kwargs["atcs"]
    devices = kwargs["ds"]
    max_hop = kwargs["max_hop"]
    congestion_scope = kwargs["congestion_scope"]

    t_len = len(atcs)
    y_len = len(atcs[0])
    x_len = len(atcs[0][0])
    allocation_plan = create_blank_allocation_plan(atcs, devices)
    for time, cloudlets in enumerate(tqdm(atcs)):
        ds = list(filter(lambda d: d.is_poweron(time), devices))
        reqapp = ["1","2","3"]
        #　reqapp ごとにデバイスを分ける
        dsa1 = list(filter(lambda d: d.appret(reqapp[0]), ds))
        dsa2 = list(filter(lambda d: d.appret(reqapp[1]), ds))
        dsa3 = list(filter(lambda d: d.appret(reqapp[2]), ds))
        # 要求数が多い順番を特定
        ds_app_len = [
            len(dsa1),
            len(dsa2),
            len(dsa3)
        ]
        max_len = [0,0,0]
        for i in range(0,3):
            max_len[i] = str(np.argmax(ds_app_len))
            ds_app_len[int(max_len[i])] = 0

        # app ごとの混雑度を計測
        congestion_mapa1 = simple_create_congestion_map(time, x_len, y_len, dsa1, congestion_scope)
        congestion_mapa2 = simple_create_congestion_map(time, x_len, y_len, dsa2, congestion_scope)
        congestion_mapa3 = simple_create_congestion_map(time, x_len, y_len, dsa3, congestion_scope)
        # app ごとの混雑度と近傍の利用可能cloudletの
        set_app_pri(atcs, congestion_mapa1, time, dsa1, x_len, y_len, max_len, congestion_scope)
        set_app_pri(atcs, congestion_mapa2, time, dsa2, x_len, y_len, max_len, congestion_scope)
        set_app_pri(atcs, congestion_mapa3, time, dsa3, x_len, y_len, max_len, congestion_scope)

        ds = sorted(ds, key=lambda d: d.ds_pri, reverse=False)

        for d in ds:
            # step1 前回と同じ場所に置くことが適切かどうか判定し、適切なら配置を試行する
            now_pos = d.get_pos(time)
            if d.startup_time != time:
                prev_pos = d.get_allocation_point(time - 1)
                if distance(prev_pos, now_pos) <= max_hop:
                    # 前回と同じ場所に置くことを試行する
                    if cloudlets[prev_pos.y][prev_pos.x].can_append_device(d, True):
                        allocate(d, time, prev_pos, allocation_plan, cloudlets)
                        continue
            # step2
            if d.is_poweron(time + max_hop):
                next_pos = d.get_pos(time + max_hop)
            else:
                next_pos = d.get_pos(d.shutdown_time - 1)
            for hop in range(max_hop, 30):
                nps = near_points(now_pos, hop, Point(x_len - 1, y_len - 1), Point(0, 0))
                nps = sorted(nps, key=lambda p: distance(p, next_pos))
                tp, index = search(nps, True, key=lambda p: cloudlets[p.y][p.x].can_append_device(d, True))
                if index == -1:
                    continue
                allocate(d, time, tp, allocation_plan, cloudlets)
                break
            else:
                # どこにも割当られなかった場合
                allocation = Allocation(now_pos.x, now_pos.y, -1)
                allocation_plan[d.name][time] = allocation
                d.set_allocation_point(time, allocation)
                print("allocation failed", d.name, time)
    return allocation_plan

def simple_use_plan_07(kwargs) -> AllocationPlan:
    atcs = kwargs["atcs"]
    devices = kwargs["ds"]
    max_hop = kwargs["max_hop"]
    congestion_scope = kwargs["congestion_scope"]

    t_len = len(atcs)
    y_len = len(atcs[0])
    x_len = len(atcs[0][0])
    allocation_plan = create_blank_allocation_plan(atcs, devices)
    for time, cloudlets in enumerate(tqdm(atcs)):
        ds = list(filter(lambda d: d.is_poweron(time), devices))
        congestion_map = simple_create_congestion_map(time, x_len, y_len, ds, congestion_scope)
        # print_congestion(congestion_map, x_len, y_len)
        ds = sorted(ds, key=lambda d: congestion_map[d.get_pos(time).y][d.get_pos(time).x], reverse=True)
        for d in ds:
            # step1 前回と同じ場所に置くことが適切かどうか判定し、適切なら配置を試行する
            now_pos = d.get_pos(time)
            if d.startup_time != time:
                prev_pos = d.get_allocation_point(time - 1)
                if distance(prev_pos, now_pos) <= max_hop:
                    # 前回と同じ場所に置くことを試行する
                    if cloudlets[prev_pos.y][prev_pos.x].can_append_device(d, True):
                        allocate(d, time, prev_pos, allocation_plan, cloudlets)
                        continue
            # step2
            if d.is_poweron(time + max_hop):
                next_pos = d.get_pos(time + max_hop)
            else:
                next_pos = d.get_pos(d.shutdown_time - 1)
            for hop in range(max_hop, 30):
                nps = near_points(now_pos, hop, Point(x_len - 1, y_len - 1), Point(0, 0))
                nps = sorted(nps, key=lambda p: distance(p, next_pos))
                tp, index = search(nps, True, key=lambda p: cloudlets[p.y][p.x].can_append_device(d, True))
                if index == -1:
                    continue
                allocate(d, time, tp, allocation_plan, cloudlets)
                break
            else:
                # どこにも割当られなかった場合
                allocation = Allocation(now_pos.x, now_pos.y, -1)
                allocation_plan[d.name][time] = allocation
                d.set_allocation_point(time, allocation)
                print("allocation failed", d.name, time)
    return allocation_plan


