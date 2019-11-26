from CloudletSimulator.simulator.model.edge_server import MEC_servers, check_add_device,MEC_server
from CloudletSimulator.simulator.model.device import Device
from geopy.distance import vincenty

def nearest_search(device:Device, mec:MEC_servers, plan_index, cover_range, time):
    #data = len(mec)
    data = 100
    distance =[None] * data
    device_lat = float(device.plan[plan_index].y)
    device_lon = float(device.plan[plan_index].x)
    device_position = (device_lat, device_lon)

    for m in range(data):
        position = (mec[m].lat, mec[m].lon)
        if  mec[m].check_resource(device.use_resource) == True:
            distance[m] = vincenty(position, device_position).miles * 1609.34
        else:
            distance[m] = None
        #distance[m] = distance_calc(float(device.plan[plan_index].y),
                                     #float(device.plan[plan_index].x), mec[m].lat, mec[m].lon)
    ans_id = distance.index(min(distance))
    if min(distance) <= cover_range:
        print(device.mec_name)
        ans_id = mec[ans_id].name
        print(mec[ans_id].name, device.mec_name)
        if mec[ans_id].name == device.mec_name:
            print(device.plan[plan_index])
            mec[ans_id]._mode == "keep"
            print("KEEP", plan_index)
            device.mec_name = mec[ans_id].name
            mec[ans_id].append_having_device(time, device)

        elif mec[ans_id].name != device.mec_name and check_add_device(device, time)==False:
            # リソースを増やす
            mec[ans_id] == "decrease"
            print("DECREASE")
            mec[ans_id].resource_adjustment(device, mec[ans_id]._mode)
            # リソースを減らす
            mec[ans_id]._mode = "add"
            mec[ans_id].resource_adjustment(device, mec[ans_id]._mode)
            device.mec_name = device.mec_name = mec[ans_id].name
            mec[ans_id].append_having_device(time, device)

        #elif check_add_device(device, time)==False:
            # リソースを減らす
            #mec[ans_id]._mode == "add"
            #mec[ans_id].resource_adjustment(device, mec[ans_id]._mode)
            #device.mec_name = ans_id
        else:
            # リソースを減らす
            mec[ans_id]._mode == "add"
            mec[ans_id].resource_adjustment(device, mec[ans_id]._mode)
            device.mec_name = mec[ans_id].name
            device.mec_name = mec[ans_id].name
            mec[ans_id].append_having_device(time, device)
        return True, ans_id
    else:
        return False, ans_id

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
