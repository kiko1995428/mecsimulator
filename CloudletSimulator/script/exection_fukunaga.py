from simulator.main import simulation
from simulator import setting

if setting.run_setting is True:
    alg = setting.allocation_algorithm
    path = setting.inputdata_file
else:
    alg = "simple_use_plan_02"
    path = "fukunaga-4.data"
    print("algorithm", alg)
    print("inputdata", path)
    simulation(algorithm=alg, inputdata_file=path, max_hop=2, congestion_scope=0)
