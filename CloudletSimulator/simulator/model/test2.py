# edege_serverのテスト用プログラム
# 全体時間を考慮している

from CloudletSimulator.simulator.model.edge_server import MEC_server, check_between_time, check_plan_index
from CloudletSimulator.simulator.model.device import Device
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
f = open('/Users/sugimurayuuki/Desktop/mecsimulator/CloudletSimulator/sumo/device.binaryfile', 'rb')
# MECインスタンスをCSVを元に生成
data_length = len(df)
for index, series in df.iterrows():
    mec[index] = MEC_server(MEC_resource, index + 1, server_type, series["lon"], series["lat"],
                            cover_range, system_end_time)

# バイナリデータを読み込み
f = open('/Users/sugimurayuuki/Desktop/mecsimulator/CloudletSimulator/dataset/device.binaryfile', 'rb')
m = open('/Users/sugimurayuuki/Desktop/mecsimulator/CloudletSimulator/simulator/model/mec.binaryfile', 'rb')
# 事前に作成しておいたバイナリデータからデバイスインスタンスを作成
devices = pickle.load(f)
#mec = pickle.load(m)
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

# ここに全体時間の動きを考慮したプログラムを書く
# システム時間
for t in range(system_end_time):  # システムの秒数
    print("【現在時刻:", t, "】")
    # デバイス
    for i in range(50):
        # 各デバイスのplanのindexが、デバイスの稼働時間を超えているか判定する。
        # 超えていれば新しいデバイスの処理に移る。
        if (check_plan_index(plan_index[i], moving_time[i]) == True) or (t > devices[i].shutdown_time):
            continue
        # 各デバイスのplanのindexが、デバイスの稼働時間内か判定する。
        elif check_between_time(devices[i], t) == True:
            # MECサーバ
            for index in range(data_length):
                mode = mec[index].mode_adjustment(devices[i], plan_index[t], mode, old_id, t)
                # print(mode)
                # if mec[index]._congestion_flag[t] == False:
                if True:
                    # リソース量をチェック
                    if mec[index].check_resource(devices[i].use_resource) == True:
                            # ここで基地局のカバー範囲内にあるか判定する。
                            memo, device_flag = mec[index].cover_range_search(devices[i], plan_index[t], mode)
                            # ここで基地局に割り振られたデバイスのインスタンスを各MECのhaving_devicesリストに追加していく。
                            if (device_flag == True) and (same != i):
                                # ここをセッターからセットできるようにする。
                                mec[index]._having_devices[t].append(devices[i].name)
                                #devices[i].mec_name = (t, mec[index].name)
                                same = i
                            # memoが0以外の時は、MECのid（name）が返ってくる
                            if memo > 0:
                                print("車両ID:", i, ", 時刻:", t, ", 割り当てたMEC_ID:", memo)
                                print("MECのリソース量:", mec[index].resource,
                                      ", 割り当てたデバイスの数:",
                                      int(mec[index].allocated_devices_count(MEC_resource, 1)))
                                print("---")
                                old_id = memo
                                memo = 0
                                break
        plan_index[i] = plan_index[i] + 1
print()
#for t in range(system_end_time):
    #for index in range(data_length):
        #print("MEC:", mec[index].name, ", current time:", t, mec[index]._test)
        #print("Number of having devices:", len(mec[index]._having_devices[t]), ", MEC_resource", mec[index].resource)
