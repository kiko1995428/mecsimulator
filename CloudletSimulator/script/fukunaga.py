from simulator.model.cloudlet import Cloudlet, create_all_time_cloudlets
from simulator.model.device import Device
from simulator.model.point import Point
from simulator.model.application import *
from simulator.utility.point import route
from simulator.utility.data import input_data_to_file
from typing import List
from simulator.model.point import Point3D
import random


t_len = 30
x_len = 30
y_len = 30

atcs = create_all_time_cloudlets(t_len, x_len, y_len)
"""
for x in range(x_len):
    for y in range(y_len):
        for t in range(t_len):
            n = random.randint(0, 2)
            if n == 0:
                #app = Application(name="a1")
            elif n == 1:
                #app = Application(name="a2")
            else:
                #app = Application(name="a3")
            #atcs[x][y][t].apps_append(app)
"""
devices = []  # type:List[Device]
d_num = 100
for i in range(d_num):
        d = Device(name="d{}".format(i))
        d.startup_time = 0
        n = random.randint(0, 3)
        if n == 0:
            d.plan = route(Point(0, 0), Point(x_len, y_len))
        if n == 1:
            d.plan = route(Point(x_len, y_len), Point(0, 0))
        if n == 2:
            d.plan = route(Point(0, y_len), Point(x_len, 0))
        if n == 3:
            d.plan = route(Point(y_len, 0), Point(0, x_len))
        n = random.randint(0, 2)
        if n == 0:
            #app = Application(name="a1")
            d.use_resource = 1
        elif n == 1:
            #app = Application(name="a2")
            d.use_resource = 1
        else:
            #app = Application(name="a3")
            d.use_resource = 1
        #d.append_app(app)
        devices.append(d)

header = {
        "device_num": d_num,
        "t_length": t_len,
        "x_length": x_len,
        "y_length": y_len,
}

path = input_data_to_file(header, atcs, devices, "fukunaga")
print("outputed -> {}".format(path))
