from CloudletSimulator.simulator.model.edge_server import MEC_server
from CloudletSimulator.simulator.model.device import Device
from CloudletSimulator.simulator.allocation.new_congestion import traffic_congestion
from CloudletSimulator.dataset.delete_MEC import delete_mec
from CloudletSimulator.simulator.model.point import Point3D
import pandas as pd
import pickle
import random
import copy



# テスト用デバイスデータ
device_flag = False
# バイナリデータを読み込み
d = open('/Users/sugimurayuuki/Desktop/mecsimulator/CloudletSimulator/dataset/device.congestion_binaryfile_500', 'rb')
devices = pickle.load(d)
device_num = len(devices)
print("デバイスのMAX数", len(devices))
device = devices[0:1]
num = len(devices)
new_devices = None
new_device = copy.deepcopy(device[0])
for n in range(2000):
    device[0].name = n
    if new_devices is None:
        new_devices = [copy.deepcopy(device[0])]
    else:
        new_devices.append(copy.deepcopy(device[0]))

plan_num = len(new_devices[0].plan)
num = len(new_devices)
for d in range(num):
    random_value = random.randint(1, 100)
    new_plan = None
    for p in range(plan_num):
        # こいつが悪さをしてる
        pivot_time = float(new_devices[d].plan[p].time)
        if new_plan is None:
            new_plan = [Point3D(new_devices[d].plan[p].x, new_devices[d].plan[p].y, str(pivot_time + random_value))]
        else:
            new_plan.append(Point3D(new_devices[d].plan[p].x, new_devices[d].plan[p].y, str(pivot_time + random_value)))
    new_devices[d].plan = new_plan

#221秒間ある
f = open('/Users/sugimurayuuki/Desktop/mecsimulator/CloudletSimulator/dataset/device.clone_binaryfile', 'wb')
pickle.dump(new_devices, f)
