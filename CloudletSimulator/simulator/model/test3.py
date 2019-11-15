#edege_serverのテスト用プログラム
#全体時間を考慮している

from CloudletSimulator.simulator.model.edge_server import MEC_server, cover_range_search, allocated_devices_count, traffic_congestion
from CloudletSimulator.simulator.model.device import Device
import pandas as pd
import pickle

system_end_time = 4736 #SUMO全体の計算時間

#CSV読み込み
df = pd.read_csv("/Users/sugimurayuuki/Desktop/mecsimulator/CloudletSimulator/base_station/kddi_okayama_city.csv", dtype={'lon':'float','lat':'float'})
#基地局の種類を設定
server_type = "LTE"
#サーバの初期リソース量
MEC_resource = 200
#基地局のカバー範囲を設定(メートル)
cover_range = 500
#CSVの行数を取得（基地局の数）
n = len(df)
print("Number of MEC server:", n)
#基地局の数のオブジェクト用リストを作成
mec = [MEC_server(0,00, " ", 00.00, 00.00, 0, 0)] * n

#テスト用デバイスデータ
device_flag = False
#バイナリデータを読み込み
f = open('/Users/sugimurayuuki/Desktop/mecsimulator/CloudletSimulator/sumo/device.binaryfile', 'rb')
#MECインスタンスをCSVを元に生成
data_length = len(df)
for index, series in df.iterrows():
    mec[index] = MEC_server(MEC_resource, index + 1, server_type, series["lon"], series["lat"],
                            cover_range, system_end_time)
#事前に作成しておいたバイナリデータからデバイスインスタンスを作成
devices = pickle.load(f)
#デバイスの総数
num = len(devices)
print(num)

start_up_time =[0.0] * num
end_time = [0.0] * num
for i in range(num):
    #start_up_time[i] = float(devices[i].plan[0].time)
    devices[i].startup_time = float(devices[i].plan[0].time)
    #end_time[i] = float(devices[i].plan[-1].time)

app_resource = 1
same = None
#ここに全体時間の動きを考慮したプログラムを書く
#for i in range(num-1): #デバイスの数
for i in range(100):
    cnt = 0
    plan_len = len(devices[i].plan)
    for j in range(system_end_time): #システムの秒数
        if cnt >= plan_len:
            break
        elif (devices[i].startup_time >= j and j <= devices[i].shutdown_time):
            device_lon = float(devices[i].plan[cnt].x)
            device_lat = float(devices[i].plan[cnt].y)
            for index in range(data_length): #基地局数
                if (mec[index].resource - app_resource) >= 0:
                    # ここで基地局のカバー範囲内にあるか判定する。
                    memo, amount, judge = cover_range_search(device_flag, device_lon, device_lat, mec[index].lon,
                                                      mec[index].lat, cover_range, index+1, mec[index].resource,
                                                      app_resource)
                    #memo, amount = test(device_flag, devices, i , cnt, mec[index].lon, mec[index].lat,
                                        #cover_range, index+1, mec[index].resource, app_resource, j)
                    mec[index].resource = amount
                    #ここで基地局に割り振られたデバイスのインスタンスを各MECのhaving_devicesリストに追加していく。
                    if (judge == True) and (same != i):
                        #ここをセッターからセットできるようにする。
                        mec[index]._having_devices[j].append(devices[i].name)
                        same = i

                # memoが0以外の時は、MECのid（name）が返ってくる
                    if memo > 0:
                        tmp = memo
                        memo = 0
                        #print("車両ID：", i, ", 時刻：", j, ", allocated MEC ID is ", tmp)
                        break
            cnt = cnt + 1

#MECサーバの毎秒ごとに持つデバイスの数とデバイスの名前を表示する。
for i in range(data_length):
    if len(mec[i]._having_devices[1]) != 0:
        print("MEC_ID:",i)
        print("len:", len(mec[i]._having_devices[1]), ", list:",mec[i]._having_devices[1])
sum = 0
for index in range(data_length): #基地局数
    print("MEC_ID:", mec[index].name, ", traffic_congestion:", traffic_congestion(mec[index].lon, mec[index].lat, cover_range, num, devices, 400))
    sum = sum + traffic_congestion(mec[index].lon, mec[index].lat, cover_range, num, devices, 400)
print(sum)