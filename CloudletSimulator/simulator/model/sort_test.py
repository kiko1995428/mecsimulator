# edege_serverのテスト用プログラム
# 全体時間を考慮している

from CloudletSimulator.simulator.model.edge_server import MEC_server
from CloudletSimulator.simulator.model.device import Device
from CloudletSimulator.simulator.allocation.new_congestion import traffic_congestion, devices_congestion_sort, sorted_devices
import pandas as pd
import pickle
import random
import random

# SUMO全体の計算時間
#system_end_time = 4736
system_end_time = 100


# バイナリデータを読み込み
d = open('congestion_sorted_devices.binaryfile', 'rb')
devices = pickle.load(d)
num = len(devices)
for t in range(system_end_time):
    for d in range(num):
        devices[d]._congestion_status[t] = random.randint(1, 20)

#ソートができているかわからない
#テストが必要
sorted_devices = devices_congestion_sort(devices, system_end_time)

f = open('congestion_sorted_devices.binaryfile', 'wb')
pickle.dump(devices, f)
f.close