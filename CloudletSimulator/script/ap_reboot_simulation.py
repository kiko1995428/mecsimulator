from CloudletSimulator.script.nearest_simulation import nearest_simulation
from CloudletSimulator.script.continue_nearest_simulation import continue_nearest_simulation
from CloudletSimulator.script.continue_priority_simulation import continue_priority_simulation
from CloudletSimulator.simulator.convenient_function.line_notify import LINE_notify
from CloudletSimulator.dataset.congestion_set import make_congestion_binary
# パラメータ
# system_end_time = 4736
system_time = 1000
# device_num = 1948
device_num = 800
search_distance = 1000
MEC_resource = 100


LINE_notify("デバイス少なめ")
#LINE_notify("making congestion binary")
#make_congestion_binary(system_time, 800, MEC_resource, search_distance)

LINE_notify("混雑度順＋最近傍")
path_w = "/Users/sugimurayuuki/Desktop/mecsimulator/CloudletSimulator/simulation_result/ap_reboot/R_less_nearest.csv"
nearest_simulation(system_time, device_num, MEC_resource, 0, path_w)

LINE_notify("混雑度順＋継続割り当て＋最近傍")
path_w = "/Users/sugimurayuuki/Desktop/mecsimulator/CloudletSimulator/simulation_result/ap_reboot/R_less_continue_nearest_result.csv"
continue_distance = 200
continue_nearest_simulation(system_time, device_num, MEC_resource, continue_distance, 0, path_w)

LINE_notify("混雑度順＋継続割り当て＋経路予測")
path_w = "/Users/sugimurayuuki/Desktop/mecsimulator/CloudletSimulator/simulation_result/ap_reboot/R_less_continue_priority_result.csv"
continue_distance = 200
f_time = 2
continue_priority_simulation(system_time, device_num, MEC_resource, continue_distance, f_time, 0, path_w)

"""
LINE_notify("デバイス普通")
device_num = 300
LINE_notify("到着順＋最近傍")
path_w = "/Users/sugimurayuuki/Desktop/mecsimulator/CloudletSimulator/simulation_result/ap_reboot/R_normal_nearest.csv"
nearest_simulation(system_time, device_num, MEC_resource, 2, path_w)

LINE_notify("到着順＋継続割り当て＋最近傍")
path_w = "/Users/sugimurayuuki/Desktop/mecsimulator/CloudletSimulator/simulation_result/ap_reboot/R_normal_continue_nearest_result.csv"
continue_distance = 300
continue_nearest_simulation(system_time, device_num, MEC_resource, continue_distance, 2, path_w)

LINE_notify("到着順＋継続割り当て＋経路予測")
path_w = "/Users/sugimurayuuki/Desktop/mecsimulator/CloudletSimulator/simulation_result/ap_reboot/R_normal_continue_priority_result.csv"
continue_distance = 300
f_time = 2
continue_priority_simulation(system_time, device_num, MEC_resource, continue_distance, f_time, 2, path_w)

LINE_notify("デバイス多い")
device_num = 500
LINE_notify("到着順＋最近傍")
path_w = "/Users/sugimurayuuki/Desktop/mecsimulator/CloudletSimulator/simulation_result/ap_reboot/R_many_nearest.csv"
nearest_simulation(system_time, device_num, MEC_resource, 2, path_w)

LINE_notify("到着順＋継続割り当て＋最近傍")
path_w = "/Users/sugimurayuuki/Desktop/mecsimulator/CloudletSimulator/simulation_result/ap_reboot/R_many_continue_nearest_result.csv"
continue_distance = 300
continue_nearest_simulation(system_time, device_num, MEC_resource, continue_distance, 2, path_w)

LINE_notify("到着順＋継続割り当て＋経路予測")
path_w = "/Users/sugimurayuuki/Desktop/mecsimulator/CloudletSimulator/simulation_result/ap_reboot/R_many_continue_priority_result.csv"
continue_distance = 300
f_time = 2
continue_priority_simulation(system_time, device_num, MEC_resource, continue_distance, f_time, 2, path_w)

"""

LINE_notify("シミュレーション完了")
