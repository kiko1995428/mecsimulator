# edege_serverのテスト用プログラム
# 全体時間を考慮している

from CloudletSimulator.simulator.model.edge_server import MEC_server, check_between_time, check_plan_index
from CloudletSimulator.simulator.model.device import Device
import pandas as pd
import pickle
import random
import numpy as np
from CloudletSimulator.simulator.allocation.new_nearest import nearest_search


system_end_time = 100
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
sd = open('congestion_sorted_devices.binaryfile', 'rb')
devices = pickle.load(d)
sorted_devices = pickle.load(sd)

num = len(devices) # デバイスの総数
print(num)
moving_time = [0] * num
plan_index = [0] * num # 各deviceのplanリストのindex用リスト
for t in range(system_end_time):
    for i in range(100):
        sorted_devices[t][i].startup_time = int(sorted_devices[t][i].startup_time) # 各デバイスの起動時間を設定する

same = None # 割り当てに被りがないように直前に割り当てたMECのIDを保存する変数
mode = "add" # リソースの割り当て状態、初期状態はadd
old_id = None # t-1秒前のMECのIDを保存するための変数
nearest_range = 250
cnt =[0]*100
for t in range(100):
    print("[TIME:", t, "]")
    for i in range(100):
        print("---new device---", sorted_devices[t][i].name)
        # ここで判定漏れがある
        if (check_plan_index(sorted_devices[t][i].plan_index, len(sorted_devices[t][i].plan)) == False):
            print("skip")
            continue
        if check_between_time(sorted_devices[t][i], t) == True:
            print(sorted_devices[t][i].plan_index)
            device_flag, memo = nearest_search(sorted_devices[t][i], mec, sorted_devices[t][i].plan_index, cover_range, t)
            if device_flag == True and memo != 0:
            #if device_flag == True:
                mec[memo].save_resource(t)
                print("device:", sorted_devices[t][i].name, "--->", "MEC_ID:", mec[memo].name, ", index:", i)
                print(sorted_devices[t][i].mec_name, mec[memo].resource)
                cnt[t] = cnt[t]+1
                mec[memo].save_resource(t)
                #print(t, memo, index)
                memo = 0
            else:
                print("NOT FIND")
            print()
            sorted_devices[t][i]._plan_index = sorted_devices[t][i]._plan_index + 1

def check_simulation(time, mec_num, mec_resource, having_device_resouce_sum, mec_resource_sum):
    original_resource = mec_resource * mec_num
    numerical_goal = original_resource - having_device_resouce_sum
    if numerical_goal == mec_resource_sum:
        print("time:",time, " correct")
    else:
        print("time:", time, " error")

sum = 0
mec_sum = 0
for t in range(100):
    #print("time:", t)
    for m in range(103):
        #if t == 95:
            #print("MEC_ID:", mec[m].name, ", having devices:", mec[m]._having_devices_count[t],
                    #", mec_resouce:", mec[m]._resource_per_second[t], ", current time:", t)
            #sum = sum + mec[m]._having_devices_count[t]
            #mec_sum = mec_sum + mec[m]._resource_per_second[t]
        sum = sum + mec[m]._having_devices_count[t]
        mec_sum = mec_sum + mec[m]._resource_per_second[t]
    check_simulation(t, 103, 100, sum, mec_sum)
    sum = 0
    mec_sum = 0
print(sum, (103*100-sum), mec_sum)
print()
print(1)

