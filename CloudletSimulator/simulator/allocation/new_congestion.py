from CloudletSimulator.simulator.model.edge_server import MEC_servers, check_add_device,MEC_server
from CloudletSimulator.simulator.model.device import Device,Devices
import math
from math import radians, cos, sin, asin, sqrt, atan2
from typing import List

#system_time = 200
#sorted_device = [Devices]
#sorted_devices = [Devices] * system_time

def traffic_congestion(mecs:MEC_servers, devices: Devices, system_time, seach_distance):
    data_length = len(mecs)
    for t in range (system_time):
        print("time:", t, ", ", t/system_time*100, "%")
        for m in range (data_length):
            traffic_congestion_calc(mecs[m], devices, t, seach_distance)
    #devices_congestion_sort(devices, system_time)

def traffic_congestion_calc(mec:MEC_server, devices: Devices, time , search_distance):
    """
    あるMECのカバー範囲内の要求リソース量の総和を求める計算（混雑度）
    :param device: デバイス
    :param time: システムのある時間t
    :param search_distance: 加算距離
    :return ある時刻tのときのMECのカバー範囲内の要求リソース量の総和
    """
    cnt = 0
    device_num = len(devices)
    sum = 0
    save = [None]
    for i in range(device_num):
        startup = devices[i].startup_time
        shutdown = devices[i].shutdown_time
        if startup <= time and shutdown >= time:
            # デバイスのplanのindex番号を計算
            index = int(time) - int(startup)
            if index < (shutdown - startup):
                distance = distance_calc(float(devices[i].plan[index].y), float(devices[i].plan[index].x), mec.lat,
                                         mec.lon)
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
            devices[save_index]._congestion_status[time] = sum

# デバイスを混雑度順に降順ソートする
def devices_congestion_sort(devices:Device, system_time):
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
