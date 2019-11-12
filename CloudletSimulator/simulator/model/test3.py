#edege_serverのテスト用プログラム
#全体時間を考慮している

from CloudletSimulator.simulator.model.edge_server import MEC_server, cover_range_search, allocated_devices_count
import pandas as pd
import pickle

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
mec = [MEC_server(0,00, " ", 00.00, 00.00, 0)] * n

#テスト用デバイスデータ
device_flag = False
#バイナリデータを読み込み
f = open('/Users/sugimurayuuki/Desktop/mecsimulator/CloudletSimulator/sumo/device.binaryfile', 'rb')
#MECインスタンスをCSVを元に生成
data_length = len(df)
for index, series in df.iterrows():
    mec[index] = MEC_server(MEC_resource, index + 1, server_type, series["lon"], series["lat"],
                            cover_range)
#事前に作成しておいたバイナリデータからデバイスインスタンスを作成
devices = pickle.load(f)
#デバイスの総数
num = len(devices)
print(num)

system_end_time = 4736
start_up_time =[0.0] * num
end_time = [0.0] * num
for i in range(num-1):
    start_up_time[i] = float(devices[i].plan[0].time)
    end_time[i] =float(devices[i].plan[-1].time)

app_resource = 1
#ここに全体時間の動きを考慮したプログラムを書く
for i in range(num-1): #デバイスの数
    for j in range(system_end_time): #システムの秒数
        if (start_up_time[i] >= j) and (j <= end_time[i]):
            plan_len=len(devices[i].plan)
            for n in range(plan_len): #予定表のインデックス
                if float(devices[i].plan[n].time) == float(j):
                    device_lon = float(devices[i].plan[n].x)
                    device_lat = float(devices[i].plan[n].y)
            #device_lon = float(devices[i].plan[].x)
            #device_lat = float(devices[i].plan[].y)
                    for index in range(data_length-200): #基地局数
                        if (mec[index].resource - app_resource) >= 0:
                            # ここで基地局のカバー範囲内にあるか判定する。
                            memo, amount = cover_range_search(device_flag, device_lon, device_lat, mec[index].lon,
                                                              mec[index].lat,
                                                              cover_range, index + 1, mec[index].resource, app_resource)
                            mec[index].resource = amount
                        # memoが0以外の時は、MECのid（name）が返ってくる
                        if memo > 0:
                            tmp = memo
                            memo = 0
                            break


sum=0
#格MECサーバの割り当てたデバイス数を表示する処理
for i in range(data_length):
    cnt = allocated_devices_count(MEC_resource, mec[i].resource, app_resource)
    #print("MEC_ID:", mec[i].name, ", resource:", mec[i].resource, ", allocated_devices_count(MEC):", int(cnt))
    sum = sum + cnt
print("number of allocated total devices:", int(sum))