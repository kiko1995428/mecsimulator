import collections
from typing import List, Dict

from simulator.model.cloudlet import AllTimeCloudlets
from simulator.model.device import Devices

"""
割り当て計画の定義
型アノテーション用だが現状意味はない(2017/06/14)
"""
Allocation = collections.namedtuple('Allocation', ('x', 'y', 'hop'))
AllocationPlan = Dict["str", List[Allocation]]


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
