from CloudletSimulator.simulator.model.edge_server import MEC_servers, check_add_device,MEC_server
from CloudletSimulator.simulator.model.device import Device,Devices
from geopy.distance import vincenty
import math
from math import radians, cos, sin, asin, sqrt, atan2


# 混雑度の基準値
def congestion_standard(mec: MEC_server):
    return mec.resource * 0.3

def all_traffic_congestion(mecs:MEC_servers, devices: Devices, system_time):
    data_length = len(mecs)
    for t in range (system_time):
        for m in range (data_length):
            create_congestion_list(mecs[m], mecs[m].traffic_congestion(devices, t), t)


def traffic_congestion(mec:MEC_server, devices: Devices, time):
    """
    あるMECのカバー範囲内の要求リソース量の総和を求める計算（混雑度）
    :param device: デバイス
    :param time: システムのある時間t
    :return ある時刻tのときのMECのカバー範囲内の要求リソース量の総和
    """
    cnt = 0
    device_num = len(devices)
    sum = 0
    for i in range(device_num):
        startup = devices[i].startup_time
        shutdown = devices[i].shutdown_time
        if startup <= time and shutdown >= time:
            # デバイスのplanのindex番号を計算
            index = int(time) - int(startup)
            if index < (shutdown - startup):
                distance = distance_calc(float(devices[i].plan[index].y), float(devices[i].plan[index].x), mec.lat,
                                         mec.lon)
                if distance <= mec.range:
                    cnt = cnt + 1
                    sum = sum + devices[i].use_resource
    return sum


def congestion_check(mec:MEC_server, total_resource):
    """
    混雑しているかのチェック
    :param total_resource:要求リソース量
    :return: true -> 実行可能, false -> 実行不可能
    """
    if total_resource >= congestion_standard(mec):
        return True
    else:
        return False


def create_congestion_list(mec:MEC_server, total_resource, current_time):
    """
    混雑度表を作成するメソッド
    :param total_resource:カバー範囲内のデバイスの総要求リソース量
    :param current_time:現在時刻
    :return 混雑している場合はTrue, そうでなければFalse
    """
    if total_resource >= mec.congestion_standard:
        mec._congestion_flag[current_time] = True
    else:
        mec._congestion_flag[current_time] = False

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
