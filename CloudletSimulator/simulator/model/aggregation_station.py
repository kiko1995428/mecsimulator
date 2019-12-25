from CloudletSimulator.simulator.model.edge_server import MEC_servers, MEC_server

def set_aggregation_station(mecs:MEC_servers):
    """
    MECを管理する集約局をセットするメソッド
    :param mecs: MEC群
    """
    mec_num = len(mecs)
    #central_lat = 34.663377
    central_lat = 34.664405
    #central_lon = 133.917336
    central_lon = 133.91157
    for m in range(mec_num):
        # 左下
        if mecs[m].lat <= central_lat and mecs[m].lon <= central_lon:
            mecs[m].set_aggregation_station(1)
        # 右下
        elif mecs[m].lat <= central_lat and central_lon <= mecs[m].lon:
            mecs[m].set_aggregation_station(2)
        # 左上
        elif central_lat <= mecs[m].lat and mecs[m].lon <= central_lon:
            mecs[m].set_aggregation_station(3)
        # 右上
        elif central_lat <= mecs[m].lat and central_lon <= mecs[m].lon:
       # else:
            mecs[m].set_aggregation_station(4)
