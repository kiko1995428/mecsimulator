#edege_serverのテスト用プログラム
#全体時間を考慮している

from CloudletSimulator.simulator.model.edge_server import MEC_server, between_time
from CloudletSimulator.simulator.model.device import Device
import pandas as pd
import pickle
import random
#SUMO全体の計算時間
system_end_time = 4736
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
    """
    mec[index].apps_append("AP1")
    mec[index].apps_append("AP2")
    mec[index].apps_append("AP3")

    """
    random_app = random.uniform(1, 3)
    if random_app == 1:
        mec[index].apps_append("AP1")
        mec[index].apps_append("AP2")
    elif random_app == 2:
        mec[index].apps_append("AP1")
        mec[index].apps_append("AP3")
    else:
        mec[index].apps_append("AP2")
        mec[index].apps_append("AP3")



#事前に作成しておいたバイナリデータからデバイスインスタンスを作成
devices = pickle.load(f)
#デバイスの総数
num = len(devices)
print(num)

for i in range(num):
    devices[i].startup_time = float(devices[i].plan[0].time)
    random_app = random.uniform(1,3)
    if random_app == 1:
        devices[i].apps = "AP1"
    elif random_app == 2:
        devices[i].apps = "AP2"
    else:
        devices[i].apps = "AP3"

app_resource = 1
same = None
#ここに全体時間の動きを考慮したプログラムを書く
#for i in range(num-1): #デバイスの数
for i in range(100):
    cnt = 0 #デバイスの計画表にある稼働時間をカウントするための変数
    plan_len = len(devices[i].plan)
    for j in range(system_end_time): #システムの秒数
        if cnt >= plan_len:
            break
        elif between_time(devices[i], j)==True :
            device_lon = float(devices[i].plan[cnt].x)
            device_lat = float(devices[i].plan[cnt].y)
            for index in range(data_length): #基地局数
                #print("ID:", mec[index].name, ",", "type:", mec[index].server_type, ",", "resource:",
                      #mec[index].resource)
                #print("lat:", mec[index].lat, ",", "lon:", mec[index].lon)
                #print("range:", mec[index].range, "m")
                #追加可能APを持っているか判定
                if(mec[index].is_operatable_application(devices[i]._apps) == True):
                    #リソース量をチェック
                    if mec[index].check_resource(app_resource)==True:
                        # ここで基地局のカバー範囲内にあるか判定する。
                        memo,device_flag = mec[index].cover_range_search(devices[i], cnt, app_resource)
                        #ここで基地局に割り振られたデバイスのインスタンスを各MECのhaving_devicesリストに追加していく。
                        if (device_flag == True) and (same != i):
                            #ここをセッターからセットできるようにする。
                            mec[index]._having_devices[j].append(devices[i].name)
                            same = i

                    #memoが0以外の時は、MECのid（name）が返ってくる
                        if memo > 0:
                            print("車両ID：", i, ", 時刻：", j, ", allocated MEC ID is ", memo)
                            memo = 0
                            break
            cnt = cnt + 1
"""
#MECサーバの毎秒ごとに持つデバイスの数とデバイスの名前を表示する。
for i in range(data_length):
    if len(mec[i]._having_devices[1]) != 0:
        print("MEC_ID:",i)
        print("len:", len(mec[i]._having_devices[1]), ", list:",mec[i]._having_devices[1])
        
for index in range(data_length): #基地局数
    print(mec[index].allocated_devices_count(MEC_resource, app_resource))

sum = 0
for index in range(data_length): #基地局数
    sum = sum + mec[index].traffic_congestion(devices, 400, app_resource)
    if mec[index].congestion_check(mec[index].traffic_congestion(devices, 400, app_resource)) == True:
        print("MEC_ID:", mec[index].name, ", traffic_congestion:",mec[index].traffic_congestion(devices, 400, app_resource) )
print(sum)
"""
