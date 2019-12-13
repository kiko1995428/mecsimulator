from CloudletSimulator.simulator.model.edge_server import MEC_servers, MEC_server

def set_aggregation_station(mecs:MEC_servers):
    mec_num = len(mecs)
    central_lat = 34.663377
    central_lon = 133.917336
    for m in range(mec_num):
        if mecs[m].lat <= central_lat and mecs[m].lon <= central_lon:
            mecs[m].set_aggregation_station(1)
        elif mecs[m].lat <= central_lat and central_lon <= mecs[m].lon:
            mecs[m].set_aggregation_station(2)
        elif central_lat <= mecs[m].lat and mecs[m].lon <= central_lon:
            mecs[m].set_aggregation_station(3)
        else:
            mecs[m].set_aggregation_station(4)
