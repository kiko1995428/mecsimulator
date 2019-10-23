class Application:
    num = 0
    app_pri = 1
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

    def app_pri_set(self, value: int) -> None:
        self.app_pri = value