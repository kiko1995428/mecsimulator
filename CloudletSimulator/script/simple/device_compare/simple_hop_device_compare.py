from CloudletSimulator.script.simple.simple_nearest_onely_simulation import nearest_simulation
from CloudletSimulator.dataset.simple_congetion_set2 import make_congestion_binary
from CloudletSimulator.simulator.convenient_function.line_notify import LINE_notify
LINE_notify("デバイス少なめ")
# パラメータ
# 時間4736, デバイス1948
system_time = 100
device_num = 100
MEC_resource = 50
continue_distance = 500
how_compare = "hop"

LINE_notify("到着順")
path_w = "/Users/sugimurayuuki/Desktop/mecsimulator/CloudletSimulator/simulation_result/hop/test.csv"
nearest_simulation(system_time, MEC_resource, device_num, 0, path_w, how_compare)
LINE_notify("リソース順")
path_w = "/Users/sugimurayuuki/Desktop/mecsimulator/CloudletSimulator/simulation_result/hop/test.csv"
nearest_simulation(system_time, MEC_resource, device_num, 1,  path_w, how_compare)
LINE_notify("混雑度順")
make_congestion_binary(system_time, device_num, MEC_resource, continue_distance)
path_w = "/Users/sugimurayuuki/Desktop/mecsimulator/CloudletSimulator/simulation_result/hop/test.csv"
nearest_simulation(system_time, MEC_resource, device_num, 2, path_w, how_compare)
"""
LINE_notify("デバイス普通")
device_num = 500
LINE_notify("到着順")
path_w = "/Users/sugimurayuuki/Desktop/mecsimulator/CloudletSimulator/simulation_result/hop/device_normal_arrival.csv"
nearest_simulation(system_time, MEC_resource, device_num, 0, path_w, how_compare)
LINE_notify("リソース順")
path_w = "/Users/sugimurayuuki/Desktop/mecsimulator/CloudletSimulator/simulation_result/hop/device_normal_resource.csv"
nearest_simulation(system_time, MEC_resource, device_num, 1,  path_w, how_compare)
LINE_notify("混雑度順")
make_congestion_binary(system_time, device_num, MEC_resource, continue_distance)
path_w = "/Users/sugimurayuuki/Desktop/mecsimulator/CloudletSimulator/simulation_result/hop/device_normal_congestion.csv"
nearest_simulation(system_time, MEC_resource, device_num, 2, path_w, how_compare)

LINE_notify("デバイス多め")
device_num = 1000
LINE_notify("到着順")
path_w = "/Users/sugimurayuuki/Desktop/mecsimulator/CloudletSimulator/simulation_result/hop/device_many_arrival.csv"
nearest_simulation(system_time, MEC_resource, device_num, 0, path_w, how_compare)
LINE_notify("リソース順")
path_w = "/Users/sugimurayuuki/Desktop/mecsimulator/CloudletSimulator/simulation_result/hop/device_many_resource.csv"
nearest_simulation(system_time, MEC_resource, device_num, 1,  path_w, how_compare)
LINE_notify("混雑度順")
make_congestion_binary(system_time, device_num, MEC_resource, continue_distance)
path_w = "/Users/sugimurayuuki/Desktop/mecsimulator/CloudletSimulator/simulation_result/hop/device_many_congestion.csv"
nearest_simulation(system_time, MEC_resource, device_num, 2, path_w, how_compare)
"""
LINE_notify("シミュレーション完了")
