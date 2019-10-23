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
