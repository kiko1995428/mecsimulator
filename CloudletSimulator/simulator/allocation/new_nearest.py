from CloudletSimulator.simulator.model.edge_server import MEC_servers, check_add_device,MEC_server, check_between_time, check_plan_index
from CloudletSimulator.simulator.model.device import Device
from CloudletSimulator.simulator.model.hop_calc import hop_calc, keep_hop
from geopy.distance import vincenty
import math
from math import radians, cos, sin, asin, sqrt, atan2
import sys
import numpy
import collections
from typing import List, Dict


def nearest_search(device:Device, mec:MEC_servers, plan_index, cover_range, time):
    """
    最近傍法のアルゴリズムでリソース割り当てを行うメソッド
    最も近いMECサーバをデバイスに割り当てる
    :param device: デバイス
    :param mec: MECサーバ群
    :param plan_index: デバイスのplanのindex
    :param cover_range: 基地局のカバー範囲
    :param time: 現在時刻t
    :return: 割り当てたans_idをTrueと共に返す, 割り当てられなかった時はFalseを返す
    """
    # data = len(mec)
    data = 100
    distance = [None] * data
    #device_lat = float(device.plan[plan_index].y)
    #device_lon = float(device.plan[plan_index].x)
    #device_position = (device_lat, device_lon)
    cnt = 0

    # 最近傍法を使うために、各MECサーバとの距離を計算
    for m in range(data):
        #position = (mec[m].lat, mec[m].lon)
        if mec[m].check_resource(device.use_resource) == True and len(device.plan) > plan_index:
            distance[m] = distance_calc(float(device.plan[plan_index].y),
                                        float(device.plan[plan_index].x), mec[m].lat, mec[m].lon)
            #distance[m] = vincenty(position, device_position).miles * 1609.34
        else:
            distance[m] = 100000000000
            cnt = cnt + 1
        #print(distance)
    if cnt < data:
        # 最も距離が近いMECサーバを選び、その配列のインデックスを取得する
        ans_id = distance.index(min(distance))

        #if min(distance) <= cover_range:
        if True:
            # 最も距離が近いMECサーバを選び、その配列のインデックスを取得する
            # ans_id = distance.index(min(distance))
            print(device.mec_name)
            ans_id = mec[ans_id].name
            print(mec[ans_id].name, device.mec_name, device.lost_flag)
            #継続割り当ての時
            if mec[ans_id].name == device.mec_name and device.lost_flag == False:
                print(device.plan[plan_index])
                device.set_mode = "keep"
                mec[ans_id].custom_resource_adjustment(device, time)
                print("KEEP", plan_index)
                device.mec_name = mec[ans_id].name

                mec[ans_id].add_having_device(time)
                mec[ans_id].save_resource(time)
                device.switch_lost_flag = False

                # 追加項目
                keep_hop(device)
                print(mec[ans_id].aggregation_station)
                device._aggregation_name = mec[ans_id].aggregation_station
                mec[ans_id].add_allocation_count(time)
                mec[ans_id]._keep_count = mec[ans_id]._keep_count + 1

            # 移動する時(新規割り当て以外)
            elif mec[ans_id].name != device.mec_name and device._lost_flag == False and mec[ans_id].name != None:
                # リソースを増やす
                device.set_mode = "decrease"
                mec[device.mec_name - 1].custom_resource_adjustment(device, time)
                device.add_hop_count()
                #hop_calc(device, mec[device.mec_name - 1])
                mec[device.mec_name - 1].save_resource(time)
                print("DECREASE")
                print("切替", device._aggregation_name, mec[ans_id])

                # リソースを減らす
                device.set_mode = "add"
                mec[ans_id].custom_resource_adjustment(device, time)
                device.add_hop_count()
                device.mec_name = mec[ans_id].name

                # 新規追加
                hop_calc(device, mec[ans_id], time)
                device._aggregation_name = mec[ans_id].aggregation_station

                mec[ans_id].add_having_device(time)
                mec[ans_id].save_resource(time)
                device.switch_lost_flag = False
            else:
                # リソースを減らす
                device.set_mode = "add"
                mec[ans_id].custom_resource_adjustment(device, time)
                device.add_hop_count()

                device.mec_name = mec[ans_id].name

                # 新規追加
                hop_calc(device, mec[ans_id], time)
                device._aggregation_name = mec[ans_id].aggregation_station

                mec[ans_id].add_having_device(time)
                mec[ans_id].save_resource(time)
                #if device._lost_flag == True and device.startup_time != time:
                    #mec[ans_id].add_reboot_count(time)
                device.switch_lost_flag = False
            return True, ans_id
        else:
            # lostした時リソースを増やす
            #if  mec[ans_id].name != None and device._lost_flag == False and check_add_device(device, time) == False:
            if mec[ans_id].name != None and device._lost_flag == False:
                device.set_mode = "decrease"
                print("DECREASE")
                mec[device.mec_name - 1].custom_resource_adjustment(device, time)
                mec[device.mec_name - 1].save_resource(time)
                device.add_hop_count()
                device.set_mode = "add"
            device.switch_lost_flag = True
            device._lost_flag = True
            device.mec_name = None
            return False, ans_id
    else:
        # lostした時リソースを増やす
        #if device._lost_flag == False and check_add_device(device, time) == False:
        if device._lost_flag == False:
            device.set_mode = "decrease"
            print("DECREASE")
            mec[device.mec_name - 1].custom_resource_adjustment(device, time)
            device.add_hop_count()
            mec[device.mec_name - 1].save_resource(time)
            device.set_mode = "add"

        #print(device._lost_flag)
        device.switch_lost_flag = True
        device._lost_flag = True
        device.mec_name = None
        ans_id = None
        print("---------------")
        return False, ans_id


# lost割り当てなし
def nearest_search2(device:Device, mec:MEC_servers, plan_index, cover_range, time):
    """
    最近傍法のアルゴリズムでリソース割り当てを行うメソッド
    最も近いMECサーバをデバイスに割り当てる
    :param device: デバイス
    :param mec: MECサーバ群
    :param plan_index: デバイスのplanのindex
    :param cover_range: 基地局のカバー範囲
    :param time: 現在時刻t
    :return: 割り当てたans_idをTrueと共に返す, 割り当てられなかった時はFalseを返す
    """
    data = len(mec)
    distance = collections.namedtuple("distance", ("index", "value"))
    mec_distance = [distance] * data
    cnt = 0

    # 最近傍法を使うために、各MECサーバとの距離を計算
    for m in range(data):
        #position = (mec[m].lat, mec[m].lon)
        if mec[m].check_resource(device.use_resource) == True and len(device.plan) > plan_index and mec[m].resource>0:
            #print(mec[m].check_resource(device.use_resource))
            tmp_distance = distance_calc(float(device.plan[plan_index].y),
                                        float(device.plan[plan_index].x), mec[m].lat, mec[m].lon)
            mec_distance[m] = distance(m, tmp_distance)
            #distance[m] = vincenty(position, device_position).miles * 1609.34
        else:
            #distance[m] = 1000000.0000
            mec_distance[m] = distance(m, 1000000000)
            cnt = cnt + 1
        #print(distance)
    #if cnt < data:
    # 最も距離が近いMECサーバを選び、その配列のインデックスを取得する
    #for m in range(data):
        #if mec[m].resource <= 0:
            #distance[m] = 1000000000000000

    #ここが間違ってる
    # 距離が同じ場合がある時、別のindexを返すことになる

    #ans_id = distance.index(min(distance))
    sorted_distance = sorted(mec_distance, key=lambda m:m.value)
    ans_id = sorted_distance[0].index
    if mec_distance[ans_id].value != sorted_distance[0].value:
        print(mec_distance[ans_id], sorted_distance[0])
        sys.exit()
    if mec[ans_id].resource == 0:
        print(mec_distance[ans_id], sorted_distance[0])
        sys.exit()
    ans_id = ans_id

    # 最も距離が近いMECサーバを選び、その配列のインデックスを取得する
    # ans_id = distance.index(min(distance))
    #print(device.mec_name)
    #ans_id = mec[ans_id].name
    print(mec[ans_id].name, device.mec_name, device.lost_flag)
    if mec[ans_id].resource > 0:
        #継続割り当ての時
        if mec[ans_id].name == device.mec_name:
            device.set_mode = "keep"
            mec[ans_id].custom_resource_adjustment(device, time)
            print("KEEP", plan_index)
            device.mec_name = mec[ans_id].name

            mec[ans_id].add_having_device(time)
            mec[ans_id].save_resource(time)
            device.switch_lost_flag = False

            # 追加項目
            keep_hop(device)
            print(mec[ans_id].aggregation_station)
            device._aggregation_name = mec[ans_id].aggregation_station
            mec[ans_id].add_allocation_count(time)
            mec[ans_id]._keep_count = mec[ans_id]._keep_count + 1

        # 移動する時(新規割り当て以外)
        elif mec[ans_id].name != device.mec_name and mec[ans_id].name != None and device.mec_name != []:
            #mec_index = mec_index_search(device, mec)
            # リソースを増やす
            device.set_mode = "decrease"
            print("デバイスの前のMEC:", device.mec_name, "前のMEC", mec[device.mec_name - 1].name)
            # 前に割り振ったMECのリソースを回復
            mec[device.mec_name - 1].custom_resource_adjustment(device, time)
            device.add_hop_count()
            #hop_calc(device, mec[device.mec_name - 1])
            mec[device.mec_name - 1].save_resource(time)
            print("DECREASE")
            print("切替", device._aggregation_name, mec[ans_id])

            # リソースを減らす
            device.set_mode = "add"
            mec[ans_id].custom_resource_adjustment(device, time)
            device.add_hop_count()
            device.mec_name = mec[ans_id].name

            # 新規追加
            hop_calc(device, mec[ans_id], time)
            device._aggregation_name = mec[ans_id].aggregation_station

            mec[ans_id].add_having_device(time)
            mec[ans_id].save_resource(time)
            device.switch_lost_flag = False
        else:
            # リソースを減らす
            device.set_mode = "add"
            mec[ans_id].custom_resource_adjustment(device, time)
            device.add_hop_count()

            device.mec_name = mec[ans_id].name

            # 新規追加
            hop_calc(device, mec[ans_id], time)
            device._aggregation_name = mec[ans_id].aggregation_station

            mec[ans_id].add_having_device(time)
            mec[ans_id].save_resource(time)
            #if device._lost_flag == True and device.startup_time != time:
                #mec[ans_id].add_reboot_count(time)
            device.switch_lost_flag = False
        print("MEC_RESOURCE", mec[ans_id].resource)
        return True, ans_id
    for m in range(data):
        print(m, ans_id, mec_distance[m])
    print("mec_id", mec[ans_id].name, "resource", mec[ans_id].resource, "distance", mec_distance[ans_id])
    sys.exit()
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

