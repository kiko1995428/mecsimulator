"""
プログラムの流れ
１．モジュール読み込み
２．データの定義
３．cloudletの3次元モデルの作成
４．cloudletサーバを座標にセット（APの割り当て）
５．デバイスの設定
	１．デバイスのAP設定（APとリソースの割り当て）
	２．デバイスの経路情報設定（始点から終点までの座標リスト）
６．デバイスとcloudletサーバの情報をファイルに書き込む　
"""
from simulator.model.cloudlet import Cloudlet, create_all_time_cloudlets
#時間軸、横軸、縦軸の最大長を指定してCloudletの三次元リストを生成する。
from simulator.model.device import Device
#デバイスのオブジェクト
from simulator.model.point import Point
#マスの判定
from simulator.utility.point import route
#二点間を結ぶ経路を生成する
from simulator.model.application import Application
#アプリケーションのオブジェクト
from simulator.utility.data import input_data_to_file
#デバイス群をファイルに書き込むモジュール
from typing import List
import random

cloudlets_type = "plane" #平面モデルってこと
c_sur = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

ca_num = [0, 0, 0] #Cloudletサーバの数
app1 = Application(name="1")
app2 = Application(name="2")
app3 = Application(name="3")
t_len = 30 #福永さんが研究で使うと決めた時間
x_len = 30
y_len = 30
app_name = [app1.name, app2.name, app3.name] #アプリケーションの名前のリスト
c_resource = 200 #各cloudletの所有リソース量
atcs = create_all_time_cloudlets(t_len, x_len, y_len, r=c_resource) #cloudletnoの格子状のモデルと時間軸を設定(3次元リスト)

#3次元リストの中にアプリケーションの情報をセット
#
i = 0
for x in range(x_len):
    for y in range(y_len):
        for t in range(t_len):
            if i == 0:
                #AP1とAP2の実行環境を持つCloudletサーバの設置
                atcs[x][y][t].apps_append(app1)
                atcs[x][y][t].apps_append(app2)
                ca_num[0] += 1
            if i == 1:
                #AP2とAP3の実行環境を持つCloudletサーバの設置
                atcs[x][y][t].apps_append(app2)
                atcs[x][y][t].apps_append(app3)
                ca_num[1] += 1

            if i == 2:
                #AP1とAP3の実行環境を持つCloudletサーバの設置
                atcs[x][y][t].apps_append(app1)
                atcs[x][y][t].apps_append(app3)
                ca_num[2] += 1
                i = 0
            else:
                i += 1
               # print(1)

devices = []  # type:List[Device]
d_num = 0 #deviceの数
da_num = [0, 0, 0] #deviceの数のリスト

#道路作成
setup_roads = [
    # 混雑道路
    #横線を引くための
    (13, Point(0, 13), Point(x_len - 1, 13)),
    (15, Point(0, 15), Point(x_len - 1, 15)), #真ん中（30の半分）
    (17, Point(0, 19), Point(x_len - 1, 17)),

    (43, Point(13, 0), Point(13, y_len - 1)),
    (45, Point(15, 0), Point(15, y_len - 1)),
    (47, Point(17, 0), Point(17, y_len - 1)),
]
"""
#分散
setup_roads = [
# 混雑道路
#    (13, Point(0, 0), Point(x_len - 1, y_len -1)),
#    (15, Point(x_len-1, y_len-1), Point(0, 0)),
#    (43, Point(0, y_len-1), Point(x_len-1, 0)),
 #   (45, Point(x_len-1, 0), Point(0, y_len-1)),
]
"""

#print(len(setup_roads))
min_road_device_num = 3 #経路に対するデバイスの最小数
max_road_device_num = 9 #経路に対するデバイスの最大数
min_use_resource = 1 #デバイスが使える最小リソース数
max_use_resource = 5 #デバイスが使える最大リソース数
app1 = Application(name="1", use_resource=3)
app2 = Application(name="2", use_resource=3)
app3 = Application(name="3", use_resource=3)
app_resourse = [app1.use_resource, app2.use_resource, app3.use_resource] #アプリケーションが使えるリソース量のリスト

print(x_len)
n = 90
dnum = 1 #デバイス数
for road in setup_roads:
    road_num = road[0] #setup_roadsの1列目
    side_a = road[1] #setup_roadsの2列目(x軸が始点 or y軸が始点)
    #print(side_a)
    side_b = road[2] #setup_roadsの3列目（x軸が終点 or y軸が終点）
    for i in range(x_len):
        for j in range(n):
            d_name = "d{0}{1:05}".format(road_num, d_num)
            d = Device(name=d_name) #デバイスのオブジェクトに名前を代入してインスタンス作成
            d.startup_time = 0 #デバイスのインスタンスに起動時間を代入
            if dnum == 13:
                d.append_app(Application(name="1", use_resource=random.randint(min_use_resource, max_use_resource)))
                da_num[2] += 1
                dnum = 1
            elif dnum % 2 == 0:
                d.append_app(Application(name="2", use_resource=random.randint(min_use_resource, max_use_resource)))
                da_num[0] += 1
            else:
                d.append_app(Application(name="3", use_resource=random.randint(min_use_resource, max_use_resource)))
                da_num[1] += 1
            dnum += 1
            if random.randint(0, 3) == 0:
                # 別サイドをゴールにする
                # route(始点,　終点): 二点間を結ぶ経路を生成し、始点から終点までのリストを返す
                roads = list(filter(lambda r: r[0] / 30 != road[0] / 30, setup_roads))
                r = roads[random.randint(0, len(roads) - 1)]
                goal = random.randint(1, 2) #任意の範囲の整数のランダムを返す

                #デバイスの経路情報設定
                if random.randint(0, 1) == 0:
                    if road[0] < 30:
                        d.plan = route(Point(i, side_a.y), r[goal]) #左右の経路
                        d.plan = route(Point(side_a.x, i), r[goal]) #上下の経路
                else:
                    if road[0] < 30:
                        d.plan = route(Point(x_len - 1 - i, side_a.y), r[goal]) #左右の経路
                    else:
                        d.plan = route(Point(side_a.x, y_len - 1 - i), r[goal]) #上下の経路
            else:
                if random.randint(0, 1) == 0:
                    # aからbへ
                    if road[0] < 30:
                        d.plan = route(Point(i, side_a.y), side_b)
                    else:
                        d.plan = route(Point(side_a.x, i), side_b)
                else:
                    # bからaへ
                    if road[0] < 30:
                        d.plan = route(Point(x_len - 1 - i, side_a.y), side_a)
                    else:
                        d.plan = route(Point(side_a.x, y_len - 1 - i), side_a)
            devices.append(d)
            d_num += 1

#ある程度混雑した道路状況のため？
dnum = 1 #dnumの初期化
for t in range(t_len):
    for road in setup_roads:
        road_num = road[0]
        #print("road_num2: ", road_num)
        side_a = road[1]
        side_b = road[2]
        #n = random.randint(min_road_device_num, max_road_device_num)
        for i in range(n):
            d_name = "d{0}-{1:05}".format(road_num, d_num)
            d = Device(name=d_name)
            if dnum == 13:
                d.append_app(Application(name="1", use_resource=random.randint(min_use_resource, max_use_resource)))
                da_num[2] += 1
                dnum = 1
            elif dnum % 2 == 0:
                d.append_app(Application(name="2", use_resource=random.randint(min_use_resource, max_use_resource)))
                da_num[0] += 1
            else:
                d.append_app(Application(name="3", use_resource=random.randint(min_use_resource, max_use_resource)))
                da_num[1] += 1
            dnum += 1
            if random.randint(0, 3) == 0:
                roads = list(filter(lambda r: r != road, setup_roads))
                r = roads[random.randint(0, len(roads) - 1)]
                goal = random.randint(1, 2)
                if random.randint(0, 1) == 0:
                    d.plan = route(side_a, r[goal])
                else:
                    d.plan = route(side_b, r[goal])
            else:
                if random.randint(0, 1) == 0:
                    d.plan = route(side_a, side_b)
                else:
                    d.plan = route(side_b, side_a)
            devices.append(d)
            d_num += 1

print("All_devices_num = ", d_num)
print("Device_num[AP2, AP3 ,AP1] = ", da_num) #デバイスの数のリスト
print("Cloudlet_num[AP1&AP2, AP2&AP3, AP1&AP3] =", ca_num) #cloudletサーバの数のリスト
#print("Cloudlet_resource = ", c_resource)

#辞書作成
header = {
    "device_num": d_num,
    "t_length": 30,
    "x_length": 30,
    "y_length": 30,
    "min_road_device_num": min_road_device_num,
    "max_road_device_num": max_road_device_num,
    "min_use_resource": min_use_resource,
    "max_use_resource": max_use_resource,
    "c_resource": c_resource,
    "app_name": app_name,
    "app_resourse": app_resourse
}

random.shuffle(devices)
#path = input_data_to_file(header, atcs, devices, "ieeei-d90")  #デバイスの情報をファイルに書き込んでinputdata作成
#print("outputed -> {}".format(path))
