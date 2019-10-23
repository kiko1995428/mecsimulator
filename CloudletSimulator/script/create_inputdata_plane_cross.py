# coding:utf-8
from simulator.utility.data import input_data_to_file
from simulator.dataset.cloudlets import *
from simulator.dataset.devices import *
from simulator import setting
import os.path

header = {}

# AllTimeCloudletsの生成
ans = input("Create AllTimeCloudlets with default settings?(y/n): ")
if ans == "y" or ans == "":
    x_length = setting.x_length
    y_length = setting.y_length
    t_length = setting.t_length
else:
    x_length = int(input("x_length: "))
    y_length = int(input("y_length: "))
    t_length = int(input("t_length: "))
header["x_length"] = x_length
header["y_length"] = y_length
header["t_length"] = t_length

ans = input("AllTimeCloudlets create algorithm(default={}): ".format(setting.default_all_time_cloudlets_create_algorithm))
if ans == "":
    ans = setting.default_all_time_cloudlets_create_algorithm
atcs_creater = ans
header["cloudlets_create_algorithm"] = atcs_creater

if ans == "plane":
    ans = input("Cloudlet resource(default={}): ".format(setting.default_use_resource_of_plane_cloudlets))
    if ans == "":
        c_resouce = setting.default_use_resource_of_plane_cloudlets
    else:
        c_resouce = int(ans)
    atcs = eval(atcs_creater)(t_length, x_length, y_length, c_resouce)
else:
    c_resouce = 1
    atcs = None
header["clodulets_resourde"] = c_resouce

# Devicesの生成
p_min = Point(0, 0)
p_max = Point(x_length - 1, y_length - 1)
ur_min = input("device minimum use resource(default=1): ")
if ur_min == "":
    ur_min = 1
else:
    ur_min = int(ur_min)
ur_max = input("device maximum use resource(default={}): ".format(c_resouce))
if ur_max == "":
    ur_max = c_resouce
else:
    ur_max = int(ur_max)
header["ur_min"] = ur_min
header["ur_max"] = ur_max

ans = input("Devices create algorithm(default={}): ".format(setting.default_device_create_algorithm))
if ans == "":
    ans = setting.default_device_create_algorithm
device_creater = ans
if ans == "cross":
    ans = input("road of number(default={}): ".format(6))
    if ans == "":
        r_num = 6
    else:
        r_num = int(ans)
    ans = input("density(default={}): ".format(1))
    if ans == "":
        density = 1
    else:
        density = int(ans)
    ans = input("unit per road(default={}): ".format(3))
    if ans == "":
        upr = 3
    else:
        upr = int(ans)
    ds = eval(device_creater)(p_min, p_max, int(t_length / 2), ur_min, ur_max, r_num=r_num, density=density, upr=upr)
    header["r_num"] = r_num
    header["density"] = density
    header["upr"] = upr
else:
    ds = eval(device_creater)(p_min, p_max, t_length, ur_min, ur_max)

# 説明文
ans = input("description:")

# データの書き出し
header["description"] = ans
header["devices_create_algorithm"] = device_creater
header["d_num"] = len(ds)
path = input_data_to_file(header, atcs, ds, "plane-cross")
print("outputed -> {}".format(path))

