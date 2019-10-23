"""
「プログラムの概要」
シュミレータの実行時にinputdataやアルゴリズムを元にoutputdata作成する。

"""

import datetime
import os

from simulator import setting
from simulator.evaluation import hops_each_device, hops_each_device_for_hot
from simulator.oldmodels import Point
from simulator.utility.data import allocation_plan_to_csv, input_data_from_file, dictlist_to_csv, get_num_of_change_cloudlet_from_allocation_plan
from simulator.allocation.nearest import *
from simulator.allocation.simple import *
from simulator.allocation.congestion import *
from simulator.allocation.usemovementplan import *
from simulator.utility.data import セルごとの平均ホップ数を出力


def simulation(**kwargs):
    algorithm = kwargs["algorithm"] #引数のアルゴリズム
    inputdata_file = kwargs["inputdata_file"] #引数のinputdata
    data = input_data_from_file(setting.inputdata_directory + inputdata_file) #inputdgataの呼び込み
    atcs = data["AllTimeCloudlets"] #cloudletの３次元モデル
    ds = data["Devices"] #デバイスの基本データ
    # 置き場所
    # reqapp = data[]
    kwargs["atcs"] = atcs #辞書型リストkwargsにatcsを追加
    kwargs["ds"] = ds #辞書型リストにデバイスの基本データを追加
    #inputdataの中のheaderの要素を出力
    if data["header"] is not None:
        for k in data["header"].keys():
            try:
                print(k + ":", data["header"][k])
            except KeyError:
                print(k + ": KeyError")
    print("algorithm:", algorithm)
    print("input:", inputdata_file)
    allocation_plan = eval(algorithm)(kwargs) #allocation_planの返り値Allocation（x, y, hop）
    now = datetime.datetime.today()
    # すごくきたないのであとで改修
    inputdata_file = inputdata_file[0].split(".")[0]
    #print(inputdata_file)

    output_filename = setting.outputdata_directory + inputdata_file + "-" + algorithm + now.strftime("%Y-%m-%d-%H-%M-%S")
    output_data(allocation_plan, output_filename, data)
    セルごとの平均ホップ数を出力(ds, allocation_plan, 30, 30)


def output_data(allocation_plan, output_filename, data, log=True):
    allocation_plan_to_csv(allocation_plan, output_filename + ".csv") #CSV形式で書き込み
    hsed = hops_each_device(allocation_plan, data["header"]["t_length"]) #デバイスごとの各ホップ数を表示する
    migration_num = get_num_of_change_cloudlet_from_allocation_plan(allocation_plan) #cloudleのchange回数（合計と平均）
    dictlist_to_csv(hsed, output_filename + "-hops" + ".csv") #CSV形式で書き込み(デバイスごとの各ホップ数)
    dictlist_to_csv(migration_num, output_filename + "-migrations" + ".csv") #CSV形式で書き込み(cloudleのchange回数（合計と平均）)

    if log:
        for h in hsed["sum"]:
            print(h, end=", ")
        print()
        print("migration avg: {}".format(migration_num["avg"])) #cloudleのchange回数（平均）


if __name__ == "__main__":
    if setting.run_setting is True:
        alg = setting.allocation_algorithm
        path = setting.inputdata_file
    else:
        alg = input("Allocation algorithm: ")
        while True:
            path = input("inputdata: ")
            path = setting.inputdata_directory + path
            if os.path.exists(path):
                break
            print("No such file or directory.", path)
        print("execute simulation")
        simulation(alg, path)
        print("complete!")
