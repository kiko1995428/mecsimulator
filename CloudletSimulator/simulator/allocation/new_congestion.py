from CloudletSimulator.simulator.model.edge_server import MEC_servers, check_add_device,MEC_server
from CloudletSimulator.simulator.model.device import Device, Devices, device_index_search
import math
from math import radians, cos, sin, asin, sqrt, atan2
from typing import List

#system_time = 200
#sorted_device = [Devices]
#sorted_devices = [Devices] * system_time

def traffic_congestion(mecs:MEC_servers, devices: Devices, system_time, seach_distance):
    """
    あるMECのカバー範囲内の要求リソース量の総和を求める計算（混雑度）
    :param mecs: MEC群
    :param device: デバイス群
    :param system_time: システムのある時間t
    :param search_distance: 加算距離
    """
    data_length = len(mecs)
    for t in range (system_time):
        print("time:", t, ", ", t/system_time*100, "%")
        # 各MECごとの混雑度を計算
        for m in range(data_length):
            mecs[m], devices = traffic_congestion_calc(mecs, mecs[m], devices, t, seach_distance)
    num = len(devices)
    for d in range(num):
        devices[d].mec_name = []
    #devices_congestion_sort(devices, system_time)

def traffic_congestion_calc(mecs:MEC_servers, mec:MEC_server, devices: Devices, time , search_distance):
    """
    あるMECのカバー範囲内の要求リソース量の総和を求める計算（混雑度）
    :param mec: あるMECサーバ
    :param device: デバイス群
    :param time: システムのある時間t
    :param search_distance: 加算距離
    :return ある時刻tのときのMECのカバー範囲内の要求リソース量の総和
    """
    cnt = 0
    device_num = len(devices)
    sum = 0
    # デバイスのインデックスを保存するための変数
    save = [None]
    for i in range(device_num):
        startup = devices[i].startup_time
        shutdown = devices[i].shutdown_time
        if startup <= time and shutdown >= time:
            # デバイスのplanのindex番号を計算
            index = int(time) - int(startup)
            if index < (shutdown - startup):
                # デバイスとMECとの距離を計算
                distance = distance_calc(float(devices[i].plan[index].y), float(devices[i].plan[index].x), mec.lat,
                                         mec.lon)
                # 探索距離内あるか判定
                # もしあれば追加
                if distance <= (search_distance):
                    if save[0] is None:
                        save[0] = i
                    else:
                        save.append(i)
                    cnt = cnt + 1
                    sum = sum + devices[i].use_resource
    #print(save)
    mec._congestion_status[time] = sum
    if save[0] != None:
        for save_index in save:
            # 混雑度が多ければ、値を更新する
            if devices[save_index]._congestion_status[time] == 0:
                devices[save_index]._congestion_status[time] = sum
                # 先に計算したMECと比較するために保存
                devices[save_index].mec_name = mec.name
            elif devices[save_index]._congestion_status[time] < sum:
                devices[save_index]._congestion_status[time] = sum
                devices[save_index].mec_name = mec.name
            else:
            # 値が被る時
                startup = devices[save_index].startup_time
                index = int(time) - int(startup)
                if index < (shutdown - startup):
                    previous_mec = search_mec(mecs, devices[save_index].mec_name)
                    previous_distance = distance_calc(float(devices[save_index].plan[index].y),
                                                      float(devices[save_index].plan[index].x),
                                                      previous_mec.lat, previous_mec.lon)
                    current_distance = distance_calc(float(devices[save_index].plan[index].y),
                                                      float(devices[save_index].plan[index].x), mec.lat, mec.lon)
                    if current_distance < previous_distance:
                        devices[save_index]._congestion_status[time] = sum
                        devices[save_index].mec_name = mec.name
    return mec, devices
"""
def congestion_map_calc():
    min_lat = 34.632282
    max_lat = 34.652382
    min_lon = 133.87895
    max_lon = 133.92678
    lat_value = (max_lat - min_lat) / 50
    lon_value = (max_lon - min_lon) / 50
    for n in range(250):
        # 格子状の範囲で地図を区切り、混雑度を計算できるようにする。
    print()
"""

# デバイスを混雑度順に降順ソートする
def devices_congestion_sort(devices:Device, system_time):
    """
    デバイス群を毎秒ごとに混雑度順に降順ソートする
    :param devices: あるデバイス
    :param system_time: ある時間
    :return ソート済のデバイス群
    """
    sorted_devices = [Devices] * system_time
    for t in range(system_time):
        sorted_devices[t] = sorted(devices, key=lambda d: d._congestion_status[t], reverse=True)
    return sorted_devices

# ユーグリット距離
def distance_calc(lat1, lon1, lat2, lon2):
    """
    ２点の緯度経度から距離（メートル）を計算するメソッド
    :param lat1 : １点目の　lat
    :param lon1 : １点目の　lot
    :param lat2 : ２点目の　lat
    :param lot2 : ２点目の　lot
    :return : 距離
    """
    # return distance as meter if you want km distance, remove "* 1000"
    radius = 6371 * 1000

    dLat = (lat2 - lat1) * math.pi / 180
    dLot = (lon2 - lon1) * math.pi / 180

    lat1 = lat1 * math.pi / 180
    lat2 = lat2 * math.pi / 180

    val = sin(dLat / 2) * sin(dLat / 2) + sin(dLot / 2) * sin(dLot / 2) * cos(lat1) * cos(lat2)
    ang = 2 * atan2(sqrt(val), sqrt(1 - val))
    return radius * ang  # meter

def search_mec(mecs:MEC_servers, mec_name):
    mec_num = len(mecs)
    for m in range(mec_num):
        if mecs[m].name == mec_name:
            return mecs[m]