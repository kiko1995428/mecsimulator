# edege_serverのテスト用プログラム
# 全体時間を考慮している

from CloudletSimulator.simulator.model.edge_server import MEC_server
from CloudletSimulator.simulator.model.device import Device
from CloudletSimulator.simulator.allocation.new_congestion import traffic_congestion
import pandas as pd
import pickle
import random

# SUMO全体の計算時間
#system_end_time = 4736
system_end_time = 100
# CSV読み込み
df = pd.read_csv("/Users/sugimurayuuki/Desktop/mecsimulator/CloudletSimulator/base_station/kddi_okayama_city.csv",
                 dtype={'lon': 'float', 'lat': 'float'})
# 基地局の種類を設定
server_type = "LTE"
# サーバの初期リソース量
MEC_resource = 100
# 基地局のカバー範囲を設定(メートル)
cover_range = 500
# CSVの行数を取得（基地局の数）
n = len(df)
print("Number of MEC server:", n)
# 基地局の数のオブジェクト用リストを作成
mec = [MEC_server(0, 00, " ", 00.00, 00.00, 0, 0)] * n

# テスト用デバイスデータ
device_flag = False
# バイナリデータを読み込み
d = open('/Users/sugimurayuuki/Desktop/mecsimulator/CloudletSimulator/dataset/device.binaryfile', 'rb')
devices = pickle.load(d)
num = len(devices)
for i in range(num):
    devices[i].startup_time = float(devices[i].plan[0].time) # 各デバイスの起動時間を設定する

# MECインスタンスをCSVを元に生成
data_length = len(df)
#data_length = 100
for index, series in df.iterrows():
    mec[index] = MEC_server(MEC_resource, index + 1, server_type, series["lon"], series["lat"],
                            cover_range, system_end_time)
# 時間をセット
for i in range(num):
    devices[i].startup_time = float(devices[i].plan[0].time) # 各デバイスの起動時間を設定する

# 事前に作成しておいたバイナリデータからデバイスインスタンスを作成
traffic_congestion(mec, devices, system_end_time)
f = open('congestion_sorted_devices.binaryfile', 'wb')
pickle.dump(devices, f)
f.close