"""
simulator/utility/device.py
coding          : utf-8
Author          : Kouhei Osaki
Created         : 2017/07/17
Last-Modified   : 2017/07/17
Version         : 1.0.0
Description     : Deviceに関する有用な関数などを定義している（適当
"""
from simulator.oldmodels import Point, Device, Devices
from simulator.utility.point import random_two_point, route
from tqdm import tqdm


def create_devices(p_min: Point, p_max: Point, t_max: int, npt: int, move: int):
    ds = []  # type: Devices
    for t in tqdm(range(t_max)):
        for n in range(npt):
            d = Device(startup_time=t)
            d.use_resource = 1
            start, goal = random_two_point(move, p_min, p_max)
            d.plan = route(start, goal)
            ds.append(d)
    return ds
