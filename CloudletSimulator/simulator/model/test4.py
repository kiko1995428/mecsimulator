# edege_serverのテスト用プログラム
# 全体時間を考慮している

from CloudletSimulator.simulator.model.edge_server import MEC_server, check_between_time, check_plan_index
from CloudletSimulator.simulator.model.device import Device
import pandas as pd
import pickle
import random
import numpy as np

system_end_time = 100
df = pd.read_csv("/Users/sugimurayuuki/Desktop/mecsimulator/CloudletSimulator/base_station/kddi_okayama_city.csv",
                 dtype={'lon': 'float', 'lat': 'float'})
server_type = "LTE"
MEC_resource = 200
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
f = open('/Users/sugimurayuuki/Desktop/mecsimulator/CloudletSimulator/dataset/device.binaryfile', 'rb')
devices = pickle.load(f)
num = len(devices) # デバイスの総数
print(num)
moving_time = [0] * num
plan_index = [0] * num # 各deviceのplanリストのindex用リスト
for i in range(num):
    devices[i].startup_time = float(devices[i].plan[0].time) # 各デバイスの起動時間を設定する
    moving_time[i] = len(devices[i].plan) # 各デバイスのplanの長さ（稼働時間）をリストに格納する
same = None # 割り当てに被りがないように直前に割り当てたMECのIDを保存する変数
mode = "add" # リソースの割り当て状態、初期状態はadd
old_id = None # t-1秒前のMECのIDを保存するための変数


for t in range(20):  # システムの秒数
    #print("【現在時刻:", t, "】")
    for i in range(3):
        if (check_plan_index(plan_index[i], moving_time[i]) == True):
            print("skip")
            continue
        elif check_between_time(devices[i], t) == True:
            for index in range(data_length):
                if mec[index].check_resource(devices[i].use_resource) == True:
                    mec[index].mode_adjustment(devices[i], plan_index[t], old_id, t)
                    memo, device_flag = mec[index].cover_range_search(devices[i], plan_index[t], t)
                else:
                    continue
            plan_index[i] = plan_index[i] + 1

for m in range(data_length):
    for t in range(20):
        if  mec[m]._having_devices_count[t] > 0:
             print("MEC_ID:",mec[m].name,", having devices:",mec[m]._having_devices_count[t],
                    ", mec_resouce:",mec[m]._resource, ", current time:", t, ", test:", mec[m]._test)
print()
print("end")
