from simulator.model.device import Device, Devices
from simulator.model.point import Point
from simulator.utility.point import route
import random


def single_cross(p_min: Point, p_max: Point, t_max: int, ur_min: int=0, ur_max: int=3) -> Devices:
    ds = []
    for t in range(t_max + 1):
        num = t + 1
        if t > ur_max:
            num = ur_max
        for n in range(num):
            d1 = Device()
            p1_start = Point(int((p_max.x + p_min.x) / 2), 0)
            p1_goal = Point(int((p_max.x + p_min.x) / 2), p_max.y)
            d1.plan = route(p1_start, p1_goal)
            d1.use_resource = random.randint(ur_min, ur_max)
            d1.startup_time = t

            d2 = Device()
            p2_start = Point(0, int((p_min.y + p_max.y) / 2))
            p2_goal = Point(p_max.y, int((p_min.y + p_max.y) / 2))
            d2.plan = route(p2_start, p2_goal)
            d2.use_resource = random.randint(ur_min, ur_max)
            d2.startup_time = t
            ds.append(d1)
            ds.append(d2)
    return ds


def double_cross(p_min: Point, p_max: Point, t_max: int, ur_min: int=0, ur_max: int=3) -> Devices:
    ds = []
    for t in range(t_max + 1):
        num = t + 1
        if t > ur_max:
            num = ur_max
        for n in range(num):
            d1 = Device()
            p1_start = Point(int((p_max.x + p_min.x) / 3 * 1), 0)
            p1_goal = Point(int((p_max.x + p_min.x) / 3 * 1), p_max.y)
            d1.plan = route(p1_start, p1_goal)
            d1.use_resource = random.randint(ur_min, ur_max)
            d1.startup_time = t

            d2 = Device()
            p2_start = Point(0, int((p_min.y + p_max.y) / 2))
            p2_goal = Point(p_max.y, int((p_min.y + p_max.y) / 2))
            d2.plan = route(p2_start, p2_goal)
            d2.use_resource = random.randint(ur_min, ur_max)
            d2.startup_time = t

            d3 = Device()
            p3_start = Point(int((p_max.x + p_min.x) / 3 * 2), 0)
            p3_goal = Point(int((p_max.x + p_min.x) / 3 * 2), p_max.y)
            d3.plan = route(p3_start, p3_goal)
            d3.use_resource = random.randint(ur_min, ur_max)
            d3.startup_time = t

            ds.append(d1)
            ds.append(d2)
            ds.append(d3)
    return ds


def quatro_cross(p_min: Point, p_max: Point, t_max: int, ur_min: int=0, ur_max: int=3) -> Devices:
    ds = []
    for t in range(t_max + 1):
        num = t + 1
        if t > ur_max:
            num = ur_max
        for n in range(num):
            d1 = Device()
            p1_start = Point(int((p_max.x + p_min.x) / 3 * 1), 0)
            p1_goal = Point(int((p_max.x + p_min.x) / 3 * 1), p_max.y)
            d1.plan = route(p1_start, p1_goal)
            d1.use_resource = random.randint(ur_min, ur_max)
            d1.startup_time = t

            d2 = Device()
            p2_start = Point(0, int((p_min.y + p_max.y) / 3 * 1))
            p2_goal = Point(p_max.y, int((p_min.y + p_max.y) / 3 * 1))
            d2.plan = route(p2_start, p2_goal)
            d2.use_resource = random.randint(ur_min, ur_max)
            d2.startup_time = t

            d3 = Device()
            p3_start = Point(int((p_max.x + p_min.x) / 3 * 2), 0)
            p3_goal = Point(int((p_max.x + p_min.x) / 3 * 2), p_max.y)
            d3.plan = route(p3_start, p3_goal)
            d3.use_resource = random.randint(ur_min, ur_max)
            d3.startup_time = t

            d4 = Device()
            p4_start = Point(0, int((p_min.y + p_max.y) / 3 * 2))
            p4_goal = Point(p_max.y, int((p_min.y + p_max.y) / 3 * 2))
            d4.plan = route(p4_start, p4_goal)
            d4.use_resource = random.randint(ur_min, ur_max)
            d4.startup_time = t

            ds.append(d1)
            ds.append(d2)
            ds.append(d3)
            ds.append(d4)
    return ds


def cross(p_min: Point, p_max: Point, t_max: int, ur_min: int=0, ur_max: int=3,
          r_num: int=6, density: int=1, upr: int=3) -> Devices:
    """
    
    :param p_min: 
    :param p_max: 
    :param t_max: 
    :param ur_min: 
    :param ur_max: max of use resource
    :param r_num: number of road
    :param density: 集密度？
    :param upr: unit par roads
    :return: 
    """
    ds = []
    for t in range(t_max + 1):
        for i in range(int(r_num / 2)):
            offset = density
            div = int(r_num / 2) - 1 + (2 * density)
            for j in range(upr):
                d1 = Device()
                p1_start = Point(0, int((p_min.y + p_max.y) / div) * (offset + i))
                p1_goal = Point(p_max.x, int((p_min.y + p_max.y) / div) * (offset + i))
                d1.plan = route(p1_start, p1_goal)
                d1.use_resource = random.randint(ur_min, ur_max)
                d1.startup_time = t
                ds.append(d1)
            for j in range(upr):
                d2 = Device()
                p2_start = Point(int((p_min.x + p_max.x) / div) * (offset + i), 0)
                p2_goal = Point(int((p_min.x + p_max.x) / div) * (offset + i), p_max.y)
                d2.plan = route(p2_start, p2_goal)
                d2.use_resource = random.randint(ur_min, ur_max)
                d2.startup_time = t

                ds.append(d2)
    Device.num = 0
    random.shuffle(ds)
    return ds
