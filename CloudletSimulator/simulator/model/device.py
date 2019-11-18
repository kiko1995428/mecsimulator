from CloudletSimulator.simulator.model.application import Application
from CloudletSimulator.simulator.model.route import Route, create_route
from CloudletSimulator.simulator.model.point import Point,Point3D, random_two_point
from CloudletSimulator.simulator.model.angle import Angle,Speed
from typing import List
from tqdm import tqdm


class Device:
    num = 0  # type: int
    def __init__(self, name: str=None, startup_time: int=0, plan: Route=None,
                 apps: List[Application]=None, angle: List[Angle]=None, speed: List[Speed]=None):
        if name is None:
            Device.num += 1
            self._name = "d" + str(Device.num)
        else:
            Device.num += 1
            self._name = name
        self._startup_time = startup_time
        if plan is None:
            self._plan = []
            self._allocation_plan = []
        else:
            self._plan = plan
            self._allocation_plan = [None for i in range(len(self._plan))]  # type: List[Point]
        if apps is None:
            self._apps = []   # type: List[Application]
        else:
            self._apps = apps
        if angle is None:
            self._angle = []
        else:
            self._angle = angle
        if speed is None:
            self._speed = []
        else:
            self._speed = speed

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
    def plan(self) -> Route:
        return self._plan.copy()

    @property
    def angle(self) -> Angle:
        return self._angle.copy()

    @property
    def speed(self) -> Speed:
        return self._speed.copy()

    @angle.setter
    def speed(self, value: Speed) -> None:
        self._speed = value

    @angle.setter
    def angle(self, value: Angle) -> None:
        self._angle = value

    @plan.setter
    def plan(self, value: Route) -> None:
        self._plan = value
        self._allocation_plan = [None for i in range(len(self._plan))]  # type: List[Point]

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

    def append_plan(self, value:Point3D) -> None:
        self._plan.append(value)

    def append_angle(self, value:Angle) -> None:
        self._angle.append(value)
    def append_speed(self, value:Speed) -> None:
        self._speed.append(value)
    def append_app(self, app: Application) -> None:
        self._apps.append(app)

    def remove_app(self, app: Application) -> None:
        del self._apps[self._apps.index(app)]

    def appret(self, namestr: str) -> bool:
        for app in self._apps:
            if app.name != namestr:
                return False
        return True
    def app_name(self):
        for app in self._apps:
            apn = app.name
        return apn
    def is_poweron(self, time: int) -> bool:
        if self.startup_time <= time < self.shutdown_time:
            return True
        else:
            return False

    def get_pos(self, time: int) -> Point:
        return self.plan[time - self.startup_time]

    def get_allocation_point(self, time: int) -> Point:
        p = self._allocation_plan[time - self.startup_time]
        return p

    def set_allocation_point(self, time: int, pos: Point):
        self._allocation_plan[time - self.startup_time] = pos

    def ret_ds_pri(self) -> int:
        return self.ds_pri

    def set_ds_pri(self, value: int):
        self.ds_pri = value

    def add_ds_pri(self, value: int):
        self.ds_pri += value
Devices = List[Device]


def create_devices(p_min: Point, p_max: Point, t_max: int, npt: int, move: int):
    ds = []  # type: Devices
    for t in tqdm(range(t_max)):
        for n in range(npt):
            d = Device(startup_time=t)
            d.use_resource = 1
            start, goal = random_two_point(move, p_min, p_max)
            d.plan = create_route(start, goal)
            ds.append(d)
    return ds