"""
「プログラムの概要」
シミュレータの実行ファイル
「プログラムの手順」
1. モジュールの読み込み
2. アルゴリズムファイルと使用するinputdataファイルの指定
3. シュミレータの実行
"""
from simulator.main import simulation
from simulator import setting

if setting.run_setting is True:
    alg = setting.allocation_algorithm
    path = setting.inputdata_file
else:
    alg = "simple_use_plan_07" #使用するアルゴリズムの指定
    path = "inputdata_fk-ap3-cn-dn-kyo-d50-1.data" #使用するinputdataの設定
    print("algorithm", alg)
    print("inputdata", path)
    simulation(algorithm=alg, inputdata_file=path, max_hop=0, congestion_scope=4) #シュミレータの実行