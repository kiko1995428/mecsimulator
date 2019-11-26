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
MEC_resource = 100
cover_range = 200
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
for t in range(20):
    print("[TIME:",t,"]")
    for i in range(10):
        print("---new device---",devices[i].name)
        if (check_plan_index(plan_index[i], moving_time[i]) == True):
            print("skip")
            continue
        if check_between_time(devices[i], t) == True:
            for index in range(100):
                #ここのアルゴリズムが間違っている
                if mec[index]._mode == "keep":
                    print(mec[index].name,devices[i].name)
                print("mode:", mec[index]._mode)
                if mec[index].check_resource(devices[i].use_resource) == True:
                    mec[index].mode_adjustment(devices[i], plan_index[i], t)
                    memo, device_flag = mec[index].cover_range_search(devices[i], plan_index[i], t)
                    if memo > 0 and device_flag == True:
                        memo = 0
                        #mec[m]._resouce_per_resouce[t] = mec[m].resource
                        mec[index]._resouce_per_resouce[t] = mec[index].resource
                        #print("---new device---")
                        break
                    #elif device_flag == False:
                        #if True == mec[index].custom_cover_range_search(devices[i],plan_index[t]):
                            #print("FIND")
                        #else:
                           #print("NOT")
                else:
                    mec[index]._resouce_per_resouce[t] = mec[index].resource
                    continue
            plan_index[i] = plan_index[i] + 1
    #この時点の各MECのリソース量を保存
    #for m in range(10):
        #mec[m]._resouce_per_resouce[t] = mec[m].resource

for t in range(20):
    print("time:", t)
    for m in range(100):
        if t==19:
            print("MEC_ID:",mec[m].name,", having devices:",mec[m]._having_devices_count[t],
                    ", mec_resouce:",mec[m]._resouce_per_resouce[t], ", current time:", t, ", test:", mec[m]._test)
print()
print("end")
