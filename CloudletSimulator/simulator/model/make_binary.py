# edege_serverのテスト用プログラム
# 全体時間を考慮している

from CloudletSimulator.simulator.model.edge_server import MEC_server
from CloudletSimulator.simulator.model.device import Device
from CloudletSimulator.simulator.allocation.new_congestion import all_traffic_congestion,traffic_congestion,create_congestion_list
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
MEC_resource = 200
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
f = open('/Users/sugimurayuuki/Desktop/mecsimulator/CloudletSimulator/dataset/device.binaryfile', 'rb')
# MECインスタンスをCSVを元に生成
data_length = len(df)
for index, series in df.iterrows():
    mec[index] = MEC_server(MEC_resource, index + 1, server_type, series["lon"], series["lat"],
                            cover_range, system_end_time)

# 事前に作成しておいたバイナリデータからデバイスインスタンスを作成
devices = pickle.load(f)
# デバイスの総数
num = len(devices)
for i in range(num):
    devices[i].startup_time = float(devices[i].plan[0].time)
same = None


for t in range(system_end_time):
    print(t)
    for m in range(data_length):
        create_congestion_list(mec[m], traffic_congestion(mec[m], devices, t), t)
f = open('mec.binaryfile', 'wb')
pickle.dump(mec, f)
f.close