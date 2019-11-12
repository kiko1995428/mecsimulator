#edege_serverのテスト用プログラム

from CloudletSimulator.simulator.model.edge_server import MEC_server, cover_range_search2
import pandas as pd
import pickle
#CSV読み込み
df = pd.read_csv("/Users/sugimurayuuki/Desktop/mecsimulator/CloudletSimulator/base_station/kddi_okayama_city.csv", dtype={'lon':'float','lat':'float'})
#基地局の種類を設定
server_type = "LTE"
#サーバの初期リソース量
resource = 1000
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
devices = pickle.load(f)
#適当にデバイス１つ目、時刻８の緯度経度を取得
device_lon = float(devices[0].plan[8].x) #文字列型であったので、floatに変換
device_lat = float(devices[0].plan[8].y)

#オブジェクト作成
for index, series in df.iterrows():
    mec[index] = MEC_server(resource, index+1, server_type, series["lon"], series["lat"], cover_range) #０からカウントのため、1を＋
    print("ID:", mec[index].name, ",", "type:", mec[index].server_type, ",", "resource:", mec[index].resource)
    print("lat:", mec[index].lat, ",", "lon:", mec[index].lon)
    print("range:", mec[index].range,"m")
    #ここで基地局のカバー範囲内にあるか判定する。
    device_flag, memo = cover_range_search2(device_flag, device_lon, device_lat, mec[index].lon, mec[index].lat, cover_range, index + 1)
    if memo > 0:
        tmp = memo
    print("**************")
print("correct ID is ", tmp)
