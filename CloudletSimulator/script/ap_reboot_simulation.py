from CloudletSimulator.script.nearest_simulation import nearest_simulation
from CloudletSimulator.script.continue_nearest_simulation import continue_nearest_simulation
from CloudletSimulator.script.continue_priority_simulation import continue_priority_simulation
from CloudletSimulator.simulator.convenient_function.line_notify import LINE_notify
from CloudletSimulator.dataset.congestion_set import make_congestion_binary
# パラメータ
# system_end_time = 4736
system_time = 500
# device_num = 1948
device_num = 100
search_distance = 1000
MEC_source = 2


LINE_notify("デバイス少なめ")
#LINE_notify("making congestion binary")
#make_congestion_binary(system_time, 500, MEC_source, search_distance)

LINE_notify("混雑度順＋最近傍")
path_w = "/Users/sugimurayuuki/Desktop/mecsimulator/CloudletSimulator/simulation_result/ap_reboot/C_less_nearest.csv"
nearest_simulation(system_time, device_num, MEC_source, 2, path_w)

LINE_notify("混雑度順＋継続割り当て＋最近傍")
path_w = "/Users/sugimurayuuki/Desktop/mecsimulator/CloudletSimulator/simulation_result/ap_reboot/C_less_continue_nearest_result.csv"
continue_distance = 500
continue_nearest_simulation(system_time, device_num, MEC_source, continue_distance, 2, path_w)

LINE_notify("混雑度順＋継続割り当て＋経路予測")
path_w = "/Users/sugimurayuuki/Desktop/mecsimulator/CloudletSimulator/simulation_result/ap_reboot/C_less_continue_priority_result.csv"
continue_distance = 500
f_time = 4
continue_priority_simulation(system_time, device_num, MEC_source, continue_distance, f_time, 2, path_w)

system_time = 500
# device_num = 1948
device_num = 200
search_distance = 1000
MEC_source = 2


LINE_notify("デバイス普通")
#LINE_notify("making congestion binary")
#make_congestion_binary(system_time, device_num, MEC_source, search_distance)

LINE_notify("到着順＋最近傍")
path_w = "/Users/sugimurayuuki/Desktop/mecsimulator/CloudletSimulator/simulation_result/ap_reboot/C_normal_nearest.csv"
nearest_simulation(system_time, device_num, MEC_source, 2, path_w)

LINE_notify("到着順＋継続割り当て＋最近傍")
path_w = "/Users/sugimurayuuki/Desktop/mecsimulator/CloudletSimulator/simulation_result/ap_reboot/C_normal_continue_nearest_result.csv"
continue_distance = 500
continue_nearest_simulation(system_time, device_num, MEC_source, continue_distance, 2, path_w)

LINE_notify("到着順＋継続割り当て＋経路予測")
path_w = "/Users/sugimurayuuki/Desktop/mecsimulator/CloudletSimulator/simulation_result/ap_reboot/C_normal_continue_priority_result.csv"
continue_distance = 500
f_time = 4
continue_priority_simulation(system_time, device_num, MEC_source, continue_distance, f_time, 2, path_w)

system_time = 500
# device_num = 1948
device_num = 500
search_distance = 1000
MEC_source = 2


LINE_notify("デバイス多い")
#LINE_notify("making congestion binary")
#make_congestion_binary(system_time, device_num, MEC_source, search_distance)

LINE_notify("到着順＋最近傍")
path_w = "/Users/sugimurayuuki/Desktop/mecsimulator/CloudletSimulator/simulation_result/ap_reboot/C_many_nearest.csv"
nearest_simulation(system_time, device_num, MEC_source, 2, path_w)

LINE_notify("到着順＋継続割り当て＋最近傍")
path_w = "/Users/sugimurayuuki/Desktop/mecsimulator/CloudletSimulator/simulation_result/ap_reboot/C_many_continue_nearest_result.csv"
continue_distance = 500
continue_nearest_simulation(system_time, device_num, MEC_source, continue_distance, 2, path_w)

LINE_notify("到着順＋継続割り当て＋経路予測")
path_w = "/Users/sugimurayuuki/Desktop/mecsimulator/CloudletSimulator/simulation_result/ap_reboot/C_many_continue_priority_result.csv"
continue_distance = 500
f_time = 4
continue_priority_simulation(system_time, device_num, MEC_source, continue_distance, f_time, 2, path_w)


LINE_notify("シミュレーション完了")
