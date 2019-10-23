# coding:utf-8
"""
oldmodels.py
Author          : Kouhei Osaki
Created         : 2017/06/11
Last-Modified   : 2017/07/07
Version         : 1.3.2
Description     : リソースの割当処理を行うメソッドを定義している。 
"""


import collections
from typing import List, Dict


"""
座標の定義
"""
Point = collections.namedtuple('Point', ('x', 'y'))


"""
移動計画の定義
型アノテーション用だが現状意味はない(2017/06/14)
"""
MovementPlan = List[Point]


"""
割り当て計画の定義
型アノテーション用だが現状意味はない(2017/06/14)
"""
Allocation = collections.namedtuple('Allocation', ('x', 'y', 'hop'))
AllocationPlan = Dict["str", List[Allocation]]


class Application:
    num = 0

    def __init__(self, name: str=None, use_resource: int=1):
        if name is None:
            Application.num += 1
            self._name = "a" + str(Application.num)
        else:
            self._name = name
        self._use_resource = use_resource

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @property
    def use_resource(self) -> int:
        return self._use_resource

    @use_resource.setter
    def use_resource(self, value: int) -> None:
        self._use_resource = value


class Device:
    num = 0  # type: int

    def __init__(self, name: str=None, startup_time: int=0, plan: MovementPlan=None, apps: List[Application]=None):
        if name is None:
            Device.num += 1
            self._name = "d" + str(Device.num)
        else:
            self._name = name
        self._startup_time = startup_time
        if plan is None:
            self._plan = []
        else:
            self._plan = plan
        if apps is None:
            self._apps = []   # type: List[Application]
        else:
            self._apps = apps

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @property
    def startup_time(self) -> int:
        return self._startup_time

    @startup_time.setter
    def startup_time(self, value: int) -> None:
        self._startup_time = value

    @property
    def moving_time(self) -> int:
        return len(self._plan)

    @property
    def shutdown_time(self) -> int:
        return self.startup_time + self.moving_time

    @property
    def plan(self) -> MovementPlan:
        return self._plan.copy()

    @plan.setter
    def plan(self, value: MovementPlan) -> None:
        self._plan = value

    @property
    def apps(self) -> List[Application]:
        ret = []    # type: List[Application]
        for app in self._apps:
            ret.append(app)
        return ret

    @apps.setter
    def apps(self, value: List[Application]):
        self._apps = value

    @property
    def use_resource(self) -> int:
        res = 0
        for app in self._apps:
            res += app.use_resource
        return res

    @use_resource.setter
    def use_resource(self, value: int) -> None:
        """
        利用非推奨
        :param value: 
        :return: 
        """
        if self.use_resource == value:
            pass
        elif self.use_resource < value:
            padding_app = Application(name="padding", use_resource=value - self.use_resource)
            self.append_app(padding_app)
        else:
            app = Application(name="padding", use_resource=value)
            self.apps = [app]

    def append_app(self, app: Application) -> None:
        self._apps.append(app)

    def remove_app(self, app: Application) -> None:
        del self._apps[self._apps.index(app)]


"""
デバイス集合の定義
型アノテーション用だが現状意味はない(2017/06/14)
"""
Devices = List[Device]


class Cloudlet:
    num = 0

    def __init__(self, r: int=10, devices: Devices=None, name: str=None):
        """
        コンストラクタ
        :param r: 所有リソース
        :param devices: 予約デバイス
        :param name: Cloudlet名
        """
        if name is None:
            Cloudlet.num += 1
            self._name = "c" + str(Cloudlet.num)
        else:
            self._name = name
        self._resource = r
        if devices is None:
            self._devices = []  # type: Devices
        else:
            self._devices = devices     # type: Devices

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value) -> None:
        self._name = value

    @property
    def resource(self) -> int:
        return self._resource

    @resource.setter
    def resource(self, value: int) -> None:
        self._resource = value

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

    def can_append_device(self, device: Device) -> bool:
        """
        指定されたデバイスが追加可能か判定するメソッド
        :param device: 追加するデバイス(Deviceクラス)
        :return: 追加可能ならTrue，追加不可能ならFalse
        """
        if self.empty_resource < device.use_resource:
            return False
        else:
            return True

    def append_device(self, new_device: Device) -> None:
        """
        指定されたデバイスをクラウドレットに追加する
        :param new_device: 
        :return: 
        """
        if self.can_append_device(new_device):
            self._devices.append(new_device)
        else:
            raise Exception("リソースが不足しています")

    def remove_device(self, device: Device) -> None:
        del self._devices[self._devices.index(device)]


"""
Cloudlet集合の定義
型アノテーション用だが現状意味はない(2017/06/14)
"""
CloudletRowItems = List[Cloudlet]
NearCloudlets = List[Cloudlet]
Cloudlets = List[CloudletRowItems]
AllTimeCloudlets = List[Cloudlets]
