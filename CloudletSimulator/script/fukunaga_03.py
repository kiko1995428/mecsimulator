from simulator.model.cloudlet import Cloudlet, create_all_time_cloudlets
from simulator.model.device import Device
from simulator.model.point import Point
from simulator.utility.point import route
from simulator.model.application import Application
from simulator.utility.data import input_data_to_file
from typing import List
import random

cloudlets_type = "plane"
d_random_num = 100
c_random_num = 5
c_sur = [1, 2, 3, 4, 5,6,7,8,9,10]
d_sur = [3, 8, 13, 7]
#1:5:9
#d_sur = [3, 5, 13, 7]
#1:2:3
ca_num = [0, 0, 0]
app1 = Application(name="1")
app2 = Application(name="2")
app3 = Application(name="3")
app4 = Application(name="4")
app5 = Application(name="5")
t_len = 30
x_len = 30
y_len = 30
app_name = [app1.name, app2.name, app3.name]
c_resource = 200
atcs = create_all_time_cloudlets(t_len, x_len, y_len, r=c_resource)
n1 = 0
i = 0
for x in range(x_len):
    for y in range(y_len):
        for t in range(t_len):

            #atcs[x][y][t].apps_append(app1)
            #i = random.randint(1, 3)
            #if i % 2 == 0:
            if i == 0:
            #n1 = random.randint(1, d_random_num)
            #if n1 % d_sur[0] == 0:
                atcs[x][y][t].apps_append(app1)
                atcs[x][y][t].apps_append(app2)
                ca_num[0] += 1
            #elif i % 3 == 0:
            #elif n1 % d_sur[1] == 0:
            if i == 1:
                atcs[x][y][t].apps_append(app2)
                atcs[x][y][t].apps_append(app3)
                ca_num[1] += 1
            if i == 2:
                atcs[x][y][t].apps_append(app1)
                atcs[x][y][t].apps_append(app3)
                ca_num[2] += 1
            #if i == 10:
            if i == 2:
                i = 0
            else:
                i += 1
            """
            #app 4
            elif n1 == c_sur[3]:
                atcs[x][y][t].apps_append(app1)
                atcs[x][y][t].apps_append(app4)
            elif n1 == c_sur[4]:
                atcs[x][y][t].apps_append(app2)
                atcs[x][y][t].apps_append(app4)
            elif n1 == c_sur[5]:
                atcs[x][y][t].apps_append(app3)
                atcs[x][y][t].apps_append(app4)
            #app5
            elif n1 == c_sur[6]:
                atcs[x][y][t].apps_append(app1)
                atcs[x][y][t].apps_append(app5)
            elif n1 == c_sur[7]:
                atcs[x][y][t].apps_append(app2)
                atcs[x][y][t].apps_append(app5)
            elif n1 == c_sur[8]:
                atcs[x][y][t].apps_append(app3)
                atcs[x][y][t].apps_append(app5)
            elif n1 == c_sur[9]:
                atcs[x][y][t].apps_append(app4)
                atcs[x][y][t].apps_append(app5)
             # atcs[x][y][t].apps_append(app1)
            """
            """
                #均等配置の場合
            if n1 == c_sur[0]:
                # n1 = random.randint(1, d_random_num)
                # if n1 % d_sur[0] == 0:
                atcs[x][y][t].apps_append(app1)
                atcs[x][y][t].apps_append(app2)
            elif n1 == c_sur[1]:
                # elif n1 % d_sur[1] == 0:
                atcs[x][y][t].apps_append(app2)
                atcs[x][y][t].apps_append(app3)
            elif n1 == c_sur[2]:
                atcs[x][y][t].apps_append(app1)
                atcs[x][y][t].apps_append(app3)
            # app 4
            elif n1 == c_sur[3]:
                atcs[x][y][t].apps_append(app1)
                atcs[x][y][t].apps_append(app4)
            elif n1 == c_sur[4]:
                atcs[x][y][t].apps_append(app2)
                atcs[x][y][t].apps_append(app4)
            elif n1 == c_sur[5]:
                atcs[x][y][t].apps_append(app3)
                atcs[x][y][t].apps_append(app4)
            # app5
            elif n1 == c_sur[6]:
                atcs[x][y][t].apps_append(app1)
                atcs[x][y][t].apps_append(app5)
            elif n1 == c_sur[7]:
                atcs[x][y][t].apps_append(app2)
                atcs[x][y][t].apps_append(app5)
            elif n1 == c_sur[8]:
                atcs[x][y][t].apps_append(app3)
                atcs[x][y][t].apps_append(app5)
            elif n1 == c_sur[9]:
                atcs[x][y][t].apps_append(app4)
                atcs[x][y][t].apps_append(app5)
            else :
                n1 = 0
            n1 += 1
            """

            """
            if i % 3 + 1 == c_sur[0]:
                atcs[x][y][t].apps_append(app1)
                atcs[x][y][t].apps_append(app2)
                ca_num[0] += 1
            elif i % 3 + 1 == c_sur[1]:
                atcs[x][y][t].apps_append(app2)
                atcs[x][y][t].apps_append(app3)
                ca_num[1] += 1
            elif i % 3 + 1 == c_sur[2]:
                # else :
                atcs[x][y][t].apps_append(app2)
                atcs[x][y][t].apps_append(app3)
                ca_num[2] += 1
            i += 1
            """
devices = []  # type:List[Device]
d_num = 0
da_num = [0, 0, 0, 0, 0]
#p1

setup_roads = [
#     # 混雑道路
    #(10, Point(0, 10), Point(x_len - 1, 10)),
    (13, Point(0, 13), Point(x_len - 1, 13)),
    (15, Point(0, 17), Point(x_len - 1, 15)),
    (17, Point(0, 19), Point(x_len - 1, 17)),
# #     #(20, Point(0, 20), Point(x_len - 1, 20)),
# #     #(40, Point(10, 0), Point(10, y_len - 1)),
    (43, Point(13, 0), Point(13, y_len - 1)),
    (45, Point(15, 0), Point(15, y_len - 1)),
    (47, Point(17, 0), Point(17, y_len - 1)),
    #(50, Point(20, 0), Point(20, y_len - 1)),
]

"""
#分散
setup_roads = [
#     # 混雑道路
    (13, Point(0, 0), Point(x_len - 1, y_len -1)),
    (15, Point(x_len-1, y_len-1), Point(0, 0)),
    (43, Point(0, y_len-1), Point(x_len-1, 0)),
    (45, Point(y_len-1, 0), Point(0, x_len-1)),
]
"""
min_road_device_num = 3
max_road_device_num = 9
min_use_resource = 1
max_use_resource = 5
app1 = Application(name="1", use_resource=3)#random.randint(min_use_resource, max_use_resource))
app2 = Application(name="2", use_resource=3)#random.randint(min_use_resource, max_use_resource))
app3 = Application(name="3", use_resource=3)#random.randint(min_use_resource, max_use_resource))
#app4 = Application(name="4", use_resource=3)#random.randint(min_use_resource, max_use_resource))
#app5 = Application(name="5", use_resource=3)#random.randint(min_use_resource, max_use_resource))
app_resourse = [app1.use_resource, app2.use_resource, app3.use_resource]
n = 90
dnum = 1
for road in setup_roads:
    road_num = road[0]
    side_a = road[1]
    side_b = road[2]
    for i in range(x_len):
        #n = random.randint(min_road_device_num, max_road_device_num)

        for j in range(n):
            d_name = "d{0}{1:05}".format(road_num, d_num)
            d = Device(name=d_name)
            d.startup_time = 0
            #偏り有り

            #n1 = random.randint(1, d_random_num)
            if dnum == 13:
                d.append_app(Application(name="1", use_resource=random.randint(min_use_resource, max_use_resource)))
                da_num[2] += 1
                dnum = 1
            elif dnum % 2 == 0:
                d.append_app(Application(name="2", use_resource=random.randint(min_use_resource, max_use_resource)))
                da_num[0] += 1
            else:
                d.append_app(Application(name="3", use_resource=random.randint(min_use_resource, max_use_resource)))
                da_num[1] += 1
            dnum += 1

            # 偏りなし ap
            """
            n1 = random.randint(1, 3)
            if n1 == c_sur[0]:
                d.append_app(app1)
                da_num[0] += 1
            elif n1 == c_sur[1]:
                d.append_app(app2)
                da_num[1] += 1
            elif n1 == c_sur[2]:
                d.append_app(app3)
                da_num[2] += 1
            """


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
dnum = 1
for t in range(t_len):
    for road in setup_roads:
        road_num = road[0]
        side_a = road[1]
        side_b = road[2]
        #n = random.randint(min_road_device_num, max_road_device_num)
        for i in range(n):
            d_name = "d{0}-{1:05}".format(road_num, d_num)
            d = Device(name=d_name)
            #偏り
            # n1 = random.randint(1, d_random_num)
            # if n1 % d_sur[0] == 0:
            #     d.append_app(Application(name="1", use_resource=random.randint(min_use_resource, max_use_resource)))
            #     da_num[2] += 1
            # elif n1 % d_sur[1] == 0:
            #     d.append_app(Application(name="2", use_resource=random.randint(min_use_resource, max_use_resource)))
            #     da_num[0] += 1
            # else:
            #     d.append_app(Application(name="3", use_resource=random.randint(min_use_resource, max_use_resource)))
            #     da_num[1] += 1
            if dnum == 13:
                d.append_app(Application(name="1", use_resource=random.randint(min_use_resource, max_use_resource)))
                da_num[2] += 1
                dnum = 1
            elif dnum % 2 == 0:
                d.append_app(Application(name="2", use_resource=random.randint(min_use_resource, max_use_resource)))
                da_num[0] += 1
            else:
                d.append_app(Application(name="3", use_resource=random.randint(min_use_resource, max_use_resource)))
                da_num[1] += 1
            dnum += 1
            """
            # 偏りなし ap3
            n1 = random.randint(1, 3)
            if n1 == c_sur[0]:
                d.append_app(app1)
                da_num[0] += 1
            elif n1 == c_sur[1]:
                d.append_app(app2)
                da_num[1] += 1
            elif n1 == c_sur[2]:
                d.append_app(app3)
                da_num[2] += 1
            """

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
print(da_num)
print(ca_num)
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
    "app_name": app_name,
    "app_resourse": app_resourse
}
random.shuffle(devices)
path = input_data_to_file(header, atcs, devices, "ieeei-d90")
print("outputed -> {}".format(path))

