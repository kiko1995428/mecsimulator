from CloudletSimulator.simulator.model.edge_server import MEC_servers
import math
from math import radians, cos, sin, asin, sqrt, atan2

def delete_mec(mecs: MEC_servers):
    mec_num = len(mecs)
    another_mecs = mecs
    check_flag = False
    m = 0
    while(check_flag == False):
        sm = 0
        check_flag2 = False
        while(check_flag2 == False):
            if mecs[m].name != mecs[sm].name:
                distance = distance_calc(mecs[m].lat, mecs[m].lon, mecs[sm].lat, mecs[sm].lon)
                if distance <= 50:
                    mecs.pop(sm)
                    mec_num = len(mecs)
            if sm == mec_num - 1:
                check_flag2 = True
                continue
            sm = sm + 1

        if m == mec_num - 1:
            check_flag = True
            break
        m = m + 1
    return mecs



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

