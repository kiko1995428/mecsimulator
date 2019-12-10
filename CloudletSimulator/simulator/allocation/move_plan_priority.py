from CloudletSimulator.simulator.model.edge_server import MEC_servers, check_add_device, check_between_time
from CloudletSimulator.simulator.model.device import Device
from geopy.distance import vincenty
import math
from math import radians, cos, sin, asin, sqrt, atan2


# 移動経路優先度計算
def move_plan_priority_calc(mec:MEC_servers, device:Device, plan_index, time, f_time):
    if time % f_time == 0 and plan_index + f_time < len(device.plan):
        mec_num = len(mec)
        # 各MECサーバとの距離を計算
        for m in range(mec_num):

            if mec[m].check_resource(device.use_resource) == True and len(device.plan[plan_index + f_time]) > plan_index:
                mec[m]._device_distance = distance_calc(float(device.plan[plan_index + f_time].y),
                                            float(device.plan[plan_index + f_time].x), mec[m].lat, mec[m].lon)
        sorted_mecs = sorted(mec, key=lambda  m:m._device_distance)
        return True, sorted_mecs
    else:
        return False, mec

# 移動経路優先割り当て
def priority_allocation(mecs:MEC_servers, device:Device, plan_index, time):
    mec_num = len(mecs)
    memo = 0
    previous_index = mec_index_search(mecs, device)
    device_flag = False
    if check_between_time(device, time) == True:
        for m in range(mec_num):
            if (mecs[m].check_resource(device.use_resource) == True) and (plan_index < len(device.plan)):
                device_flag, memo = mode_adjustment(mecs, m, device, time)
                if device_flag == True:
                    return True, memo - 1
            # 最後まで見つからないとき
            if mec_num <= m and device_flag == False:
                # 初めてlost状態のときに中間局までデバイスを投げる
                if mecs[m].name != None and device._lost_flag == False:
                    device.set_mode = "decrease"
                    #print("DECREASE")
                    mecs[previous_index].custom_resource_adjustment(device, time)
                    mecs[previous_index].save_resource(time)
                    device.add_hop_count()
                    device.set_mode = "add"
                # lost状態
                device.switch_lost_flag = True
                device._lost_flag = True
                device.mec_name = None
    return False, memo-1

def mode_adjustment(mecs:MEC_servers, mec_index, device: Device, time):
    plan_index = device.plan_index
    previous_index = mec_index_search(mecs, device)
    if (mecs[mec_index].resource > 0) and ((mecs[mec_index].resource - device.use_resource) >= 0) and plan_index < len(device.plan):
        current_distance = distance_calc(float(device.plan[plan_index].y),
                                         float(device.plan[plan_index].x), mecs[mec_index].lat, mecs[mec_index].lon)
        current_id, device_flag = mecs[mec_index].custom_cover_range_search(device, plan_index)
        #if device_flag is True and device.mec_name is not None:
            #print("device_flag", device_flag, "current_id", current_id, "device.MEC_name", device.mec_name, ", check add device", check_add_device(device, time) )
        if (device_flag == True and current_id == device.mec_name):
            #print("MEC", mecs[mec_index].name, "KEEP", ", plan_index[", device.name, "]:", plan_index)
            #print("KEEP")
            device.set_mode = "keep"
            mecs[mec_index].custom_resource_adjustment(device, time)
            device.mec_name = mecs[mec_index].name
            mecs[mec_index].add_having_device(time)
            mecs[mec_index].save_resource(time)
            device.switch_lost_flag = False
            current_id = mecs[mec_index].name
            return True, current_id
        # 切替&切替先を見つけている時
        elif device_flag == True and current_id != device.mec_name and check_add_device(device, time) == False and device.mec_name is not None:
            # リソースを増やす
            #print("DECREASE(main)")
            device.set_mode = "decrease"
            mecs[previous_index].custom_resource_adjustment(device, time)
            #print("リソース回復",device._mec_name, mecs[previous_index].name, mecs[previous_index].resource)
            device.add_hop_count()
            mecs[previous_index].save_resource(time)

            #print("ADD")
            device.set_mode = "add"
            device.mec_name = mecs[mec_index].name
            mecs[mec_index].add_having_device(time)
            device.add_hop_count()
            mecs[mec_index].add_reboot_count(time)
            mecs[mec_index].custom_resource_adjustment(device, time)
            mecs[mec_index].save_resource(time)
            device.switch_lost_flag = False
            current_id = mecs[mec_index].name
            return True, current_id

        # 新規割り当て or lost時からの割り当て
        elif device_flag == True and current_id != device.mec_name and check_add_device(device, time) == True:
            #print("ADD")
            device.set_mode = "add"
            device.mec_name = mecs[mec_index].name
            mecs[mec_index].add_having_device(time)
            device.add_hop_count()
            # lost時の割り当てのみ
            if device._lost_flag == True and device.startup_time != time:
                mecs[mec_index].add_reboot_count(time)
            mecs[mec_index].custom_resource_adjustment(device, time)
            mecs[mec_index].save_resource(time)
            device.switch_lost_flag = False
            current_id = mecs[mec_index].name
            return True, current_id
        else:
            device.set_mode = "add"
            return False, current_id

def cover_range_search(mecs:MEC_servers, mec_index, device: Device, time):
    memo = 0
    plan_index = device.plan_index
    if (mecs[mec_index].resource > 0) and ((mecs[mec_index].resource - device.use_resource) >= 0):
        distance = distance_calc(float(device.plan[plan_index].y),
                                 float(device.plan[plan_index].x), mecs[mec_index].lat, mecs[mec_index].lon)
        if distance <= mecs[mec_index].range:
            memo = mec_index
            # リソースを減らす
            device.add_hop_count()
            device.mec_name = mecs[mec_index].name
            mecs[mec_index].add_having_device(time)
            if device._lost_flag == True and device.startup_time != time:
                mecs[mec_index].add_reboot_count(time)
            # リソース割り当て
            #print("MEC_ID", mecs[mec_index].name)
            mecs[mec_index].custom_resource_adjustment(device, time)
            mecs[mec_index].save_resource(time)
            device.switch_lost_flag = False
            return True, memo
    return False, memo
"""
        elif mecs[mec_index].name != None and device._lost_flag == False:
            print("-------------")
            device.set_mode = "decrease"
            print("DECREASE")
            mecs[device.mec_name - 1].custom_resource_adjustment(device, time)
            mecs[device.mec_name - 1].save_resource(time)
            device.add_hop_count() 
            device.set_mode = "add"
            device.switch_lost_flag = True
            device._lost_flag = True
            device.mec_name = None
            return False, memo
    # lostした時リソースを増やす
    if device._lost_flag == False:
        print("+++++++++++++")
        device.set_mode = "decrease"
        print("DECREASE")
        mecs[device.mec_name - 1].custom_resource_adjustment(device, time)
        device.add_hop_count()
        mecs[device.mec_name - 1].save_resource(time)
        device.set_mode = "add"
"""

    #device.switch_lost_flag = True
    #device._lost_flag = True
    #device.mec_name = None
    #return False, memo

def mec_index_search(mecs:MEC_servers, device:Device):
    mec_num = len(mecs)
    for m in range (mec_num):
        if device.mec_name == mecs[m].name:
            return m
            break



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