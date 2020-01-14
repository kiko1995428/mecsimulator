from CloudletSimulator.simulator.model.edge_server import MEC_servers, check_add_device, MEC_server,check_between_time, check_plan_index
from CloudletSimulator.simulator.model.device import Device
from CloudletSimulator.simulator.model.hop_calc import keep_hop
import math
from math import radians, cos, sin, asin, sqrt, atan2

def continue_search(device:Device, mec:MEC_servers, plan_index, cover_range, time, continue_distance):
    # 指定時間内なら、継続して割り当てるメソッド
    #　継続割り当ての最初の割り当てどうか調べる
    # 指定時間内か調べる
    # カバー範囲内か判定を行う
    #--
    #指定時間以内
    if device.mec_name != [] and device.mec_name is not None:
        print(device.mec_name)
        mec_index = int(device.mec_name) - 1
        # 指定時間以内 かつ　リソース残量OK　かつ　稼働時間内
        if device._continue_count == 0 and mec[mec_index].check_resource(device.use_resource) == True and len(device.plan) > plan_index:
            distance = distance_calc(float(device.plan[plan_index].y),
                                     float(device.plan[plan_index].x), mec[mec_index].lat, mec[mec_index].lon)
            #カバー範囲内なら
            #if distance <= cover_range and distance <= continue_distance:
            if distance <= continue_distance:
                print(device.plan[plan_index])
                device.set_mode = "keep"
                mec[mec_index].custom_resource_adjustment(device, time)

                # 追加
                keep_hop(device)
                mec[mec_index].add_allocation_count(time)
                mec[mec_index]._keep_count = mec[mec_index]._keep_count + 1

                print("KEEP", plan_index)
                device.mec_name = mec[mec_index].name
                mec[mec_index].add_having_device(time)
                mec[mec_index].save_resource(time)
                device.switch_lost_flag = False
                device.set_continue_count("add")
                #return True, mec_index
                return True, mec[mec_index].name
            else:
                device.set_continue_count("reset")
                return False, mec_index
        else:
            device.set_continue_count("reset")
            return False, mec_index
    else:
        device.set_continue_count("reset")
        return False, 0

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