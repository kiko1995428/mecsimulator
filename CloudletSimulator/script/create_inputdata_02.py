from simulator.model.cloudlet import Cloudlet, create_all_time_cloudlets
from simulator.model.device import Device
from simulator.model.point import Point
from simulator.utility.point import route
from simulator.utility.data import input_data_to_file
from simulator.model.application import *
from typing import List
import random

cloudlets_type = "plane"

t_len = 30
x_len = 30
y_len = 30
atcs = create_all_time_cloudlets(t_len, x_len, y_len, r=5)


devices = []  # type:List[Device]
d_num = 0

setup_roads = [
    # 混雑道路
    #(10, Point(0, 10), Point(x_len - 1, 10)),
    (13, Point(0, 13), Point(x_len - 1, 13)),
    (15, Point(0, 15), Point(x_len - 1, 15)),
    (17, Point(0, 17), Point(x_len - 1, 17)),
    #(20, Point(0, 20), Point(x_len - 1, 20)),
    #(40, Point(10, 0), Point(10, y_len - 1)),
    (43, Point(13, 0), Point(13, y_len - 1)),
    (45, Point(15, 0), Point(15, y_len - 1)),
    (47, Point(17, 0), Point(17, y_len - 1)),
    #(50, Point(20, 0), Point(20, y_len - 1)),
]

min_road_device_num = 3
max_road_device_num = 9
min_use_resource = 1
max_use_resource = 3
c_resource = 5

for road in setup_roads:
    road_num = road[0]
    side_a = road[1]
    side_b = road[2]
    for i in range(x_len):
        n = random.randint(min_road_device_num, max_road_device_num)
        for j in range(n):
            d_name = "d{0}{1:05}".format(road_num, d_num)
            d = Device(name=d_name)
            d.use_resource = random.randint(min_use_resource, max_use_resource)
            d.startup_time = 0
            if n == 0:
                app = Application(name="a1")
            elif n == 1:
                app = Application(name="a2")
            else:
                app = Application(name="a3")

            if random.randint(0, 3) == 0:
                # 別サイドをゴールにする
                roads = list(filter(lambda r: r[0] / 30 != road[0] / 30, setup_roads))
                r = roads[random.randint(0, len(roads) - 1)]
                goal = random.randint(1, 2)
                if random.randint(0, 1) == 0:
                    if road[0] < 30:
                        # 左右のルート
                        d.plan = route(Point(i, side_a.y), r[goal])
                    else:
                        # 上下のルート
                        d.plan = route(Point(side_a.x, i), r[goal])
                else:
                    if road[0] < 30:
                        # 左右のルート
                        d.plan = route(Point(x_len - 1 - i, side_a.y), r[goal])
                    else:
                        # 上下のルート
                        d.plan = route(Point(side_a.y, y_len - 1 - i), r[goal])
            else:
                if random.randint(0, 1) == 0:
                    # aからbへ
                    if road[0] < 30:
                        d.plan = route(Point(i, side_a.y), side_b)
                    else:
                        d.plan = route(Point(side_a.x, i), side_b)
                else:
                    # bからaへ
                    if road[0] < 30:
                        d.plan = route(Point(x_len - 1 - i, side_a.y), side_a)
                    else:
                        d.plan = route(Point(side_a.x, y_len - 1 - i), side_a)

            devices.append(d)
            d_num += 1

for t in range(t_len):
    for road in setup_roads:
        road_num = road[0]
        side_a = road[1]
        side_b = road[2]
        n = random.randint(min_road_device_num, max_road_device_num)
        for i in range(n):
            d_name = "d{0}-{1:05}".format(road_num, d_num)
            d = Device(name=d_name)
            d.use_resource = random.randint(min_use_resource, max_use_resource)
            d.startup_time = t
            if random.randint(0, 3) == 0:
                # 別混雑ルートへ切り替え
                roads = list(filter(lambda r: r != road, setup_roads))
                r = roads[random.randint(0, len(roads) - 1)]
                goal = random.randint(1, 2)
                if random.randint(0, 1) == 0:
                    d.plan = route(side_a, r[goal])
                else:
                    d.plan = route(side_b, r[goal])
            else:
                if random.randint(0, 1) == 0:
                    d.plan = route(side_a, side_b)
                else:
                    d.plan = route(side_b, side_a)
            devices.append(d)
            d_num += 1

header = {
    "device_num": d_num,
    "t_length": 30,
    "x_length": 30,
    "y_length": 30,
    "min_road_device_num": min_road_device_num,
    "max_road_device_num": max_road_device_num,
    "min_use_resource": min_use_resource,
    "max_use_resource": max_use_resource,
    "c_resource": c_resource,
}

path = input_data_to_file(header, atcs, devices, "inputdata_02")
print("outputed -> {}".format(path))

