# プロトタイププログラム
# まず、make_binanary.pyでバイナリーファイルを作成し、このプログラムを実行する

from CloudletSimulator.simulator.model.edge_server import MEC_server, check_between_time, check_plan_index
from CloudletSimulator.simulator.model.device import Device, max_hop_search, min_hop_search
from CloudletSimulator.simulator.allocation.new_congestion import traffic_congestion, devices_congestion_sort, sorted_devices
import pandas as pd
import pickle
import random
import numpy as np
from CloudletSimulator.simulator.allocation.new_nearest import nearest_search


system_end_time = 200
df = pd.read_csv("/Users/sugimurayuuki/Desktop/mecsimulator/CloudletSimulator/base_station/kddi_okayama_city.csv",
                 dtype={'lon': 'float', 'lat': 'float'})
server_type = "LTE"
MEC_resource = 100
cover_range = 500
n = len(df)
print("Number of MEC server:", n)
mec = [MEC_server(0, 00, " ", 00.00, 00.00, 0, 0)] * n
device_flag = False
f = open('/Users/sugimurayuuki/Desktop/mecsimulator/CloudletSimulator/sumo/device.binaryfile', 'rb')
data_length = len(df)
print("MECs", data_length)
for index, series in df.iterrows():
    mec[index] = MEC_server(MEC_resource, index + 1, server_type, series["lon"], series["lat"],
                            cover_range, system_end_time)

d = open('/Users/sugimurayuuki/Desktop/mecsimulator/CloudletSimulator/dataset/device.binaryfile', 'rb')
cd = open('congestion_checked_devices.binaryfile', 'rb')
#sd = open('congestion_sorted_devices.binaryfile', 'rb')
devices = pickle.load(d)

cd = pickle.load(cd)
# 混雑度順で毎秒ごとのdevicesをソートする
sorted_devices = devices_congestion_sort(cd, system_end_time)
#sorted_devices = pickle.load(sd)
# デバイスの総数
num = len(devices)
#num = 200
print(num)

# 各デバイスの起動時間を設定する
for t in range(system_end_time):
    for i in range(100):
        sorted_devices[t][i].startup_time = int(sorted_devices[t][i].startup_time)
# ---
# ここからメインの処理
for t in range(200):
    print("[TIME:", t, "]")
    for i in range(100):
        print("---new device---", sorted_devices[t][i].name)
        # plan_indexがデバイスの稼働時間外なら処理をスキップ
        if (check_plan_index(sorted_devices[t][i].plan_index, len(sorted_devices[t][i].plan)) == False):
            print("skip")
            continue
        # plan_indexが稼働時間内なら処理開始
        if check_between_time(sorted_devices[t][i], t) == True:
            print(sorted_devices[t][i].plan_index)
            # 最近傍割り当て処理
            device_flag, memo = nearest_search(sorted_devices[t][i], mec, sorted_devices[t][i].plan_index, cover_range, t)
            # 最近傍割り当てが成功したら表示する
            if device_flag == True and memo != 0:
            #if device_flag == True:
                mec[memo].save_resource(t)
                print("device:", sorted_devices[t][i].name, "--->", "MEC_ID:", mec[memo].name, ", index:", i)
                print(sorted_devices[t][i].mec_name, mec[memo].resource)
                mec[memo].save_resource(t)
                #print(t, memo, index)
                memo = 0
            else:
                print("NOT FIND")
            # plan_indexをインクリメント
            sorted_devices[t][i]._plan_index = sorted_devices[t][i]._plan_index + 1

#テスト用関数
def check_simulation(time, mec_num, mec_resource, having_device_resouce_sum, mec_resource_sum):
    original_resource = mec_resource * mec_num
    numerical_goal = original_resource - having_device_resouce_sum
    if numerical_goal == mec_resource_sum:
        print("time:",time, " correct")
    else:
        print("time:", time, " error")
#-----
#テストコード
sum = 0
mec_sum = 0
for t in range(200):
    #print("time:", t)
    for m in range(150):
        #if t == 380:
            #print("MEC_ID:", mec[m].name, ", having devices:", mec[m]._having_devices_count[t],
                    #", mec_resouce:", mec[m]._resource_per_second[t], ", current time:", t)
            #sum = sum + mec[m]._having_devices_count[t]
            #mec_sum = mec_sum + mec[m]._resource_per_second[t]
        sum = sum + mec[m]._having_devices_count[t]
        mec_sum = mec_sum + mec[m]._resource_per_second[t]
    check_simulation(t, 150, 100, sum, mec_sum)
    sum = 0
    mec_sum = 0
print(sum, (150*100-sum), mec_sum)
sorted_devices = sorted_devices[0:199]
maximum, device_id = max_hop_search(sorted_devices[-1])
print("device_id:", device_id, ", max_hop:", maximum)
minimum, device_id = min_hop_search(sorted_devices[-1])
print("device_id:", device_id, ", min_hop:", minimum)


print()
print(1)

