"""
evaluation.py
coding          : utf-8
Author          : Kouhei Osaki
Created         : 2017/06/22
Last-Modified   : 2017/06/22
Version         : 1.0.0
Description     : リソース割り当ての結果から情報を抽出するモジュール
"""
from simulator.oldmodels import AllocationPlan, Point
import typing
from typing import Dict, List

def avg_hops(ap: AllocationPlan) -> typing.Dict[str, int]:
    """
    各端末の平均ホップ数を抽出する
    :param ap: 割り当て計画
    :return: 各端末の平均ホップ数
    """
    device_names = ap.keys()
    res = {}
    for name in device_names:
        allocated = filter(lambda a: a is not None and a.hop != -1, ap[name])
        sum_hop = 0
        count = 0
        for allocation in allocated:
            sum_hop += allocation.hop
            count += 1
        res[name] = sum_hop / count
    return res


def max_hops(ap: AllocationPlan, default: int=0) -> typing.Dict[str, int]:
    """
    各端末の最大ホップ数を抽出する
    :param ap: 割り当て計画
    :param default: 最大値のデフォルト値
    :return: 各端末の最大ホップ数
    """
    device_names = ap.keys()
    res = {}
    for name in device_names:
        allocated = filter(lambda a: a is not None and a.hop != -1, ap[name])
        max_h = default
        for allocation in allocated:
            max_h = max([max_h, allocation.hop])
        res[name] = max_h
    return res


def hops_each_device(ap: AllocationPlan, hop_max: int=1000) -> Dict[str, List[int]]:
    # Todo: テスト未作成, 途中でtimeとhopを間違えてる
    """
    デバイスごとの各ホップ数を表示する
    :param ap: 
    :param hop_max: 
    :return: 
    """
    d_names = ap.keys()
    res = {"hop_count": [i for i in range(hop_max + 1)]}
    for name in d_names:
        count = [0 for i in range(hop_max + 1)]
        for a in ap[name]:
            if a is not None and a.hop >= 0:
                count[a.hop] += 1
        res[name] = count

    h_sum = []
    for h_count in range(30):
        s = 0
        for k in ap.keys():
            for t in range(hop_max):
                p = ap[k][t]
                if p is not None and p.hop == h_count:
                    s += 1
        h_sum.append(s)
    res["sum"] = h_sum
    return res #各デバイスのhop回数がリストで返される



def hops_each_device_for_hot(ap: AllocationPlan, under: int, upper: int, p_min: Point, p_max: Point,
                             hop_max: int=1000) -> Dict[str, List[int]]:
    # Todo: テスト未作成, 途中でtimeとhopを間違えてる
    """
    高負荷時間のデバイスごとの各ホップ数を表示する
    :param ap: 
    :param hop_max: 
    :return: 
    """
    d_names = ap.keys()
    res = {"hop_count": [i for i in range(hop_max + 1)]}
    for name in d_names:
        count = [0 for i in range(hop_max + 1)]
        for t, a in enumerate(ap[name]):
            if not under <= t <= upper:
                continue
            if a is not None and a.hop >= 0:
                count[a.hop] += 1
        res[name] = count

    h_sum = []
    for h_count in range(30):
        s = 0
        for k in ap.keys():
            for t in range(hop_max):
                p = ap[k][t]
                if p is None:
                    continue
                if not under <= t <= upper and p_min.x <= p.x <= p_max.x and p_min.y <= p.y <= p_max.y:
                    continue
                if p.hop == h_count:
                    s += 1
        h_sum.append(s)
    res["sum"] = h_sum

    return res
