# coding:utf-8
"""
oldallocation.py
Author          : Kouhei Osaki
Created         : 2017/06/11
Last-Modified   : 2017/07/17
Version         : 2.1.2
Description     : リソースの割当処理を行うメソッドを定義している。 
"""


from simulator.oldmodels import Allocation, AllTimeCloudlets, Devices, AllocationPlan, Cloudlets
from simulator.oldutility import create_blank_allocation_plan, get_cloudlet_point_from_cloudlets
from simulator.utility.cloudlet import near_cloudlets
from simulator.utility.point import extract
from tqdm import tqdm
from typing import List
import random


def decreasing(all_time_cloudlets: AllTimeCloudlets, devices: Devices) -> AllocationPlan:
    """
    シンプルなFFDアルゴリズムによる割当て
    リソース不足時に周辺のCloudletの探索を行わない
    旧models.FFD_allocation
    :param all_time_cloudlets: Cloudletの三次元リスト
    :param devices: Deviceのリスト
    :return: 割り当て計画
    """
    allocation_plan = create_blank_allocation_plan(all_time_cloudlets, devices)
    devices = sorted(devices, key=lambda c: c.use_resource, reverse=True)
    # time : 現在の時間, cloudlets : 現在の各クラウドレット
    for time, cloudlets in enumerate(all_time_cloudlets):
        for device in devices:
            if not (device.startup_time <= time < device.shutdown_time):
                # デバイス（端末）が稼働していない時間の場合
                continue
            # time時間での端末の位置を取得
            pos = device.plan[time - device.startup_time]
            cloudlet = cloudlets[pos.y][pos.x]
            if cloudlet.can_append_device(device):
                # 割当可能な場合
                cloudlet.append_device(device)
                allocation_plan[device.name][time] = Allocation(pos.x, pos.y, 0)
            else:
                # 割当できない場合
                allocation_plan[device.name][time] = Allocation(pos.x, pos.y, -1)
    return allocation_plan


def increasing(all_time_cloudlets: AllTimeCloudlets, devices: Devices) -> AllocationPlan:
    """
    シンプルなFFiアルゴリズムによる割当て
    リソース不足時に周辺のCloudletの探索を行わない
    :param all_time_cloudlets: Cloudletの三次元リスト
    :param devices: Deviceのリスト
    :return: 割り当て計画
    """
    allocation_plan = create_blank_allocation_plan(all_time_cloudlets, devices)
    devices = sorted(devices, key=lambda c: c.use_resource)
    # time : 現在の時間, cloudlets : 現在の各クラウドレット
    for time, cloudlets in enumerate(all_time_cloudlets):
        for device in devices:
            if not (device.startup_time <= time < device.shutdown_time):
                # デバイス（端末）が稼働していない時間の場合
                continue
            # time時間での端末の位置を取得
            pos = device.plan[time - device.startup_time]
            cloudlet = cloudlets[pos.y][pos.x]
            if cloudlet.can_append_device(device):
                # 割当可能な場合
                cloudlet.append_device(device)
                allocation_plan[device.name][time] = Allocation(pos.x, pos.y, 0)
            else:
                # 割当できない場合
                allocation_plan[device.name][time] = Allocation(pos.x, pos.y, -1)
    return allocation_plan


def simple(all_time_cloudlets: AllTimeCloudlets, devices: Devices) -> AllocationPlan:
    """
    シンプルなFFアルゴリズムによる割当て
    リソース不足時に周辺のCloudletの探索を行わない
    :param all_time_cloudlets: Cloudletの三次元リスト
    :param devices: Deviceのリスト
    :return: 割り当て計画
    """
    allocation_plan = create_blank_allocation_plan(all_time_cloudlets, devices)
    # time : 現在の時間, cloudlets : 現在の各クラウドレット
    for time, cloudlets in enumerate(all_time_cloudlets):
        for device in devices:
            if not (device.startup_time <= time < device.shutdown_time):
                # デバイス（端末）が稼働していない時間の場合
                continue
            # time時間での端末の位置を取得
            pos = device.plan[time - device.startup_time]
            cloudlet = cloudlets[pos.y][pos.x]
            if cloudlet.can_append_device(device):
                # 割当可能な場合
                cloudlet.append_device(device)
                allocation_plan[device.name][time] = Allocation(pos.x, pos.y, 0)
            else:
                # 割当できない場合
                allocation_plan[device.name][time] = Allocation(pos.x, pos.y, -1)
    return allocation_plan


def ff(all_time_cloudlets: AllTimeCloudlets, devices: Devices) -> AllocationPlan:
    """
    FFDアルゴリズムによる割当と、
    リソース不足時に最もリソースの空きの大きい周辺Cloudletを探索を行う
    :param all_time_cloudlets: 
    :param devices: 
    :return: 
    """
    allocation_plan = create_blank_allocation_plan(all_time_cloudlets, devices)
    # time : 現在の時間, cloudlets : 現在の各クラウドレット
    for time, cloudlets in enumerate(tqdm(all_time_cloudlets)):
        for device in devices:
            if not (device.startup_time <= time < device.shutdown_time):
                # デバイス（端末）が稼働していない時間の場合
                continue
            # time時間での端末の位置を取得
            pos = device.plan[time - device.startup_time]
            for hop in range(0, 10):
                near = near_cloudlets(cloudlets, pos, d_max=hop, d_min=hop)
                near = list(filter(lambda c: c.can_append_device(device), near))
                if len(near) == 0:
                    continue
                cloudlet = near[0]
                cloudlet.append_device(device)
                p = get_cloudlet_point_from_cloudlets(cloudlet.name, cloudlets=cloudlets)
                allocation_plan[device.name][time] = Allocation(p.x, p.y, hop)
                break
            else:
                # どこにも割当られなかった場合
                allocation_plan[device.name][time] = Allocation(pos.x, pos.y, -1)
    return allocation_plan


def ff_best(all_time_cloudlets: AllTimeCloudlets, devices: Devices) -> AllocationPlan:
    """
    FFDアルゴリズムによる割当と、
    リソース不足時に最もリソースの空きの大きい周辺Cloudletを探索を行う
    :param all_time_cloudlets: 
    :param devices: 
    :return: 
    """
    allocation_plan = create_blank_allocation_plan(all_time_cloudlets, devices)
    # time : 現在の時間, cloudlets : 現在の各クラウドレット
    for time, cloudlets in enumerate(tqdm(all_time_cloudlets)):
        for device in devices:
            if not (device.startup_time <= time < device.shutdown_time):
                # デバイス（端末）が稼働していない時間の場合
                continue
            # time時間での端末の位置を取得
            pos = device.plan[time - device.startup_time]
            for hop in range(0, 10):
                near = near_cloudlets(cloudlets, pos, d_max=hop, d_min=hop)
                near = list(filter(lambda c: c.can_append_device(device), near))
                if len(near) == 0:
                    continue
                cloudlet = min(near, key=lambda c: c.empty_resource)
                cloudlet.append_device(device)
                p = get_cloudlet_point_from_cloudlets(cloudlet.name, cloudlets=cloudlets)
                allocation_plan[device.name][time] = Allocation(p.x, p.y, hop)
                break
            else:
                # どこにも割当られなかった場合
                allocation_plan[device.name][time] = Allocation(pos.x, pos.y, -1)
    return allocation_plan


def ff_max(all_time_cloudlets: AllTimeCloudlets, devices: Devices) -> AllocationPlan:
    """
    FFDアルゴリズムによる割当と、
    リソース不足時に最もリソースの空きの大きい周辺Cloudletを探索を行う
    :param all_time_cloudlets: 
    :param devices: 
    :return: 
    """
    allocation_plan = create_blank_allocation_plan(all_time_cloudlets, devices)
    # time : 現在の時間, cloudlets : 現在の各クラウドレット
    for time, cloudlets in enumerate(tqdm(all_time_cloudlets)):
        for device in devices:
            if not (device.startup_time <= time < device.shutdown_time):
                # デバイス（端末）が稼働していない時間の場合
                continue
            # time時間での端末の位置を取得
            pos = device.plan[time - device.startup_time]
            for hop in range(0, 10):
                near = near_cloudlets(cloudlets, pos, d_max=hop, d_min=hop)
                if len(near) == 0:
                    continue

                cloudlet = max(near, key=lambda c: c.empty_resource)
                if cloudlet.can_append_device(device):
                    # 割当可能な場合
                    cloudlet.append_device(device)
                    p = get_cloudlet_point_from_cloudlets(cloudlet.name, cloudlets=cloudlets)
                    allocation_plan[device.name][time] = Allocation(p.x, p.y, hop)
                    break
            else:
                # どこにも割当られなかった場合
                allocation_plan[device.name][time] = Allocation(pos.x, pos.y, -1)
    return allocation_plan


def ffd(all_time_cloudlets: AllTimeCloudlets, devices: Devices) -> AllocationPlan:
    """
    FFDアルゴリズムによる割当と、
    リソース不足時に最もリソースの空きの大きい周辺Cloudletを探索を行う
    :param all_time_cloudlets: 
    :param devices: 
    :return: 
    """
    allocation_plan = create_blank_allocation_plan(all_time_cloudlets, devices)
    devices = sorted(devices, key=lambda c: c.use_resource, reverse=True)
    # time : 現在の時間, cloudlets : 現在の各クラウドレット
    for time, cloudlets in enumerate(tqdm(all_time_cloudlets)):
        for device in devices:
            if not (device.startup_time <= time < device.shutdown_time):
                # デバイス（端末）が稼働していない時間の場合
                continue
            # time時間での端末の位置を取得
            pos = device.plan[time - device.startup_time]
            for hop in range(0, 10):
                near = near_cloudlets(cloudlets, pos, d_max=hop, d_min=hop)
                near = list(filter(lambda c: c.can_append_device(device), near))
                if len(near) == 0:
                    continue
                cloudlet = near[0]
                # 割当可能な場合
                cloudlet.append_device(device)
                p = get_cloudlet_point_from_cloudlets(cloudlet.name, cloudlets=cloudlets)
                allocation_plan[device.name][time] = Allocation(p.x, p.y, hop)
                break
            else:
                # どこにも割当られなかった場合
                allocation_plan[device.name][time] = Allocation(pos.x, pos.y, -1)
    return allocation_plan


def ffd_best(all_time_cloudlets: AllTimeCloudlets, devices: Devices) -> AllocationPlan:
    """
    FFDアルゴリズムによる割当と、
    リソース不足時に最もリソースの空きの大きい周辺Cloudletを探索を行う
    :param all_time_cloudlets: 
    :param devices: 
    :return: 
    """
    allocation_plan = create_blank_allocation_plan(all_time_cloudlets, devices)
    devices = sorted(devices, key=lambda c: c.use_resource, reverse=True)
    # time : 現在の時間, cloudlets : 現在の各クラウドレット
    for time, cloudlets in enumerate(tqdm(all_time_cloudlets)):
        for device in devices:
            if not (device.startup_time <= time < device.shutdown_time):
                # デバイス（端末）が稼働していない時間の場合
                continue
            # time時間での端末の位置を取得
            pos = device.plan[time - device.startup_time]
            for hop in range(0, 10):
                near = near_cloudlets(cloudlets, pos, d_max=hop, d_min=hop)
                near = list(filter(lambda c: c.can_append_device(device), near))
                if len(near) == 0:
                    continue
                cloudlet = min(near, key=lambda c: c.empty_resource)
                # 割当可能な場合
                cloudlet.append_device(device)
                p = get_cloudlet_point_from_cloudlets(cloudlet.name, cloudlets=cloudlets)
                allocation_plan[device.name][time] = Allocation(p.x, p.y, hop)
                break
            else:
                # どこにも割当られなかった場合
                allocation_plan[device.name][time] = Allocation(pos.x, pos.y, -1)
    return allocation_plan


def ffd_max(all_time_cloudlets: AllTimeCloudlets, devices: Devices) -> AllocationPlan:
    """
    FFDアルゴリズムによる割当と、
    リソース不足時に最もリソースの空きの大きい周辺Cloudletを探索を行う
    :param all_time_cloudlets: 
    :param devices: 
    :return: 
    """
    allocation_plan = create_blank_allocation_plan(all_time_cloudlets, devices)
    devices = sorted(devices, key=lambda c: c.use_resource, reverse=True)
    # time : 現在の時間, cloudlets : 現在の各クラウドレット
    for time, cloudlets in enumerate(tqdm(all_time_cloudlets)):
        for device in devices:
            if not (device.startup_time <= time < device.shutdown_time):
                # デバイス（端末）が稼働していない時間の場合
                continue
            # time時間での端末の位置を取得
            pos = device.plan[time - device.startup_time]
            for hop in range(0, 10):
                near = near_cloudlets(cloudlets, pos, d_max=hop, d_min=hop)
                if len(near) == 0:
                    continue
                cloudlet = max(near, key=lambda c: c.empty_resource)
                if cloudlet.can_append_device(device):
                    # 割当可能な場合
                    cloudlet.append_device(device)
                    p = get_cloudlet_point_from_cloudlets(cloudlet.name, cloudlets=cloudlets)
                    allocation_plan[device.name][time] = Allocation(p.x, p.y, hop)
                    break
            else:
                # どこにも割当られなかった場合
                allocation_plan[device.name][time] = Allocation(pos.x, pos.y, -1)
    return allocation_plan


def ffi(all_time_cloudlets: AllTimeCloudlets, devices: Devices) -> AllocationPlan:
    """
    FFIアルゴリズムによる割当と、
    リソース不足時に最もリソースの空きの大きい周辺Cloudletを探索を行う
    :param all_time_cloudlets: 
    :param devices: 
    :return: 
    """
    allocation_plan = create_blank_allocation_plan(all_time_cloudlets, devices)
    devices = sorted(devices, key=lambda c: c.use_resource)
    # time : 現在の時間, cloudlets : 現在の各クラウドレット
    for time, cloudlets in enumerate(tqdm(all_time_cloudlets)):
        for device in devices:
            if not (device.startup_time <= time < device.shutdown_time):
                # デバイス（端末）が稼働していない時間の場合
                continue
            # time時間での端末の位置を取得
            pos = device.plan[time - device.startup_time]
            for hop in range(0, 10):
                near = near_cloudlets(cloudlets, pos, d_max=hop, d_min=hop)
                near = list(filter(lambda c: c.can_append_device(device), near))
                if len(near) == 0:
                    continue
                cloudlet = near[0]
                # 割当可能な場合
                cloudlet.append_device(device)
                p = get_cloudlet_point_from_cloudlets(cloudlet.name, cloudlets=cloudlets)
                allocation_plan[device.name][time] = Allocation(p.x, p.y, hop)
                break
            else:
                # どこにも割当られなかった場合
                allocation_plan[device.name][time] = Allocation(pos.x, pos.y, -1)
    return allocation_plan


def ffi_max(all_time_cloudlets: AllTimeCloudlets, devices: Devices) -> AllocationPlan:
    """
    FFIアルゴリズムによる割当と、
    リソース不足時に最もリソースの空きの大きい周辺Cloudletを探索を行う
    :param all_time_cloudlets: 
    :param devices: 
    :return: 
    """
    allocation_plan = create_blank_allocation_plan(all_time_cloudlets, devices)
    devices = sorted(devices, key=lambda c: c.use_resource)
    # time : 現在の時間, cloudlets : 現在の各クラウドレット
    for time, cloudlets in enumerate(tqdm(all_time_cloudlets)):
        for device in devices:
            if not (device.startup_time <= time < device.shutdown_time):
                # デバイス（端末）が稼働していない時間の場合
                continue
            # time時間での端末の位置を取得
            pos = device.plan[time - device.startup_time]
            for hop in range(0, 10):
                near = near_cloudlets(cloudlets, pos, d_max=hop, d_min=hop)
                if len(near) == 0:
                    continue
                cloudlet = max(near, key=lambda c: c.empty_resource)
                if cloudlet.can_append_device(device):
                    # 割当可能な場合
                    cloudlet.append_device(device)
                    p = get_cloudlet_point_from_cloudlets(cloudlet.name, cloudlets=cloudlets)
                    allocation_plan[device.name][time] = Allocation(p.x, p.y, hop)
                    break
            else:
                # どこにも割当られなかった場合
                allocation_plan[device.name][time] = Allocation(pos.x, pos.y, -1)
    return allocation_plan


def ffi_best(all_time_cloudlets: AllTimeCloudlets, devices: Devices) -> AllocationPlan:
    """
    FFIアルゴリズムによる割当と、
    リソース不足時に最もリソースの空きの大きい周辺Cloudletを探索を行う
    :param all_time_cloudlets: 
    :param devices: 
    :return: 
    """
    allocation_plan = create_blank_allocation_plan(all_time_cloudlets, devices)
    devices = sorted(devices, key=lambda c: c.use_resource)
    # time : 現在の時間, cloudlets : 現在の各クラウドレット
    for time, cloudlets in enumerate(tqdm(all_time_cloudlets)):
        for device in devices:
            if not (device.startup_time <= time < device.shutdown_time):
                # デバイス（端末）が稼働していない時間の場合
                continue
            # time時間での端末の位置を取得
            pos = device.plan[time - device.startup_time]
            for hop in range(0, 10):
                near = near_cloudlets(cloudlets, pos, d_max=hop, d_min=hop)
                near = list(filter(lambda c: c.can_append_device(device), near))
                if len(near) == 0:
                    continue
                cloudlet = min(near, key=lambda c: c.empty_resource)
                # 割当可能な場合
                cloudlet.append_device(device)
                p = get_cloudlet_point_from_cloudlets(cloudlet.name, cloudlets=cloudlets)
                allocation_plan[device.name][time] = Allocation(p.x, p.y, hop)
                break
            else:
                # どこにも割当られなかった場合
                allocation_plan[device.name][time] = Allocation(pos.x, pos.y, -1)
    return allocation_plan


# def select_min(atcs: AllTimeCloudlets, ds: Devices, interval: int=2) -> AllocationPlan:
#     ap = create_blank_allocation_plan(atcs, ds)
#     ds = sorted(ds, key=lambda c: c.use_resource, reverse=True)
#     for t, cs in enumerate(tqdm(atcs)):
#         for d in ds:
#             d_min = 1
#             d_max = d_min + interval
#             ctable = _check_request(cs, ds, t, d_min, d_max)
#             p = d.plan[t - d.startup_time]
#             pts = extract(p, d_max=d_max, d_min=d_min)
#             max([ for target_p in pts]
#
# def _check_request(cs: Cloudlets, ds: Devices, t: int, d_min: int=1, d_max: int=3) -> List[List[int]]:
#     check_table = [[0 for i in range(len(cs))] for j in range(len(cs[0]))]
#     for d in ds:
#         p = d.plan[t - d.startup_time]
#         pts = extract(p, d_max=d_max, d_min=d_min)
#         for tp in pts:
#             if 0 <= tp.y < len(check_table) and 0 <= tp.x < len(check_table[0]):
#                 check_table[tp.y][tp.x] += d.use_resource
#     return check_table


def ffv2(all_time_cloudlets: AllTimeCloudlets, devices: Devices) -> AllocationPlan:
    """
    :param all_time_cloudlets: 
    :param devices: 
    :return: 
    """
    allocation_plan = create_blank_allocation_plan(all_time_cloudlets, devices)
    random.shuffle(devices)
    # time : 現在の時間, cloudlets : 現在の各クラウドレット
    for time, cloudlets in enumerate(tqdm(all_time_cloudlets)):
        for device in devices:
            if not (device.startup_time <= time < device.shutdown_time):
                # デバイス（端末）が稼働していない時間の場合
                continue
            # time時間での端末の位置を取得
            pos = device.plan[time - device.startup_time]
            for hop in range(0, 30):
                near = near_cloudlets(cloudlets, pos, d_max=hop, d_min=hop)
                near = list(filter(lambda c: c.can_append_device(device), near))
                if len(near) == 0:
                    continue
                cloudlet = near[0]
                cloudlet.append_device(device)
                p = get_cloudlet_point_from_cloudlets(cloudlet.name, cloudlets=cloudlets)
                allocation_plan[device.name][time] = Allocation(p.x, p.y, hop)
                break
            else:
                # どこにも割当られなかった場合
                allocation_plan[device.name][time] = Allocation(pos.x, pos.y, -1)
    return allocation_plan


def ffdv2(all_time_cloudlets: AllTimeCloudlets, devices: Devices) -> AllocationPlan:
    """
    FFDアルゴリズムによる割当と、
    リソース不足時に最もリソースの空きの大きい周辺Cloudletを探索を行う
    :param all_time_cloudlets: 
    :param devices: 
    :return: 
    """
    allocation_plan = create_blank_allocation_plan(all_time_cloudlets, devices)
    random.shuffle(devices)
    devices = sorted(devices, key=lambda c: c.use_resource, reverse=True)
    # time : 現在の時間, cloudlets : 現在の各クラウドレット
    for time, cloudlets in enumerate(tqdm(all_time_cloudlets)):
        for device in devices:
            if not (device.startup_time <= time < device.shutdown_time):
                # デバイス（端末）が稼働していない時間の場合
                continue
            # time時間での端末の位置を取得
            pos = device.plan[time - device.startup_time]
            for hop in range(0, 30):
                near = near_cloudlets(cloudlets, pos, d_max=hop, d_min=hop)
                near = list(filter(lambda c: c.can_append_device(device), near))
                if len(near) == 0:
                    continue
                cloudlet = near[0]
                # 割当可能な場合
                cloudlet.append_device(device)
                p = get_cloudlet_point_from_cloudlets(cloudlet.name, cloudlets=cloudlets)
                allocation_plan[device.name][time] = Allocation(p.x, p.y, hop)
                break
            else:
                # どこにも割当られなかった場合
                allocation_plan[device.name][time] = Allocation(pos.x, pos.y, -1)
    return allocation_plan


def ffdv2_max(all_time_cloudlets: AllTimeCloudlets, devices: Devices) -> AllocationPlan:
    """
    FFDアルゴリズムによる割当と、
    リソース不足時に最もリソースの空きの大きい周辺Cloudletを探索を行う
    :param all_time_cloudlets: 
    :param devices: 
    :return: 
    """
    allocation_plan = create_blank_allocation_plan(all_time_cloudlets, devices)
    random.shuffle(devices)
    devices = sorted(devices, key=lambda c: c.use_resource, reverse=True)
    # time : 現在の時間, cloudlets : 現在の各クラウドレット
    for time, cloudlets in enumerate(tqdm(all_time_cloudlets)):
        for device in devices:
            if not (device.startup_time <= time < device.shutdown_time):
                # デバイス（端末）が稼働していない時間の場合
                continue
            # time時間での端末の位置を取得
            pos = device.plan[time - device.startup_time]
            for hop in range(0, 30):
                near = near_cloudlets(cloudlets, pos, d_max=hop, d_min=hop)
                near = list(filter(lambda c: c.can_append_device(device), near))
                if len(near) == 0:
                    continue
                cloudlet = max(near, key=lambda c: c.empty_resource)
                # 割当可能な場合
                cloudlet.append_device(device)
                p = get_cloudlet_point_from_cloudlets(cloudlet.name, cloudlets=cloudlets)
                allocation_plan[device.name][time] = Allocation(p.x, p.y, hop)
                break
            else:
                # どこにも割当られなかった場合
                allocation_plan[device.name][time] = Allocation(pos.x, pos.y, -1)
    return allocation_plan


def ffdv2_min(all_time_cloudlets: AllTimeCloudlets, devices: Devices) -> AllocationPlan:
    """
    FFDアルゴリズムによる割当と、
    リソース不足時に最もリソースの空きの大きい周辺Cloudletを探索を行う
    :param all_time_cloudlets: 
    :param devices: 
    :return: 
    """
    allocation_plan = create_blank_allocation_plan(all_time_cloudlets, devices)
    random.shuffle(devices)
    devices = sorted(devices, key=lambda c: c.use_resource, reverse=True)
    # time : 現在の時間, cloudlets : 現在の各クラウドレット
    for time, cloudlets in enumerate(tqdm(all_time_cloudlets)):
        for device in devices:
            if not (device.startup_time <= time < device.shutdown_time):
                # デバイス（端末）が稼働していない時間の場合
                continue
            # time時間での端末の位置を取得
            pos = device.plan[time - device.startup_time]
            for hop in range(0, 30):
                near = near_cloudlets(cloudlets, pos, d_max=hop, d_min=hop)
                near = list(filter(lambda c: c.can_append_device(device), near))
                if len(near) == 0:
                    continue
                cloudlet = min(near, key=lambda c: c.empty_resource)
                # 割当可能な場合
                cloudlet.append_device(device)
                p = get_cloudlet_point_from_cloudlets(cloudlet.name, cloudlets=cloudlets)
                allocation_plan[device.name][time] = Allocation(p.x, p.y, hop)
                break
            else:
                # どこにも割当られなかった場合
                allocation_plan[device.name][time] = Allocation(pos.x, pos.y, -1)
    return allocation_plan


def ffiv2(all_time_cloudlets: AllTimeCloudlets, devices: Devices) -> AllocationPlan:
    """
    FFIアルゴリズムによる割当と、
    リソース不足時に最もリソースの空きの大きい周辺Cloudletを探索を行う
    :param all_time_cloudlets: 
    :param devices: 
    :return: 
    """
    allocation_plan = create_blank_allocation_plan(all_time_cloudlets, devices)
    random.shuffle(devices)
    devices = sorted(devices, key=lambda c: c.use_resource)
    # time : 現在の時間, cloudlets : 現在の各クラウドレット
    for time, cloudlets in enumerate(tqdm(all_time_cloudlets)):
        for device in devices:
            if not (device.startup_time <= time < device.shutdown_time):
                # デバイス（端末）が稼働していない時間の場合
                continue
            # time時間での端末の位置を取得
            pos = device.plan[time - device.startup_time]
            for hop in range(0, 30):
                near = near_cloudlets(cloudlets, pos, d_max=hop, d_min=hop)
                near = list(filter(lambda c: c.can_append_device(device), near))
                if len(near) == 0:
                    continue
                cloudlet = near[0]
                # 割当可能な場合
                cloudlet.append_device(device)
                p = get_cloudlet_point_from_cloudlets(cloudlet.name, cloudlets=cloudlets)
                allocation_plan[device.name][time] = Allocation(p.x, p.y, hop)
                break
            else:
                # どこにも割当られなかった場合
                allocation_plan[device.name][time] = Allocation(pos.x, pos.y, -1)
    return allocation_plan


def ffv2no(all_time_cloudlets: AllTimeCloudlets, devices: Devices) -> AllocationPlan:
    """
    FFIアルゴリズムによる割当と、
    リソース不足時に最もリソースの空きの大きい周辺Cloudletを探索を行う
    :param all_time_cloudlets: 
    :param devices: 
    :return: 
    """
    allocation_plan = create_blank_allocation_plan(all_time_cloudlets, devices)
    #random.shuffle(devices)
    #devices = sorted(devices, key=lambda c: c.use_resource)
    # time : 現在の時間, cloudlets : 現在の各クラウドレット
    for time, cloudlets in enumerate(tqdm(all_time_cloudlets)):
        for device in devices:
            if not (device.startup_time <= time < device.shutdown_time):
                # デバイス（端末）が稼働していない時間の場合
                continue
            # time時間での端末の位置を取得
            pos = device.plan[time - device.startup_time]
            for hop in range(0, 30):
                near = near_cloudlets(cloudlets, pos, d_max=hop, d_min=hop)
                near = list(filter(lambda c: c.can_append_device(device), near))
                if len(near) == 0:
                    continue
                cloudlet = near[0]
                # 割当可能な場合
                cloudlet.append_device(device)
                p = get_cloudlet_point_from_cloudlets(cloudlet.name, cloudlets=cloudlets)
                allocation_plan[device.name][time] = Allocation(p.x, p.y, hop)
                break
            else:
                # どこにも割当られなかった場合
                allocation_plan[device.name][time] = Allocation(pos.x, pos.y, -1)
    return allocation_plan
