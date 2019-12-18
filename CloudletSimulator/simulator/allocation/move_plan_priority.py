from CloudletSimulator.simulator.model.edge_server import MEC_servers, check_add_device, check_between_time
from CloudletSimulator.simulator.model.device import Device
from CloudletSimulator.simulator.model.hop_calc import hop_calc, keep_hop
import math
from math import radians, cos, sin, asin, sqrt, atan2
import sys
import collections

# 移動経路優先度計算
def move_plan_priority_calc(mecs:MEC_servers, device:Device, plan_index, time, f_time, continue_distance):
    hoge_hoge = mecs
    len_hoge = len(hoge_hoge)
    # sorted_flagをリセット
    mecs = reset_sorted_mec(mecs)
    # 予測時間の時に探索が終わっていないかどうか
    #if plan_index + f_time < len(device.plan):
    mec_num = len(mecs)
    mec = None
    mec_set = collections.namedtuple("mec_set", ("ID", "way"))
    # 各MECサーバとの距離を計算
    for m in range(mec_num):
        print(device.plan_index, f_time, len(device.plan))
        disntace = distance_calc(float(device.plan[plan_index + int(f_time)].y), float(device.plan[plan_index + int(f_time)].x), mecs[m].lat, mecs[m].lon)
       # 継続割り当ての距離以内にいるサーバを調べる
        if disntace <= continue_distance:
           #found_judge = True
           if mec is None:
               mec = [mec_set(mecs[m].name, disntace)]
           else:
               mec.append(mec_set(mecs[m].name, disntace))

    # カバー範囲内のMECを見つけた時
    if mec is not None:
            # デバイスとの距離が近いMECを昇順でソートする
            tmp_mecs = sorted(mec, key=lambda m: m.way, reverse=False)
            print(tmp_mecs)
            array_num = len(tmp_mecs)
            # tmp_mecsを元に、returnするために必要なMEC群を作成する。
            sorted_mecs = None
            for i in range(array_num):
                if sorted_mecs is None:
                    sorted_mecs = [search_mec(mecs, tmp_mecs[i].ID)]
                    sorted_mecs[0]._sorted_flag = True
                else:
                    sorted_mecs.append(search_mec(mecs, tmp_mecs[i].ID))
                    sorted_mecs[i]._sorted_flag = True

            # ソートしたデータの長さを取得
            # ループ短縮用
            sort_finished_index = len(sorted_mecs)
            # ソートしていないMECを追加する。
            sorted_mecs = adding_mec(mecs, sorted_mecs)
            print(sorted_mecs)
            #check_mec_num(sorted_mecs)
            #check_mec_index(sorted_mecs)
            return True, sorted_mecs, sort_finished_index
    else:
        return False, mecs, 0

def check_mec_num(mecs:MEC_servers):
    mec_num = len(mecs)
    if mec_num != 548:
        sys.exit()

def check_mec_index(mecs:MEC_servers):
    mec_num = len(mecs)
    lost = [False] * mec_num
    for s in range(mec_num):
        for m in range(mec_num):
            if mecs[m].name == s + 1:
                break
        if m == mec_num:
            lost[s] = True
    if lost.count(True) == 0:
        return True
    else:
        print(lost.count)
        sys.exit()
        return False

# ソートしているMEC以外を追加するメソッド
# MEC全体の数を変えないための処理
def adding_mec(mecs: MEC_servers, sorted_mecs: MEC_servers):
    mec_num = len(mecs)
    sorted_mecs_num = len(sorted_mecs)
    for sm in range(sorted_mecs_num):
        for m in range(mec_num):
            # もし同じ名前なら
            if mecs[m].name == sorted_mecs[sm].name:
                # 同じMECの名前のところにコピー
                mecs[m] = sorted_mecs[sm]
                #mecs[m]._sorted_flag = True
                # 入れ替え先のインデックスを取得
                f_index = search_mec_index(mecs, sorted_mecs[sm].name)
                # 順番を入れ替え
                mecs[sm], mecs[f_index] = mecs[f_index], mecs[sm]
                break
    return mecs

# MECの並びをリセットするメソッド
def reset_sorted_mec(mecs:MEC_servers):
    mec_num = len(mecs)
    for m in range(mec_num):
        mecs[m]._sorted_flag = False
    return mecs

# 見つけたいMECの名前からMECを見つけてMECインスタンスそのものを返すメソッド
def search_mec(mecs:MEC_servers, mec_name):
    mec_num = len(mecs)
    for m in range(mec_num):
        if mecs[m].name == mec_name:
            return mecs[m]

# 見つけたいMECの名前からMECを見つけてMECのインデックスを返すメソッド
def search_mec_index(mecs:MEC_servers, mec_name):
    mec_num = len(mecs)
    for m in range(mec_num):
        if mecs[m].name == mec_name:
            return m
    return None

# 処理が被っている
def mec_index_search(mecs:MEC_servers, device:Device):
    mec_num = len(mecs)
    for m in range(mec_num):
        if device.mec_name == mecs[m].name:
            return m
            break

# 移動経路優先割り当て
def priority_allocation(mecs:MEC_servers, device:Device, plan_index, time, sort_finish_index):
    mec_num = len(mecs)
    allocated_mec_id = 0
    device_flag = False
    # デバイスが稼働時間内かチェック
    if check_between_time(device, time) == True:
        # 優先度順に割り当てられているMECに割り当て処理
        for m in range(sort_finish_index):
            if (mecs[m].check_resource(device.use_resource) == True) and (mecs[m].resource > 0) and (plan_index < len(device.plan)):
                device_flag, allocated_mec_id = mode_adjustment(mecs, m, device, time)
                print("allocation judge", device_flag, "mec_num", len(mecs))
                if device_flag == True:
                    return True, allocated_mec_id
    #print(device_flag)
    # 割り当て失敗した場合
    print("failed priority allocation")
    return False, allocated_mec_id

def mode_adjustment(mecs:MEC_servers, mec_index, device: Device, time):
    #plan_index = device.plan_index
    #previous_index = mec_index_search(mecs, device)
    current_id = mecs[mec_index].name
    print("割り振るMEC_ID", current_id, "前に割り振ったMEC_ID", device.mec_name)
    mec_index = search_mec_index(mecs, current_id)

    if (current_id == device.mec_name):
        print("KEEP")
        # デバイスをkeepモードにセット
        device.set_mode = "keep"
        # デバイスに割り振るMECの名前を保存
        device.mec_name = mecs[mec_index].name
        # MECに割り当てられたデバイスを追加
        mecs[mec_index].add_having_device(time)
        # MECのリソースを保存
        mecs[mec_index].save_resource(time)
        device.switch_lost_flag = False
        # 割り当てるMECを保存
        current_id = mecs[mec_index].name
        # ホップ数加算
        #hop_calc(device, mecs, mec_index, time)
        keep_hop(device)
        # 割り当て先のMECの管理する集約局を保存
        device._aggregation_name = mecs[mec_index].aggregation_station
        # 割り当て回数を加算
        mecs[mec_index].add_allocation_count(time)
        # keep処理の回数を加算
        mecs[mec_index]._keep_count = mecs[mec_index]._keep_count + 1

        return True, current_id
    # 切替&切替先を見つけている時
    elif current_id != device.mec_name and check_add_device(device, time) == False and device.mec_name != [] and device.mec_name is not None:
        # リソースを増やす
        previous_index = search_mec_index(mecs, device.mec_name)
        print("DECREASE(main)")
        device.set_mode = "decrease"
        print(previous_index, device.mec_name)
        print("増やす前のMECのID", device.mec_name, mecs[previous_index].name)
        print("増やす前のリソース", mecs[previous_index].resource)
        #print(previous_index)
        mecs[previous_index].custom_resource_adjustment(device, time)
        mecs[previous_index].save_resource(time)

        print("ADD")
        print("減らす前のID", mecs[mec_index].name)
        print("減らす前のリソース", mecs[mec_index].resource)
        print(mec_index, previous_index)
        device.set_mode = "add"
        device.mec_name = mecs[mec_index].name

        mecs[mec_index].add_having_device(time)
        mecs[mec_index].custom_resource_adjustment(device, time)
        mecs[mec_index].save_resource(time)
        print("減らした後のリソース", mecs[previous_index].resource)
        device.switch_lost_flag = False
        current_id = mecs[mec_index].name

        # 新規追加
        hop_calc(device, mecs[mec_index], time)
        device._aggregation_name = mecs[mec_index].aggregation_station
        return True, current_id

    # 新規割り当て
    #elif current_id != device.mec_name and check_add_device(device, time) == True and device._first_flag == True:
    else:
        print("ADD")
        device.set_mode = "add"
        device.mec_name = mecs[mec_index].name
        mecs[mec_index].add_having_device(time)
        # 新規追加
        hop_calc(device, mecs[mec_index], time)
        device._aggregation_name = mecs[mec_index].aggregation_station
        mecs[mec_index].custom_resource_adjustment(device, time)
        mecs[mec_index].save_resource(time)
        device.switch_lost_flag = False
        current_id = mecs[mec_index].name

        return True, current_id

    return False, 1

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
"""
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

            # 追加項目
            keep_hop(device)
            device._aggregation_name = mecs[mec_index].aggregation_station
            mecs[mec_index].add_allocation_count(time)
            mecs[mec_index]._keep_count = mecs[mec_index]._keep_count + 1

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

            # 新規追加
            hop_calc(device, mecs[mec_index], time)
            device._aggregation_name = mecs[mec_index].aggregation_station

            return True, current_id

        # 新規割り当て or lost時からの割り当て
        elif device_flag == True and current_id != device.mec_name and check_add_device(device, time) == True:
            #print("ADD")
            device.set_mode = "add"
            device.mec_name = mecs[mec_index].name
            mecs[mec_index].add_having_device(time)
            device.add_hop_count()

            # 追加
            if device._first_flag == True:
                # 新規追加
                hop_calc(device, mecs[mec_index], time)
                device._aggregation_name = mecs[mec_index].aggregation_station

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
"""