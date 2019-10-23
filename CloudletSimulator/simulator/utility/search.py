from typing import Iterable, Callable, Any


def search(iterable: Iterable, obj, key: Callable=lambda k: k) -> (Any, int):
    for index, o in enumerate(iterable):
        if key(o) == obj:
            return o, index
    else:
        return None, -1
