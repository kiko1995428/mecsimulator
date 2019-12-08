from CloudletSimulator.script.edge_prototype import edge_simulation
from CloudletSimulator.simulator.convenient_function.line_notify import LINE_notify


print("FIRST SIMULATION")
path_w = "/Users/sugimurayuuki/Desktop/mecsimulator/CloudletSimulator/simulation_result/prototype_result.csv"
edge_simulation(100, 200, path_w)
#print("SECOND SIMULATION")
#path_w = "/Users/sugimurayuuki/Desktop/mecsimulator/CloudletSimulator/simulation_result/prototype_result2.csv"
#edge_simulation(200, 200, path_w)

# シミュレーション完了をLINE通知してくれる
# シミュレーション結果を添付することも可能
LINE_notify()