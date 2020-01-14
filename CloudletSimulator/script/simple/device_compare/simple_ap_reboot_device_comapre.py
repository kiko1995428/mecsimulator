from CloudletSimulator.script.simple.simple_nearest_onely_simulation import nearest_simulation
from CloudletSimulator.script.simple.simple_continue_priority_simulation import continue_priority_simulation
from CloudletSimulator.script.simple.simple_continue_nearest_simulation import continue_nearest_simulation
from CloudletSimulator.dataset.simple_congestion_set1 import make_congestion_binary
from CloudletSimulator.simulator.convenient_function.line_notify import LINE_notify

# パラメータ
# system_end_time = 4736
system_time = 100
# device_num = 1948
device_num = 100
search_distance = 500
MEC_resource = 40
how_compare = "ap_reboot"

LINE_notify("デバイス少なめ")
make_congestion_binary(system_time, device_num, MEC_resource, search_distance)
LINE_notify("混雑度順＋最近傍")
path_w = "/Users/sugimurayuuki/Desktop/mecsimulator/CloudletSimulator/simulation_result/ap_reboot/test.csv"
nearest_simulation(system_time, MEC_resource, device_num, 2, path_w, how_compare)
LINE_notify("混雑度順＋継続割り当て＋最近傍")
path_w = "/Users/sugimurayuuki/Desktop/mecsimulator/CloudletSimulator/simulation_result/ap_reboot/test.csv"
continue_distance = 1000
#continue_nearest_simulation(system_time,  MEC_resource, device_num, continue_distance, 2, path_w)
LINE_notify("混雑度順＋継続割り当て＋経路予測")
path_w = "/Users/sugimurayuuki/Desktop/mecsimulator/CloudletSimulator/simulation_result/ap_reboot/test.csv"
continue_distance = 1000
f_time = 3
continue_priority_simulation(system_time,  MEC_resource, device_num, continue_distance, f_time, 2, path_w, how_compare)
"""
LINE_notify("デバイス普通")
device_num = 500
make_congestion_binary(system_time, device_num, MEC_resource, search_distance)
LINE_notify("到着順＋最近傍")
path_w = "/Users/sugimurayuuki/Desktop/mecsimulator/CloudletSimulator/simulation_result/ap_reboot/R_normal_nearest.csv"
nearest_simulation(system_time,  MEC_resource, device_num, 2, path_w, how_compare)
LINE_notify("到着順＋継続割り当て＋最近傍")
path_w = "/Users/sugimurayuuki/Desktop/mecsimulator/CloudletSimulator/simulation_result/ap_reboot/R_normal_continue_nearest_result.csv"
continue_distance = 1000
continue_nearest_simulation(system_time, MEC_resource, device_num,  continue_distance, 2, path_w, how_compare)
LINE_notify("到着順＋継続割り当て＋経路予測")
path_w = "/Users/sugimurayuuki/Desktop/mecsimulator/CloudletSimulator/simulation_result/ap_reboot/R_normal_continue_priority_result.csv"
continue_distance = 1000
f_time = 3
continue_priority_simulation(system_time, MEC_resource, device_num,  continue_distance, f_time, 2, path_w, how_compare)

LINE_notify("デバイス多い")
device_num = 1000
make_congestion_binary(system_time, device_num, MEC_resource, search_distance)
LINE_notify("到着順＋最近傍")
path_w = "/Users/sugimurayuuki/Desktop/mecsimulator/CloudletSimulator/simulation_result/ap_reboot/R_many_nearest.csv"
nearest_simulation(system_time, MEC_resource, device_num, 2, path_w, how_compare)
LINE_notify("到着順＋継続割り当て＋最近傍")
path_w = "/Users/sugimurayuuki/Desktop/mecsimulator/CloudletSimulator/simulation_result/ap_reboot/R_many_continue_nearest_result.csv"
continue_distance = 1000
continue_nearest_simulation(system_time, MEC_resource, device_num,  continue_distance, 2, path_w, how_compare)
LINE_notify("到着順＋継続割り当て＋経路予測")
path_w = "/Users/sugimurayuuki/Desktop/mecsimulator/CloudletSimulator/simulation_result/ap_reboot/R_many_continue_priority_result.csv"
continue_distance = 1000
f_time = 3
continue_priority_simulation(system_time, MEC_resource, device_num, continue_distance, f_time, 2, path_w, how_compare)
"""
LINE_notify("シミュレーション完了")