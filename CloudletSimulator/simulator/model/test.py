#edege_serverのテスト用プログラム

from CloudletSimulator.simulator.model.edge_server import MEC_server, old_cover_range_search, allocated_devices_count
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
mec = [MEC_server(0,00, " ", 00.00, 00.00, 0,0)] * n
system_end_time = 4736

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
for i in range(num-1):
    device_lon = float(devices[i].plan[1].x)
    device_lat = float(devices[i].plan[1].y)
    app_resource = 1
    for index in range(data_length):
        #print("ID:", mec[index].name, ",", "type:", mec[index].server_type, ",", "resource:", mec[index].resource)
        #print("lat:", mec[index].lat, ",", "lon:", mec[index].lon)
        #print("range:", mec[index].range, "m")
        #混雑判定
        if (mec[index].resource - app_resource)>=0:
            #ここで基地局のカバー範囲内にあるか判定する。
            memo, amount, device_flag = old_cover_range_search(device_flag, device_lon, device_lat, mec[index].lon, mec[index].lat,
                                    cover_range, index+1, mec[index].resource, app_resource)
            mec[index].resource = amount
        #memoが0以外の時は、MECのid（name）が返ってくる
        if memo > 0:
            tmp = memo
            memo = 0
            break
    #print("車両ID：", i, ",", "allocated MEC ID is ", tmp)

#print("********")
sum=0
#格MECサーバの割り当てたデバイス数を表示する処理
for i in range(data_length):
    cnt = allocated_devices_count(MEC_resource, mec[i].resource, app_resource)
    print("MEC_ID:", mec[i].name, ", resource:", mec[i].resource, ", allocated_devices_count(MEC):", int(cnt))
    sum = sum + cnt
print("number of allocated total devices:", int(sum))