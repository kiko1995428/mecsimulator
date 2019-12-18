# プロトタイププログラム
# まず、make_binanary.pyでバイナリーファイルを作成し、このプログラムを実行する

from CloudletSimulator.simulator.model.edge_server import MEC_server, MEC_servers, check_between_time, check_plan_index, check_allocation, copy_to_mec, application_reboot_rate
from CloudletSimulator.simulator.model.device import max_hop_search, min_hop_search, average_hop_calc,device_index_search, device_resource_calc
from CloudletSimulator.simulator.allocation.new_congestion import traffic_congestion, devices_congestion_sort
from CloudletSimulator.simulator.allocation.new_continue import continue_search
from CloudletSimulator.simulator.convenient_function.write_csv import write_csv
from CloudletSimulator.simulator.allocation.new_nearest import nearest_search
from CloudletSimulator.simulator.allocation.move_plan_priority import move_plan_priority_calc, priority_allocation, mec_index_search,search_mec_index
from CloudletSimulator.simulator.model.aggregation_station import set_aggregation_station
import pandas as pd
import pickle


def continue_priority_simulation(system_end_time, MEC_resource, device_num, continue_distance, f_time, device_allocation_method, path_w):

    df = pd.read_csv("/Users/sugimurayuuki/Desktop/mecsimulator/CloudletSimulator/base_station/kddi_okayama_city.csv",
                     dtype={'lon': 'float', 'lat': 'float'})
    server_type = "LTE"
    cover_range = 500
    n = len(df)
    print("Number of MEC server:", n)
    mec = [MEC_server(0, 00, " ", 00.00, 00.00, 0, 0)] * n
    for index, series in df.iterrows():
        mec[index] = MEC_server(MEC_resource, index + 1, server_type, series["lon"], series["lat"],
                                cover_range, system_end_time)
    mec_num = len(df)

    # 集約局を対応するMECに設定する
    set_aggregation_station(mec)

    # 到着順
    if device_allocation_method == 0:
        d = open('/Users/sugimurayuuki/Desktop/mecsimulator/CloudletSimulator/dataset/device.binaryfile', 'rb')
        devices = pickle.load(d)
        devices = devices[0:device_num]
        num = len(devices)
        for i in range(num):
            devices[i].startup_time = float(devices[i].plan[0].time)  # 各デバイスの起動時間を設定する
            devices[i].set_congestion_status(system_end_time)
            devices[i].set_MEC_distance(len(df))
            devices[i]._first_flag = True
            devices[i]._allocation_plan = [None] * system_end_time

        sorted_devices = [devices] * system_end_time
    # リソース順
    elif device_allocation_method == 1:
        d = open('/Users/sugimurayuuki/Desktop/mecsimulator/CloudletSimulator/dataset/device.binaryfile', 'rb')
        devices = pickle.load(d)
        devices = devices[0:device_num]
        num = len(devices)
        devices = reverse_resource_sort(devices)
        for i in range(num):
            devices[i].startup_time = float(devices[i].plan[0].time)  # 各デバイスの起動時間を設定する
            devices[i].set_congestion_status(system_end_time)
            devices[i].set_MEC_distance(len(df))
            devices[i]._first_flag = True
        sorted_devices = [devices] * system_end_time
    # 混雑度順
    else:
        # 混雑度計算
        # traffic_congestion(mec, devices, system_end_time, 1000)
        cd = open('/Users/sugimurayuuki/Desktop/mecsimulator/CloudletSimulator/dataset/congestion_checked_devices.binaryfile', 'rb')
        cd = pickle.load(cd)
        devices = cd
        num = len(devices)
        print("device_num", num)

        # 混雑度順で毎秒ごとのdevicesをソートする
        sorted_devices = devices_congestion_sort(devices, system_end_time)

    keep_count = 0
    # save_devices = [] * data_length
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
                # 継続割り当て
                continue_flag, allocation_MEC_name = continue_search(sorted_devices[t][i], mec,
                                                                     sorted_devices[t][i].plan_index, cover_range, t,
                                                                     continue_distance)

                if continue_flag == True:
                    keep_count = keep_count + 1
                if continue_flag == False:
                    print("移動経路優先度選択")
                    loop_count = 0
                    # 移動経路優先で使う探索範囲の初期化
                    search_distance = continue_distance
                    # 移動経路優先で使う未来の時刻の初期化
                    ftime = f_time
                    # 優先度割り当て用のFLAGの初期化
                    property_flag = False
                    # 優先度を割り当てられるまで完了するまでループ（探索範囲内にMECがなければ、距離を500つずつ増やす）
                    # 車の平均速度を50km/hと仮定すると13m/s
                    while (property_flag == False):
                        # 予測時間の時にデバイスが稼働時間内の場合
                        if sorted_devices[t][i].plan_index + ftime < len(sorted_devices[t][i].plan):
                            print("if")
                            # 優先度ソート用のFLAGの初期化
                            sort_flag = False
                            # 移動経路優先度計算が完了するまで繰り返す
                            calc_count = 0
                            while (sort_flag == False):
                                print("calc")
                                calc_count = calc_count + 1
                                print("ソート直前ののMECの長さ", len(mec))
                                # 移動経路優先度にMECをソート
                                sort_flag, sorted_mecs, sort_finish_index = move_plan_priority_calc(mec, sorted_devices[t][i], sorted_devices[t][i].plan_index, t, ftime, search_distance)
                                print("ソート直後ののMECの長さ", len(sorted_mecs))
                                # 探索範囲の加算
                                search_distance = search_distance + 500
                            print(sort_flag, search_distance, sorted_devices[t][i].plan_index + ftime,
                                  len(sorted_devices[t][i].plan))
                            # 優先度順にソートしたMECを選択
                            property_flag, allocation_MEC_name = priority_allocation(sorted_mecs, sorted_devices[t][i],
                                                                                     sorted_devices[t][i].plan_index, t,
                                                                                     sort_finish_index)
                            # MECを更新
                            if property_flag == True:
                                mec = sorted_mecs

                        # 予測時間がデバイスの稼働時間を超えてしまった場合
                        else:
                            print("else")
                            # デバイスの終了時間のインデックスを調べる
                            shutdown_index = sorted_devices[t][i].shutdown_time - sorted_devices[t][i].startup_time
                            # デバイスの終了時間のインデックスを予測時間に代入
                            ftime = shutdown_index - sorted_devices[t][i].plan_index

                # 継続割り当て or 移動経路優先割り当てに成功した場合
                # 割り当てたときのMECとデバイスの情報を表示
                if continue_flag == True or property_flag == True:

                    # 移動経路優先割り当てでソートした場合
                    # MECを更新
                    # if property_flag == True:
                    # mec = sorted_mecs

                    # ID順に昇順ソート
                    mec = sorted(mec, key=lambda m: m.name, reverse=False)

                    # deviceが直前で割り当てたMECを取得
                    mec_index = search_mec_index(mec, allocation_MEC_name)

                    print(mec_index, mec[mec_index].name)
                    print("device:", sorted_devices[t][i].name, ", use_resource:", sorted_devices[t][i].use_resource,
                          "--->", "MEC_ID:", mec[mec_index].name, ", index:", i)
                    print("割り振られたMEC:", sorted_devices[t][i].mec_name, ", MEC残量リソース:", mec[mec_index].resource)
                    print(mec_index, len(save_devices))

                    # ---
                    # 毎秒ごとの割り当てたデバイスを保存
                    # なぜindexがmec_indexなの？ <- mec用のリストだから
                    if save_devices[mec_index] == None:
                        save_devices[mec_index] = [sorted_devices[t][i].name]
                    else:
                        save_devices[mec_index].append(sorted_devices[t][i].name)
                    # ---
                    # print(t, mec_index, index)
                    allocation_MEC_name = 0
                else:
                    # デバイスが割り振れなかった時
                    # ここが実行されるのは本来ありえない
                    print("NOT FIND")
                    print("not find MEC error")
                    sys.exit()

                # plan_indexをインクリメント(planを読み込むため)
                sorted_devices[t][i]._plan_index = sorted_devices[t][i]._plan_index + 1

            else:
                # デバイスの稼働時間を超えた時の処理
                if sorted_devices[t][i].mec_name != [] and sorted_devices[t][i]._lost_flag == False:
                    mec = sorted(mec, key=lambda m: m.name, reverse=False)
                    print("device", sorted_devices[t][i].mec_name, ": shutdown")
                    print("DECREASE")
                    sorted_devices[t][i].set_mode = "decrease"
                    print(sorted_devices[t][i].mec_name)
                    mec[sorted_devices[t][i].mec_name - 1].custom_resource_adjustment(sorted_devices[t][i], t)
                    mec[sorted_devices[t][i].mec_name - 1].save_resource(t)
                    sorted_devices[t][i].set_mode = "add"
                    sorted_devices[t][i]._lost_flag = True

    # ある時刻tのMECに一時的に保存していた割り当てたデバイスをコピーする。
    copy_to_mec(mec, save_devices, t)

    # MECを昇順に直す
    mec = sorted(mec, key=lambda m: m.name, reverse=False)

    sum = 0
    mec_sum = 0
    having_device_resource_sum = 0
    for t in range(system_end_time):
        # print("time:", t)
        for m in range(mec_num):
            if t == 95:
                # if mec[m]._having_devices_count[t] != (MEC_resource- mec[m]._resource_per_second[t]):
                # if mec[m].name == 11:
                print("MEC_ID:", mec[m].name, ", having devices:", mec[m]._having_devices[t],
                      mec[m]._having_devices_count[t],
                      ", mec_resouce:", mec[m]._resource_per_second[t], ", current time:", t, mec[m]._test)
                # sum = sum + mec[m]._having_devices_count[t]
            # mec_sum = mec_sum + mec[m]._resource_per_second[t]
            # sum = sum + mec[m]._having_devices_count[t]
            mec_sum = mec_sum + mec[m]._resource_per_second[t]
            if mec[m]._having_devices[t] is not None:
                # print("check", mec[m]._having_devices[t])
                device_index = device_index_search(sorted_devices[t], mec[m]._having_devices[t])
                # print(mec[m]._having_devices[t], device_index)
                having_device_resource_sum = having_device_resource_sum + device_resource_calc(sorted_devices[t],
                                                                                               device_index)
        check_allocation(t, mec_num, MEC_resource, having_device_resource_sum, mec_sum)
        print((mec_num * MEC_resource - having_device_resource_sum), mec_sum)
        having_device_resource_sum = 0
        sum = 0
        mec_sum = 0
    # print(sum, (150*100-sum), mec_sum)

    print("system_time: ", system_end_time)
    print("MEC_num: ", mec_num)
    print("device_num: ", num)

    sorted_devices = sorted_devices[0:system_end_time]
    maximum = max_hop_search(sorted_devices[-1])
    print("max_hop: ", maximum)
    minimum = min_hop_search(sorted_devices[-1])
    print("min_hop: ", minimum)
    average_hop = average_hop_calc(sorted_devices[-1])
    print("average_hop: ", average_hop)
    reboot_rate = application_reboot_rate(mec, system_end_time)
    print("AP reboot rate:", reboot_rate)
    print("continue_count", keep_count)

    result = [system_end_time]
    result.append(mec_num)
    result.append(num)
    result.append(maximum)
    result.append(minimum)
    result.append(average_hop)
    result.append(reboot_rate)

    # pathを動的に変えることで毎回新しいファイルを作成することができる
    write_csv(path_w, result)
    print("finish")