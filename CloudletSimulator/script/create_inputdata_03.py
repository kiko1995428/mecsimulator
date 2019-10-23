"""
超低負荷入力データ生成
"""

from simulator.model.cloudlet import Cloudlet, create_all_time_cloudlets
from simulator.model.device import Device
from simulator.model.point import Point
from simulator.utility.point import route
from simulator.utility.data import input_data_to_file
from typing import List
import random

cloudlets_type = "plane"

t_len = 30
x_len = 30
y_len = 30
atcs = create_all_time_cloudlets(t_len, x_len, y_len)


devices = []  # type:List[Device]
d_num = 0

setup_roads = [
    # 混雑道路
    (10, Point(0, 10), Point(x_len - 1, 10)),
    (13, Point(0, 13), Point(x_len - 1, 13)),
    (15, Point(0, 15), Point(x_len - 1, 15)),
    (17, Point(0, 17), Point(x_len - 1, 17)),
    (20, Point(0, 20), Point(x_len - 1, 20)),
    (40, Point(10, 0), Point(10, y_len - 1)),
    (43, Point(13, 0), Point(13, y_len - 1)),
    (45, Point(15, 0), Point(15, y_len - 1)),
    (47, Point(17, 0), Point(17, y_len - 1)),
    (50, Point(20, 0), Point(20, y_len - 1)),
]

min_road_device_num = 1
max_road_device_num = 1
min_use_resource = 1
max_use_resource = 1

for road in setup_roads:
    road_num = road[0]
    left_side = road[1]
    right_side = road[2]
    for i in range(x_len):
        n = random.randint(min_road_device_num, max_road_device_num)
        for j in range(n):
            d_name = "d{0}{1:05}".format(road_num, d_num)
            d = Device(name=d_name)
            d.use_resource = random.randint(min_use_resource, max_use_resource)
            d.startup_time = 0
            if random.randint(0, 3) == 0:
                roads = list(filter(lambda r: r != road, setup_roads))
                r = roads[random.randint(0, len(roads) - 1)]
                if random.randint(0, 1) == 0:
                    if road[0] < 30:
                        d.plan = route(Point(i, left_side.y), r[1])
                    else:
                        d.plan = route(Point(left_side.x, i), r[1])
                else:
                    if road[0] < 30:
                        d.plan = route(Point(x_len - 1 - i, left_side.y), r[1])
                    else:
                        d.plan = route(Point(left_side.y, y_len - 1- i), r[1])
            else:
                if random.randint(0, 1) == 0:
                    if road[0] < 30:
                        d.plan = route(Point(i, left_side.y), right_side)
                    else:
                        d.plan = route(Point(left_side.x, i), right_side)
                else:
                    if road[0] < 30:
                        d.plan = route(Point(x_len - 1 - i, left_side.y), left_side)
                    else:
                        d.plan = route(Point(left_side.x, y_len - 1 - i), left_side)

            devices.append(d)
            d_num += 1

for t in range(t_len):
    for road in setup_roads:
        road_num = road[0]
        left_side = road[1]
        right_side = road[2]
        n = random.randint(min_road_device_num, max_road_device_num)
        for i in range(n):
            d_name = "d{0}-{1:05}".format(road_num, d_num)
            d = Device(name=d_name)
            d.use_resource = random.randint(min_use_resource, max_use_resource)
            d.startup_time = t
            if random.randint(0, 3) == 0:
                roads = list(filter(lambda r: r != road, setup_roads))
                r = roads[random.randint(0, len(roads) - 1)]
                if random.randint(0, 1) == 0:
                    d.plan = route(left_side, r[1])
                else:
                    d.plan = route(right_side, r[1])
            else:
                if random.randint(0, 1) == 0:
                    d.plan = route(left_side, right_side)
                else:
                    d.plan = route(right_side, left_side)
            devices.append(d)
            d_num += 1

header = {
    "device_num": d_num,
    "t_length": 30,
    "x_length": 30,
    "y_length": 30,
    "c_max_resource": 5,
    "max_road_device_num": 6
}

path = input_data_to_file(header, atcs, devices, "inputdata_03")
print("outputed -> {}".format(path))

