from simulator.utility.data import input_data_from_file
from simulator import setting
import os


if setting.run_setting is True:
    path = setting.inputdata_file
else:
    while True:
        path = input("inputdata: ")
        path = setting.inputdata_directory + path
        if os.path.exists(path):
            break
        if path == "quit":
            exit()
        print("No such file or directory.", path)
    data = input_data_from_file(path)
    atcs = data["AllTimeCloudlets"]
    ds = data["Devices"]
    if data["header"] is not None:
        for k in data["header"].keys():
            try:
                print(k + ":", data["header"][k])
            except KeyError:
                print(k + ": KeyError")