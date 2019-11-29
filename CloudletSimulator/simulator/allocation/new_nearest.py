from CloudletSimulator.simulator.model.edge_server import MEC_servers, check_add_device,MEC_server, check_between_time, check_plan_index
from CloudletSimulator.simulator.model.device import Device
from geopy.distance import vincenty
import math
from math import radians, cos, sin, asin, sqrt, atan2

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

    # 最近傍法を使うために、各MECサーバとの距離を計算
    for m in range(data):
        #position = (mec[m].lat, mec[m].lon)
        if mec[m].check_resource(device.use_resource) == True:
            distance[m] = distance_calc(float(device.plan[plan_index].y),
                                        float(device.plan[plan_index].x), mec[m].lat, mec[m].lon)
            #distance[m] = vincenty(position, device_position).miles * 1609.34
        else:
            distance[m] = None
        #print(distance)
    # 最も距離が近いMECサーバを選び、その配列のインデックスを取得する
    ans_id = distance.index(min(distance))
    if min(distance) <= cover_range:
        # 最も距離が近いMECサーバを選び、その配列のインデックスを取得する
        # ans_id = distance.index(min(distance))
        print(device.mec_name)
        ans_id = mec[ans_id].name
        print(mec[ans_id].name, device.mec_name, device.lost_flag)
        #継続割り当ての時
        if mec[ans_id].name == device.mec_name and device.lost_flag == False:
            print(device.plan[plan_index])
            #mec[ans_id]._mode = "keep"
            device.set_mode = "keep"
            mec[ans_id].custom_resource_adjustment(device, time)
            print("KEEP", plan_index)
            device.mec_name = mec[ans_id].name
            mec[ans_id].add_having_device(time)
            device.switch_lost_flag = False
        # 移動する時(新規割り当て以外)
        elif mec[ans_id].name != device.mec_name and device._lost_flag == False and mec[ans_id].name != None:
            # リソースを増やす
            device.set_mode = "decrease"
            mec[device.mec_name - 1].custom_resource_adjustment(device, time)
            mec[device.mec_name -1].save_resource(time)
            print("DECREASE")
            #mec[device.mec_name-1].decrease_having_device(time)

            # リソースを減らす
            device.set_mode = "add"
            mec[ans_id].custom_resource_adjustment(device, time)
            device.mec_name = mec[ans_id].name
            mec[ans_id].add_having_device(time)
            #mec[ans_id].save_resource(time)
            device.switch_lost_flag = False
        else:
            # リソースを減らす
            device.set_mode = "add"
            mec[ans_id].custom_resource_adjustment(device, time)
            device.mec_name = mec[ans_id].name
            mec[ans_id].add_having_device(time)
            #mec[ans_id].save_resource(time)
            device.switch_lost_flag = False
        return True, ans_id
    else:
        # lostした時リソースを増やす
        if  mec[ans_id].name != None and device._lost_flag == False and check_add_device(time) == False:
            mec[ans_id]._mode == "decrease"
            device.set_mode = "decrease"
            print("DECREASE")
            mec[device.mec_name - 1].custom_resource_adjustment(device, time)
            mec[device.mec_name - 1].save_resource(time)
            #mec[device.mec_name - 1].decrease_having_device(time)
            device.set_mode = "add"

        device.switch_lost_flag = True
        device._lost_flag = True
        device.mec_name = None
        return False, ans_id


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
