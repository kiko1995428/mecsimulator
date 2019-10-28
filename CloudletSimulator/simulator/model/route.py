from simulator.model.point import Point, adjacency, Point3D
from typing import List, Dict
import random


Route = List[Point3D]


def create_route(start: Point, goal: Point) -> Route:
    """
    二点間を結ぶ経路を生成する
    :param start: 開始座標
    :param goal: 終了座標
    :return: startからgoalに行くために経由する座標のリスト
    """
    current = Point(start.x, start.y)
    r = [Point(current.x, current.y)]  # type:List[Point]
    while current != goal:
        # goalに到達するまでループ
        x_dir = goal.x - current.x
        y_dir = goal.y - current.y
        if x_dir > 0 and y_dir > 0:
            # 目的地が右下
            if random.randint(0, 1) == 0:
                # 下に移動
                current = Point(current.x, current.y + 1)
            else:
                # 右に移動
                current = Point(current.x + 1, current.y)
            r.append(current)
        elif x_dir > 0 and y_dir < 0:
            # 目的地が右上
            if random.randint(0, 1) == 0:
                # 上に移動
                current = Point(current.x, current.y - 1)
            else:
                # 右に移動
                current = Point(current.x + 1, current.y)
            r.append(current)
        elif x_dir < 0 and y_dir > 0:
            # 目的地が左下
            if random.randint(0, 1) == 0:
                # 下に移動
                current = Point(current.x, current.y + 1)
            else:
                # 左に移動
                current = Point(current.x - 1, current.y)
            r.append(current)
        elif x_dir < 0 and y_dir < 0:
            # 目的地が左上
            if random.randint(0, 1) == 0:
                # 上に移動
                current = Point(current.x, current.y - 1)
            else:
                # 左に移動
                current = Point(current.x - 1, current.y)
            r.append(current)
        elif x_dir == 0 and y_dir > 0:
            # 目的地が下
            current = Point(current.x, current.y + 1)
            r.append(current)
        elif x_dir == 0 and y_dir < 0:
            # 目的地が上
            current = Point(current.x, current.y - 1)
            r.append(current)
        elif x_dir > 0 and y_dir == 0:
            # 目的地が右
            current = Point(current.x + 1, current.y)
            r.append(current)
        elif x_dir < 0 and y_dir == 0:
            # 目的地が左
            current = Point(current.x - 1, current.y)
            r.append(current)
        else:
            raise Exception
    return r


def continuity(r: Route) -> bool:
    """
    targetが持つ経路が上下左右いずれかで連続しているかを調べる
    :param r: 検査する経路
    :return: 連続している場合True，していない場合False
    """
    prev = None  # type: Point
    for current in r:
        if prev is None:
            # 最初の一個目の場合
            prev = current
            continue
        if adjacency(current, prev):
            prev = current
        else:
            return False
    return True

