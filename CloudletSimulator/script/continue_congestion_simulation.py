

from CloudletSimulator.simulator.model.edge_server import MEC_server, MEC_servers, check_between_time, check_plan_index, check_allocation, copy_to_mec, application_reboot_rate
from CloudletSimulator.simulator.model.device import max_hop_search, min_hop_search, average_hop_calc,device_index_search, device_resource_calc
from CloudletSimulator.simulator.allocation.new_congestion import traffic_congestion, devices_congestion_sort
from CloudletSimulator.simulator.allocation.new_continue import continue_search
from CloudletSimulator.simulator.convenient_function.write_csv import write_csv
from CloudletSimulator.simulator.allocation.new_nearest import nearest_search
import pandas as pd
import pickle

def continue_congestion_simulation(system_end_time, device_num, continue_distance,  path_w):
    df = pd.read_csv("/Users/sugimurayuuki/Desktop/mecsimulator/CloudletSimulator/base_station/kddi_okayama_city.csv",
                     dtype={'lon': 'float', 'lat': 'float'})
    server_type = "LTE"
    MEC_resource = 100
    cover_range = 500
    n = len(df)
    print("Number of MEC server:", n)
    mec = [MEC_server(0, 00, " ", 00.00, 00.00, 0, 0)] * n
    for index, series in df.iterrows():
        mec[index] = MEC_server(MEC_resource, index + 1, server_type, series["lon"], series["lat"],
                                cover_range, system_end_time)
    mec_num = len(mec)
    device_flag = False
    f = open('/Users/sugimurayuuki/Desktop/mecsimulator/CloudletSimulator/sumo/device.binaryfile', 'rb')
    mec_num = len(df)
    print("MECs", mec_num)
    mec = [MEC_server(0, 00, " ", 00.00, 00.00, 0, 0)] * n
    for index, series in df.iterrows():
        mec[index] = MEC_server(MEC_resource, index + 1, server_type, series["lon"], series["lat"],
                                cover_range, system_end_time)
    # ---
    # デバイスの準備
    d = open('/Users/sugimurayuuki/Desktop/mecsimulator/CloudletSimulator/dataset/device.binaryfile', 'rb')
    devices = pickle.load(d)
    devices = devices[0:device_num]
    num = len(devices)
    print("device_num", num)
    for i in range(num):
        devices[i].startup_time = float(devices[i].plan[0].time)  # 各デバイスの起動時間を設定する
        devices[i].set_congestion_status(system_end_time)

    # 混雑度計算
    traffic_congestion(mec, devices, system_end_time)
    # 混雑度順で毎秒ごとのdevicesをソートする
    sorted_devices = devices_congestion_sort(devices, system_end_time)
    # sorted_devices = pickle.load(sd)


    # 各デバイスの起動時間を設定する
    for t in range(system_end_time):
        for i in range(num):
            sorted_devices[t][i].startup_time = int(sorted_devices[t][i].startup_time)

    #save_devices = [] * data_length
    # ---
    # ここからメインの処理
    for t in range(system_end_time):
        print("[TIME:", t, "]")
        # ある時刻tのMECに割り当てらえたデバイスを一時的に保存する用の変数
        save_devices = [None] * mec_num
        for i in range(num):
            print("---new device---", sorted_devices[t][i].name)
            # plan_indexがデバイスの稼働時間外なら処理をスキップ
            if (check_plan_index(sorted_devices[t][i].plan_index, len(sorted_devices[t][i].plan)) == False):
                print("skip")
                continue
            # plan_indexが稼働時間内なら処理開始
            if check_between_time(sorted_devices[t][i], t) == True:
                print(sorted_devices[t][i].plan_index)
                # 継続 + 最近近傍
                device_flag, memo = continue_search(sorted_devices[t][i], mec, sorted_devices[t][i].plan_index, cover_range, t, continue_distance)
                if device_flag == False:
                    device_flag, memo = nearest_search(sorted_devices[t][i], mec, sorted_devices[t][i].plan_index, cover_range, t)
                # 割り当てが成功したら表示する
                if device_flag == True and memo != 0:
                    #print("device:", sorted_devices[t][i].name, ", use_resource:", sorted_devices[t][i].use_resource, "--->", "MEC_ID:", mec[memo].name, ", index:", i)
                    #print(sorted_devices[t][i].mec_name, mec[memo].resource)
                    #print(memo, len(save_devices))
                    # ---
                    # なぜindexがmemoなの？ <- mec用のリストだから
                    if save_devices[memo] == None:
                        save_devices[memo] = [sorted_devices[t][i].name]
                    else:
                        save_devices[memo].append(sorted_devices[t][i].name)
                    # ---
                    print(t, memo, index)
                    memo = 0
                else:
                    print("NOT FIND")
                # plan_indexをインクリメント
                sorted_devices[t][i]._plan_index = sorted_devices[t][i]._plan_index + 1
        # ある時刻tのMECに一時的に保存していた割り当てたデバイスをコピーする。
        copy_to_mec(mec, save_devices, t)

    #-----
    # リソース消費量がそれぞれで違う時のテスト用関数を作成する
    # 各秒でMECが持っているデバイスのインデックスと数がわかるものとする

    sum = 0
    mec_sum = 0
    having_device_resource_sum = 0
    for t in range(system_end_time):
        #print("time:", t)
        for m in range(150):
            #if t == 16:
                #print("MEC_ID:", mec[m].name, ", having devices:", mec[m]._having_devices[t], mec[m]._having_devices_count[t],
                        #", mec_resouce:", mec[m]._resource_per_second[t], ", current time:", t)
                #sum = sum + mec[m]._having_devices_count[t]
            #mec_sum = mec_sum + mec[m]._resource_per_second[t]
            #sum = sum + mec[m]._having_devices_count[t]
            mec_sum = mec_sum + mec[m]._resource_per_second[t]
            if mec[m]._having_devices[t] is not None:
                #print("check", mec[m]._having_devices[t])
                device_index = device_index_search(sorted_devices[t], mec[m]._having_devices[t])
                #print(mec[m]._having_devices[t], device_index)
                having_device_resource_sum = having_device_resource_sum + device_resource_calc(sorted_devices[t], device_index)
        check_allocation(t, 150, 100, having_device_resource_sum, mec_sum)
        print((15000 - having_device_resource_sum), mec_sum)
        having_device_resource_sum = 0
        sum = 0
        mec_sum = 0
    #print(sum, (150*100-sum), mec_sum)

    print("system_time: ", system_end_time)
    print("MEC_num: ", mec_num)
    print("device_num: ", num)

    sorted_devices = sorted_devices[0:system_end_time]
    maximum, max_device_id = max_hop_search(sorted_devices[-1])
    print("device_id: ", max_device_id, ", max_hop:", maximum)
    minimum, min_device_id = min_hop_search(sorted_devices[-1])
    print("device_id: ", min_device_id, ", min_hop:", minimum)
    average_hop = average_hop_calc(sorted_devices[-1])
    print("average_hop: ", average_hop)
    reboot_rate = application_reboot_rate(mec, system_end_time)
    print("AP reboot rate:", reboot_rate)

    result = [system_end_time]
    result.append(mec_num)
    result.append(num)
    result.append(maximum)
    result.append(max_device_id)
    result.append(minimum)
    result.append(min_device_id)
    result.append(average_hop)
    result.append(reboot_rate)

    # pathを動的に変えることで毎回新しいファイルを作成することができる
    write_csv(path_w, result)
