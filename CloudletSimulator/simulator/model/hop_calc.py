from CloudletSimulator.simulator.model.edge_server import MEC_servers, MEC_server
from CloudletSimulator.simulator.model.device import Device

def mec_compare(device:Device, mec: MEC_server):
    # もし直前に割り当てたMECと今割り当てられるMECが同じ場合
    if device._aggregation_name == mec._aggregation_name:
        return True
    else:
        return False

def mec_index_search(device:Device, mecs: MEC_servers):
    mec_num = len(mecs)
    for m in range(mec_num):
        if device._old_mec_name == mecs[m].name:
            return m
    return False

def hop_calc(device:Device, mec: MEC_server, time):
    # ホップ数計算
    # 最初の割り当て
    if device._first_flag == True:
        device._hop = [1]
        device._first_flag = False
    # 切替成功
    else:
        mec.add_reboot_count(time)
        # 集約局が同一の時
        if mec_compare(device, mec) == False:
            device._hop.append(3)
        # 集約曲が違う時
        else:
            device._hop.append(5)

def keep_hop(device:Device):
    device._hop.append(1)
