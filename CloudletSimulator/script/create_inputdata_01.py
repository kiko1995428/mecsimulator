from simulator.model.cloudlet import Cloudlet, create_all_time_cloudlets
from simulator.model.device import Device
from simulator.model.point import Point
from simulator.utility.point import route
from typing import List
import random

cloudlets_type = "plane"

t_len = 10
x_len = 30
y_len = 30
atcs = create_all_time_cloudlets(t_len, x_len, y_len)


devices = []  # type:List[Device]

# device name is 10000 - 10999[
r_num = 10
r_pos = Point(10, 0)
d_num = 0
for i in range(x_len):
    n = random.randint(5)
    for j in range(n):
        d = Device(name="d10{0:03}".format(d_num))
        d.use_resource = random.randint(3)
        d.startup_time = 0
        d.plan = route(Point(r_pos.x + i, r_pos.y), Point(x_len - 1, r_pos.y))
        devices.append(d)
        d_num += 1
for t in range(t_len):
    n = random.randint(5)
    for i in range(n):
        d = Device(name="d10{0:03}".format(d_num))
        d.use_resource = random.randint(3)
        d.startup_time = 0
        d.plan = route(r_pos, Point(x_len - 1, r_pos.y))
        d_num += 1

# device name is
