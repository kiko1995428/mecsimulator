from simulator.oldmodels import Allocation, AllTimeCloudlets, Devices, AllocationPlan, Cloudlets
from simulator.oldutility import create_blank_allocation_plan, get_cloudlet_point_from_cloudlets
from simulator.utility.cloudlet import near_cloudlets
from simulator.utility.point import extract
from tqdm import tqdm
from typing import List
import random

def nearest(kwards) -> AllocationPlan:
    """
    最近傍割り当て方式
    もっとも近くにある割り当て可能なCloudletへ割り当てを行う
    :param all_time_cloudlets: 
    :param devices: 
    :return: 
    """
    all_time_cloudlets = kwards["atcs"]
    devices = kwards["ds"]
    allocation_plan = create_blank_allocation_plan(all_time_cloudlets, devices)
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

