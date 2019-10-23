"""
simulator/utility/data.py
coding          : utf-8
Author          : Kouhei Osaki
Created         : 2017/07/17
Last-Modified   : 2017/07/17
Version         : 1.0.0
Description     : 入出力データに関する有用な関数などを定義している（適当
"""
from simulator.oldmodels import AllTimeCloudlets, Devices, AllocationPlan
from simulator.model.device import Device
from simulator.utility.search import search
import simulator.setting
from typing import Dict, List
import csv
import pickle
import os


def allocation_plan_to_csv(ap: AllocationPlan, file_name: str):
    with open(file_name, "w", newline='') as f:
        writer = csv.writer(f)
        row = []
        for key in ap.keys():
            hops = [key]
            for a in ap[key]:
                if a is not None:
                    hops.append(a.hop)
                else:
                    hops.append(None)
            row.append(hops)

        # avg
        max_t = len(ap[list(ap.keys())[0]])
        sum = [0 for i in range(max_t)]
        num = [0 for i in range(max_t)]
        avg = [0 for i in range(max_t)]
        for key in ap.keys():
            for i in range(max_t):
                if ap[key][i] is not None:
                    hop = ap[key][i].hop
                    if hop != -1:
                        sum[i] += ap[key][i].hop
                        num[i] += 1
        for t in range(max_t):
            if num[t] == 0:
                avg[t] = -1
            else:
                avg[t] = sum[t] / num[t]
        out = ["avg"]
        out.extend(avg)
        row.append(out)

        #num
        num = [0 for i in range(max_t)]
        for key in ap.keys():
            for t in range(max_t):
                if ap[key][t] is not None:
                    num[t] += 1
        out = ["num"]
        out.extend(num)
        row.append(out)

        sucess = [0 for i in range(max_t)]
        for key in ap.keys():
            for t in range(max_t):
                if ap[key][t] is not None and ap[key][t].hop >= 0:
                    sucess[t] += 1
        out = ["sucess"]
        out.extend(sucess)
        row.append(out)

        writer.writerows(row) #CSV書き込み


def get_num_of_change_cloudlet_from_allocation_plan(ap: AllocationPlan):
    ret = {}
    allcount = 0
    for key in ap.keys():
        prev = None
        count = 0
        ccount = 0
        for al in ap[key]:
            if al is not None:
                ccount += 1
                now = (al.x, al.y)
                if prev != now:
                    count += 1
                prev = (al.x, al.y)
        ret[key] = [count / ccount]
        allcount += (count / ccount)
    ret["sum"] = [allcount]
    ret["avg"] = [allcount / len(ap.keys())]
    return ret


def dictlist_to_csv(d: Dict[str, List[int]], filename: str) -> None:
    with open(filename, "w", newline='') as f:
        writer = csv.writer(f)
        rows = [] #list
        row = []
        ks = d.keys() #alocation_planのリスト
        for k in ks:
            row = [k]
            for data in d[k]:
                row.append(data)
            rows.append(row)
        writer.writerows(rows) #csv形式で書き込み


def input_data_from_file(path: str) -> Dict:
    """
    devicesをファイルから読み取る
    :param path: 読み取るファイル名
    :return: (AlltimeCloudlets, Devices)
    """
    f = open(path, 'rb')
    data = pickle.load(f)
    f.close()
    return data


def input_data_to_file(header: Dict, atcs: AllTimeCloudlets, ds: Devices, group_name: str="default") -> str:
    """
    デバイス集合をファイルへ書き込む
    :param header: 辞書型の入力データ情報 例{"x_length": 10, "y_length":10}
    :param atcs: AllTimeCloudlets
    :param ds: Devices
    :param group_name: 入力データ種別
    :return: 出力パス
    """
    num = 1
    while True:
        path = simulator.setting.inputdata_directory + group_name + "-" + str(num) + ".data"
        if not os.path.exists(path):
            break
        num = num + 1
    if header is None:
        header = {
            "t_length": len(atcs),
            "y_length": len(atcs[0]),
            "x_length": len(atcs[0][0]),
            "d_num": len(ds)
        }
    data = {"header": header, "AllTimeCloudlets": atcs, "Devices": ds}
    f = open(path, 'wb')
    pickle.dump(data, f)
    f.close()
    return path


def セルごとの平均ホップ数を出力(devices: Devices, allocation_plan: AllocationPlan, x_length, y_length):
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    cells = [[[0, 0, 0] for i in range(x_length)] for j in range(y_length)]
    for k in allocation_plan.keys():
        for time, al in enumerate(allocation_plan[k]):
            if al is not None and al.hop != -1:
                device, index = search(devices, k, key=lambda d: d.name) # type:(Device, int)
                pos = device.get_pos(time)
                cells[pos.y][pos.x][0] += al.hop
                cells[pos.y][pos.x][1] += 1
                prev_max = cells[pos.y][pos.x][2]
                cells[pos.y][pos.x][2] = max([prev_max, al.hop])

    for row in cells:
        for cell in row:
            if cell[1] == 0:
                print("  ".format(), end=" ")
                continue
            if cell[0] == 0:
                print("{0:02}".format(0), end=" ")
                continue
            avg_hop = int(cell[0]/cell[1])
            if avg_hop < 1:
                COLOR = OKBLUE
            elif avg_hop < 2:
                COLOR = OKGREEN
            elif avg_hop < 3:
                COLOR = WARNING
            else:
                COLOR = FAIL

            print(COLOR + "{0:02}".format(avg_hop) + ENDC, end=" ")
        print()

    print("--------------------------")
    for row in cells:
        for cell in row:
            if cell[1] == 0:
                print("  ".format(), end=" ")
                continue
            if cell[0] == 0:
                print("{0:02}".format(0), end=" ")
                continue
            max_hop = int(cell[2])
            if max_hop < 3:
                COLOR = OKBLUE
            elif max_hop < 6:
                COLOR = OKGREEN
            elif max_hop < 9:
                COLOR = WARNING
            else:
                COLOR = FAIL

            print(COLOR + "{0:02}".format(max_hop) + ENDC, end=" ")
        print()


