from CloudletSimulator.script.nearest_simulation import nearest_simulation
from CloudletSimulator.script.continue_nearest_simulation import continue_nearest_simulation
from CloudletSimulator.script.continue_priority_simulation import continue_priority_simulation
from CloudletSimulator.simulator.convenient_function.line_notify import LINE_notify
from CloudletSimulator.dataset.congestion_set2 import make_congestion_binary


# パラメータ
# 時間4736, デバイス1948
system_time = 200
device_num = 100
MEC_resource = 5
continue_distance = 1000
#LINE_notify("デバイス少なめ")
#LINE_notify("making congestion binary")
make_congestion_binary(system_time, device_num, MEC_resource, continue_distance)

#LINE_notify("到着順")
path_w = "/Users/sugimurayuuki/Desktop/mecsimulator/CloudletSimulator/simulation_result/hop/device_less_arrival.csv"
#neaest_simulation(4736, 1948, path_w)
nearest_simulation(system_time, MEC_resource, device_num, 0, path_w)

#LINE_notify("リソース順")
path_w = "/Users/sugimurayuuki/Desktop/mecsimulator/CloudletSimulator/simulation_result/hop/device_less_resource.csv"
nearest_simulation(system_time, MEC_resource, device_num, 1,  path_w)

#LINE_notify("混雑度順")
path_w = "/Users/sugimurayuuki/Desktop/mecsimulator/CloudletSimulator/simulation_result/hop/device_less_congestion.csv"
nearest_simulation(system_time, MEC_resource, device_num, 2, path_w)

"""
system_time = 1000
device_num = 500
MEC_resource = 10
#LINE_notify("making congestion binary")
make_congestion_binary(system_time, device_num, MEC_resource, continue_distance)

LINE_notify("デバイス普通")
LINE_notify("到着順")
path_w = "/Users/sugimurayuuki/Desktop/mecsimulator/CloudletSimulator/simulation_result/hop/device_normal_arrival.csv"
#nearest_simulation(system_time, MEC_resource, device_num, 0, path_w)

LINE_notify("リソース順")
path_w = "/Users/sugimurayuuki/Desktop/mecsimulator/CloudletSimulator/simulation_result/hop/device_normal_resource.csv"
#neaest_simulation(4736, 1948, path_w)
#nearest_simulation(system_time, MEC_resource, device_num, 1,  path_w)

LINE_notify("混雑度順")
path_w = "/Users/sugimurayuuki/Desktop/mecsimulator/CloudletSimulator/simulation_result/hop/device_normal_congestion.csv"
#neaest_simulation(4736, 1948, path_w)
#nearest_simulation(100, 100, 2, path_w)
nearest_simulation(system_time, MEC_resource, device_num, 2, path_w)

LINE_notify("デバイス多め")
# パラメータ
system_time = 1000
device_num = 800
MEC_resource = 10
#LINE_notify("making congestion binary")
make_congestion_binary(system_time, device_num, MEC_resource, continue_distance)


LINE_notify("到着順")
path_w = "/Users/sugimurayuuki/Desktop/mecsimulator/CloudletSimulator/simulation_result/hop/device_many_arrival.csv"
#nearest_simulation(system_time, MEC_resource, device_num, 0, path_w)

LINE_notify("リソース順")
path_w = "/Users/sugimurayuuki/Desktop/mecsimulator/CloudletSimulator/simulation_result/hop/device_many_resource.csv"
#nearest_simulation(system_time, MEC_resource, device_num, 1,  path_w)

LINE_notify("混雑度順")
path_w = "/Users/sugimurayuuki/Desktop/mecsimulator/CloudletSimulator/simulation_result/hop/device_many_congestion.csv"
nearest_simulation(system_time, MEC_resource, device_num, 2, path_w)

#リソース

# パラメータ
# 時間4736, デバイス1948

MEC_resource = 5
LINE_notify("リソース少なめ")
make_congestion_binary(system_time, device_num, MEC_resource, 500)


#LINE_notify("到着順")
path_w = "/Users/sugimurayuuki/Desktop/mecsimulator/CloudletSimulator/simulation_result/hop/R_less_arrival.csv"
#neaest_simulation(4736, 1948, path_w)
nearest_simulation(system_time, MEC_resource, device_num, 0, path_w)

#LINE_notify("リソース順")
path_w = "/Users/sugimurayuuki/Desktop/mecsimulator/CloudletSimulator/simulation_result/hop/R_less_resource.csv"
nearest_simulation(system_time, MEC_resource, device_num, 1,  path_w)

#LINE_notify("混雑度順")
path_w = "/Users/sugimurayuuki/Desktop/mecsimulator/CloudletSimulator/simulation_result/hop/R_less_congestion.csv"
nearest_simulation(system_time, MEC_resource, device_num, 2, path_w)


MEC_resource = 30
#LINE_notify("making congestion binary")
#make_congestion_binary(system_time, MEC_resource, device_num, 1000)

LINE_notify("リソース普通")
LINE_notify("到着順")
path_w = "/Users/sugimurayuuki/Desktop/mecsimulator/CloudletSimulator/simulation_result/hop/R_normal_arrival.csv"
nearest_simulation(system_time, MEC_resource, device_num, 0, path_w)

LINE_notify("リソース順")
path_w = "/Users/sugimurayuuki/Desktop/mecsimulator/CloudletSimulator/simulation_result/hop/R_normal_resource.csv"
#neaest_simulation(4736, 1948, path_w)
nearest_simulation(system_time, MEC_resource, device_num, 1,  path_w)

LINE_notify("混雑度順")
path_w = "/Users/sugimurayuuki/Desktop/mecsimulator/CloudletSimulator/simulation_result/hop/R_normal_congestion.csv"
#neaest_simulation(4736, 1948, path_w)
#nearest_simulation(100, 100, 2, path_w)
nearest_simulation(system_time, MEC_resource, device_num, 2, path_w)

LINE_notify("リソース多め")
system_time = 1000
device_num = 500
MEC_resource = 50
LINE_notify("simulation start")
#LINE_notify("making congestion binary")
#make_congestion_binary(system_time, MEC_resource, device_num, 1000)

LINE_notify("到着順")
path_w = "/Users/sugimurayuuki/Desktop/mecsimulator/CloudletSimulator/simulation_result/hop/R_many_arrival.csv"
nearest_simulation(system_time, MEC_resource, device_num, 0, path_w)

LINE_notify("リソース順")
path_w = "/Users/sugimurayuuki/Desktop/mecsimulator/CloudletSimulator/simulation_result/hop/R_many_resource.csv"
nearest_simulation(system_time, MEC_resource, device_num, 1,  path_w)

LINE_notify("混雑度順")
path_w = "/Users/sugimurayuuki/Desktop/mecsimulator/CloudletSimulator/simulation_result/hop/R_many_congestion.csv"
nearest_simulation(system_time, MEC_resource, device_num, 2, path_w)

LINE_notify("シミュレーション完了")
"""