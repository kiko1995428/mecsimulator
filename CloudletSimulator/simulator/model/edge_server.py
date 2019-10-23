#from simulator.model.device import Device, Devices
#from simulator.model.application import Application
#from simulator.model.point import Point, Point3D, point3d_to_point
#from typing import List
import pandas as pd


class MEC_server:
    num = 0
    cong_pri_app = [0, 0, 0]
    #def __init__(self, resource: int, point: Point3D, devices: Devices=None, name: str=None, server_type, lon, lat, range):
    def __init__(self, resource: int, name, server_type, lon, lat, range):
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
        self._apps = []
        """
        #----
        self._name = name
        self._server_type = server_type
        self._lon = lon
        self._lat = lat
        self._range = range
        #----
    """
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
    """
    @property
    def resource(self) -> int:
        return self._resource

    @resource.setter
    def resource(self, value: int) -> None:
        self._resource = value
    """
    @property
    def devices(self) -> Devices:
        new_devices = []    # type: Devices
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
    """
#---
    #ゲッター（id）
    @property
    def id(self) -> int:
        return self._id
    #ゲッタ-(server_type)
    @property
    def server_type(self) -> str:
        return self._server_type

    #ゲッター(lon)
    @property
    def lon(self) -> float:
        return self._lon
    
    #ゲッター(lat)
    @property
    def lat(self) -> float:
        return self._lat

    #ゲッター(range)
    @property
    def range(self) -> float:
        return self._range 
#---
    """
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
        
        if self.can_append_device(new_device):
            self._devices.append(new_device)
        else:
            raise Exception("リソースが不足しています")

    def apps_append(self, value: Application):
        self._apps.append(value)

    def remove_device(self, device: Device) -> None:
        del self._devices[self._devices.index(device)]
    """



"""
Cloudlet集合の定義
型アノテーション用だが現状意味はない(2017/06/14)
"""
"""
CloudletRowItems = List[Cloudlet]
NearCloudlets = List[Cloudlet]
Cloudlets = List[CloudletRowItems]
AllTimeCloudlets = List[Cloudlets]


def create_all_time_cloudlets(t_len: int, x_len: int, y_len: int, r: int=5) -> AllTimeCloudlets:
  
   # 時間軸、横軸、縦軸の最大長を指定してCloudletの三次元リストを生成する。
   # :param t_len: 時間軸の最大長
    #:param x_len: 横軸の最大長
   # :param y_len: 縦軸の最大長
   # :param r: 各クラウドレットの所有リソース
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
    #:param cloudlets:
    #:param devices:
    #:return:
   
    # Todo: 未実装
    return True
"""
#test用
if __name__ == "__main__":
    #CSV読み込み
    df = pd.read_csv("kddi_okayama_city.csv", dtype={'lon':'float','lat':'float'})
    #基地局の種類を設定
    server_type = "LTE"
    #基地局のカバー範囲を設定
    cover_range = 500
    #CSVの行数を取得（基地局の数）
    n = len(df)
    print("Number of MEC server:", n)
    #基地局の数のオブジェクト用リストを作成
    mec = [MEC_server(0,00, " ", 00.00, 00.00, 0)] * n
    #オブジェクト作成
    for index, series in df.iterrows():
        mec[index] = MEC_server(10,index+1, server_type, series["lon"], series["lat"], cover_range) #０からカウントのため、1を＋
        print("ID:", mec[index].name, ",", " type:", mec[index].server_type)
        print("lat:", mec[index].lat, ",", "lon:", mec[index].lon)
        print("range:", mec[index].range,"m")
        print("**************")