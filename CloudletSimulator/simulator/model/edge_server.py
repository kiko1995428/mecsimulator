from CloudletSimulator.simulator.model.device import Device, Devices
from CloudletSimulator.simulator.model.application import Application
from CloudletSimulator.simulator.model.point import Point, Point3D, point3d_to_point
from typing import List
import math
from math import radians, cos, sin, asin, sqrt, atan2
import geopy
from geopy.distance import vincenty


class MEC_server:
    num = 0
    cong_pri_app = [0, 0, 0]

    # def __init__(self, resource: int, point: Point3D, devices: Devices=None, name: str=None, server_type, lon, lat, range):
    def __init__(self, resource: int, name, server_type, lon, lat, range, system_end_time):
        # def __init__(self, resource: int, name, server_type, lon, lat, range, system_end_time, devices: Devices = None):
        """
        コンストラクタ
        :param r: 所有リソース
        :param devices: 予約デバイス
        :param name: エッジサーバ名
        """
        """
        if name is None:
            Cloudlet.num += 1
            self._name = "c" + str(Cloudlet.num)
        else:
            self._name = name
        """
        self._resource = resource
        """
        if devices is None:
            self._devices = []  # type: Devices
        else:
            self._devices = devices     # type: Devices
        self._point = point
        """
        self._apps = []

        # ----
        self._name = name
        self._server_type = server_type
        self._lon = lon
        self._lat = lat
        self._range = range
        self._system_end_time = system_end_time
        self._having_devices = [[] * 0] * system_end_time
        # ----

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value) -> None:
        self._name = value

    @property
    def point3d(self) -> Point3D:
        return self._point

    @property
    def point(self) -> Point:
        return point3d_to_point(self._point)

    @property
    def resource(self) -> int:
        return self._resource

    @resource.setter
    def resource(self, value: int) -> None:
        self._resource = value

    @property
    def devices(self) -> Devices:
        new_devices = []  # type: Devices
        for device in self._devices:
            new_devices.append(device)
        return new_devices

    @property
    def used_resource(self) -> int:
        used_resource = 0
        for device in self._devices:
            used_resource = used_resource + device.use_resource
        return used_resource

    @property
    def empty_resource(self) -> int:
        return self.resource - self.used_resource

    @property
    def apps(self) -> List[Application]:
        ret = []  # type: List[Application]
        for app in self._apps:
            ret.append(app)
        return ret

    # ゲッタ-(server_type)
    @property
    def server_type(self) -> str:
        return self._server_type

    # ゲッター(lon)
    @property
    def lon(self) -> float:
        return self._lon

    # ゲッター(lat)
    @property
    def lat(self) -> float:
        return self._lat

    # ゲッター(range)
    @property
    def range(self) -> float:
        return self._range

    # 混雑度の基準値
    @property
    def congestion_standard(self):
        return self._resource * 0.3

    # 混雑しているのかの判定
    def congestion_judge(self, request_resource):
        if request_resource >= self.congestion_standard:
            return True
        else:
            return False

    #def check_resource(self, device: Device) -> bool:
    def check_resource(self, app_resource):
        #if self.resource - device.use_resource >= 0:
        if self.resource - app_resource >= 0:
            return True
        else:
            return False

    def is_operatable_application(self, app_name: str) -> bool:
        # 指定されたアプリケーションが実行可能か返す
        #:param app_name: アプリケーション名
        #:return: true -> 実行可能, false -> 実行不可能
        #if app_name in [app.name for app in self.apps]:
        #if app_name == self.apps[0] or app_name == self.apps[1]:
        if (app_name in self.apps) == True:
            return True
        else:
            return False


    def apps_append(self, value: Application):
        self._apps.append(value)


"""
    @property
    def having_devices(self):
        return self._having_devices

    @having_devices.setter
    def append_having_devices(self, time, device: Device):
        self._having_devices[time].append(device)

def can_append_device(self, device: Device, app_check: bool=False) -> bool:

    #指定されたデバイスが追加可能か判定するメソッド
    #:param device: 追加するデバイス(Deviceクラス)
    #:param app_check: アプリケーション名のチェックを行うか
    #:return: 追加可能ならTrue，追加不可能ならFalse

    if app_check:
        for app in device.apps:
            if not self.is_operatable_application(app.name):
                return False
    if self.empty_resource < device.use_resource:
        return False
    return True

def is_operatable_application(self, app_name: str) -> bool:
    clear

    #指定されたアプリケーションが実行可能か返す
    #:param app_name: アプリケーション名
    #:return: true -> 実行可能, false -> 実行不可能

    if app_name in [app.name for app in self.apps]:
        return True
    else:
        return False

def append_device(self, new_device: Device) -> None:

    #指定されたデバイスをクラウドレットに追加する
    #:param new_device:
    #:return:
    self._devices.append(new_device)
    if self.can_append_device(new_device):
        self._devices.append(new_device)
    else:
        raise Exception("リソースが不足しています")

def apps_append(self, value: Application):
    self._apps.append(value)

def remove_device(self, device: Device) -> None:
    del self._devices[self._devices.index(device)]

#Cloudlet集合の定義
#型アノテーション用だが現状意味はない(2017/06/14)

CloudletRowItems = List[MEC_server]
NearCloudlets = List[MEC_server]
Cloudlets = List[CloudletRowItems]
AllTimeCloudlets = List[MEC_server]


def create_all_time_cloudlets(t_len: int, x_len: int, y_len: int, r: int=5) -> AllTimeCloudlets:

   #時間軸、横軸、縦軸の最大長を指定してCloudletの三次元リストを生成する。
    #:param t_len: 時間軸の最大長
    #:param x_len: 横軸の最大長
    #:param y_len: 縦軸の最大長
    #:param r: 各クラウドレットの所有リソース
   # :return:

    all_time_cloudlets = [[[Cloudlet(r, Point3D(i, j, k)) for i in range(x_len)]
                           for j in range(y_len)]
                          for k in range(t_len)]     # type: AllTimeCloudlets
    return all_time_cloudlets


def is_valid_point(cloudlets: Cloudlets, p: Point) -> bool:
    if not (0 <= p.y < len(cloudlets)):
        return False
    if not (0 <= p.x < len(cloudlets[p.y])):
        return False
    return True


def check_allocate(cloudlets: AllTimeCloudlets, devices: Devices) -> bool:

    #正常な割り当てが成功しているかを検査する
   # :param cloudlets:
    #:param devices:
   # :return:

    # Todo: 未実装
    return True
"""


# ２点の緯度経度から距離（メートル）を返すメソッド
def distance_calc(lat1, lon1, lat2, lon2):
    # return distance as meter if you want km distance, remove "* 1000"
    radius = 6371 * 1000

    dLat = (lat2 - lat1) * math.pi / 180
    dLot = (lon2 - lon1) * math.pi / 180

    lat1 = lat1 * math.pi / 180
    lat2 = lat2 * math.pi / 180

    val = sin(dLat / 2) * sin(dLat / 2) + sin(dLot / 2) * sin(dLot / 2) * cos(lat1) * cos(lat2)
    ang = 2 * atan2(sqrt(val), sqrt(1 - val))
    return radius * ang  # meter


# 基地局のカバー範囲内の割り振られていないデバイスを探すメソッド
# リソース量はここで調整する
# cover_range_searchの引数がオブジェクト版
def cover_range_search(device: Device, plan_index, lon, lat, cover_range, id, MEC_resource,
                       app_resource):
    memo = 0
    if (MEC_resource > 0) or ((MEC_resource - app_resource) >= 0):
        distance = distance_calc(float(device.plan[plan_index].y),
                                 float(device.plan[plan_index].x), lat, lon)
        if distance <= cover_range:
            memo = id
            MEC_resource = MEC_resource - app_resource
            return memo, MEC_resource, True
        else:
            return memo, MEC_resource, False
    else:
        return memo, MEC_resource, False


# test用簡易版
def cover_range_search2(device_flag, device_lon, device_lat, lon, lat, cover_range, id):
    memo = 0
    if device_flag == False:
        distance = distance_calc(device_lat, device_lon, lat, lon)
        if distance <= cover_range:
            # print("found!!!!!")
            print("distance:", distance, "m")
            device_flag = True
            memo = id
            return device_flag, memo
        else:
            return device_flag, memo
    else:
        return device_flag, memo


def old_cover_range_search(device_flag, device_lon, device_lat, lon, lat, cover_range, id, MEC_resource, app_resource):
    memo = 0
    if (device_flag == False) or (MEC_resource > 0) or ((MEC_resource - app_resource) >= 0):
        distance = distance_calc(device_lat, device_lon, lat, lon)
        if distance <= cover_range:
            memo = id
            MEC_resource = MEC_resource - app_resource
            return memo, MEC_resource, True
        else:
            return memo, MEC_resource, False
    else:
        return memo, MEC_resource, False


# MECサーバに割り振れたデバイスの数を返す
def allocated_devices_count(original_resource, corrent_resource, devices_resource):
    count = (original_resource - corrent_resource) / devices_resource
    return count


# 混雑度計算
def traffic_congestion(lon, lat, cover_range, device_num, devices: Device, system_time, request_resource):
    cnt = 0
    for i in range(device_num):
        # system_timeとplanのインデックス番号の対応付ける処理を記述する必要あり
        # 引数のsystem_timeからインデックス番号と対応付けられている時間を求める
        # なぜか起動時間と終了時間が反映されていない
        startup = devices[i].startup_time
        shutdown = devices[i].shutdown_time
        # print(startup)
        # print(shutdown)
        position = (lat, lon)
        if startup <= system_time and shutdown >= system_time:
            # デバイスのplanのindex番号を計算
            index = int(system_time) - int(startup)
            if index < (shutdown - startup):
                # vincety法
                # --
                # device_lat = float(devices[i].plan[index].y)
                # device_lon = float(devices[i].plan[index].x)
                # device_position = (device_lat, device_lon)
                # distance = vincenty(position, device_position).miles * 1609.34
                # ---
                # ユーグリット距離
                distance = distance_calc(float(devices[i].plan[index].y), float(devices[i].plan[index].x), lat, lon)
                # カバー範囲内のデバイスをカウント
                if distance <= cover_range:
                    cnt = cnt + 1
    return cnt * request_resource

# MECサーバが持っているデバイスを表示
# mec.having_device[time]=[device,device,....]
# @property
# def having_device(self, time):
#    return self._having_device[time]

# @having_device.setter
# def having_device(self, time, value: Device):
#    self._having_device[time].append(value)
