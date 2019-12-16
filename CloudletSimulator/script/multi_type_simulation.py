from CloudletSimulator.script.nearest_simulation import nearest_simulation
from CloudletSimulator.script.continue_nearest_simulation import continue_nearest_simulation
from CloudletSimulator.script.continue_priority_simulation import continue_priority_simulation
from CloudletSimulator.simulator.convenient_function.line_notify import LINE_notify
from CloudletSimulator.dataset.congestion_set import make_congestion_binary

LINE_notify("simulation start")
LINE_notify("making congestion binary")
make_congestion_binary(100, 100)

LINE_notify("nearest simulation start")
path_w = "/Users/sugimurayuuki/Desktop/mecsimulator/CloudletSimulator/simulation_result/test_result.csv"
#neaest_simulation(4736, 1948, path_w)
nearest_simulation(100, 100, path_w)

LINE_notify("continue + nearest simulation start")
path_w = "/Users/sugimurayuuki/Desktop/mecsimulator/CloudletSimulator/simulation_result/test_result.csv"
continue_distance = 500
#continue_nearest_simulation(4736, 1948, continue_distance, path_w)
continue_nearest_simulation(100, 100, continue_distance, path_w)

LINE_notify("シミュレーション完了")


#continue_nearest_simulation(100, 100, 500, path_w)
#continue_priority_simulation(100, 100, 300, 30, path_w)

#print("SECOND SIMULATION")
#path_w = "/Users/sugimurayuuki/Desktop/mecsimulator/CloudletSimulator/simulation_result/prototype_result2.csv"
#edge_simulation(200, 200, path_w)

# シミュレーション完了をLINE通知してくれる
# シミュレーション結果を添付することも可能
LINE_notify("シミュレーション完了")