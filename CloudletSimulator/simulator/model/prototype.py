# プロトタイププログラム
# まず、make_binanary.pyでバイナリーファイルを作成し、このプログラムを実行する

from CloudletSimulator.simulator.model.edge_server import MEC_server, MEC_servers, check_between_time, check_plan_index, check_allocation, copy_to_mec
from CloudletSimulator.simulator.model.device import max_hop_search, min_hop_search, average_hop_calc,device_index_search, device_resource_calc
from CloudletSimulator.simulator.allocation.new_congestion import traffic_congestion, devices_congestion_sort, sorted_devices
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
for index, series in df.iterrows():
    mec[index] = MEC_server(MEC_resource, index + 1, server_type, series["lon"], series["lat"],
                            cover_range, system_end_time)
mec_num = len(mec)
device_flag = False
f = open('/Users/sugimurayuuki/Desktop/mecsimulator/CloudletSimulator/sumo/device.binaryfile', 'rb')
mec_num = len(df)
print("MECs", mec_num)

mec = [MEC_server(0, 00, " ", 00.00, 00.00, 0, 0)] * n
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
#print(num)

# 各デバイスの起動時間を設定する
for t in range(system_end_time):
    for i in range(100):
        sorted_devices[t][i].startup_time = int(sorted_devices[t][i].startup_time)

#save_devices = [] * data_length
# ---
# ここからメインの処理
for t in range(system_end_time):
    print("[TIME:", t, "]")
    # ある時刻tのMECに割り当てらえたデバイスを一時的に保存する用の変数
    save_devices = [None] * mec_num
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
                print("device:", sorted_devices[t][i].name, ", use_resource:", sorted_devices[t][i].use_resource, "--->", "MEC_ID:", mec[memo].name, ", index:", i)
                # print(sorted_devices[t][i].mec_name, mec[memo].resource)
                # print(memo, len(save_devices))
                # ---
                # なぜindexがmemoなの？ <- mec用のリストだから
                if save_devices[memo] == None:
                    save_devices[memo] = [sorted_devices[t][i].name]
                else:
                    save_devices[memo].append(sorted_devices[t][i].name)
                # ---
                #print(t, memo, index)
                memo = 0
            else:
                print("NOT FIND")
            # plan_indexをインクリメント
            sorted_devices[t][i]._plan_index = sorted_devices[t][i]._plan_index + 1
    # ある時刻tのMECに一時的に保存していた割り当てたデバイスをコピーする。
    copy_to_mec(mec, save_devices, t)

#-----
# リソース消費量がそれぞれで違う時のテスト用関数を作成する
# 各秒でMECが持っているデバイスのインデックスと数がわかるものとする

sum = 0
mec_sum = 0
having_device_resource_sum = 0
for t in range(system_end_time):
    #print("time:", t)
    for m in range(150):
        #if t == 16:
            #print("MEC_ID:", mec[m].name, ", having devices:", mec[m]._having_devices[t], mec[m]._having_devices_count[t],
                    #", mec_resouce:", mec[m]._resource_per_second[t], ", current time:", t)
            #sum = sum + mec[m]._having_devices_count[t]
        #mec_sum = mec_sum + mec[m]._resource_per_second[t]
        #sum = sum + mec[m]._having_devices_count[t]
        mec_sum = mec_sum + mec[m]._resource_per_second[t]
        if mec[m]._having_devices[t] is not None:
            #print("check", mec[m]._having_devices[t])
            device_index = device_index_search(sorted_devices[t], mec[m]._having_devices[t])
            #print(mec[m]._having_devices[t], device_index)
            having_device_resource_sum = having_device_resource_sum + device_resource_calc(sorted_devices[t], device_index)
    check_allocation(t, 150, 100, having_device_resource_sum, mec_sum)
    print((15000 - having_device_resource_sum), mec_sum)
    having_device_resource_sum = 0
    sum = 0
    mec_sum = 0
#print(sum, (150*100-sum), mec_sum)

sorted_devices = sorted_devices[0:100]
maximum, device_id = max_hop_search(sorted_devices[-1])
print("device_id:", device_id, ", max_hop:", maximum)
minimum, device_id = min_hop_search(sorted_devices[-1])
print("device_id:", device_id, ", min_hop:", minimum)
print("average_hop:", average_hop_calc(sorted_devices[-1]))

print()
print(1)

