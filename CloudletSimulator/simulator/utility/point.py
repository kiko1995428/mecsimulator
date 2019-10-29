"""
simulator/utility/point.py
Author          : Kouhei Osaki
Created         : 2017/07/12
Last-Modified   : 2017/07/12
Version         : 1.0.1
Description     : Pointに関する有用な関数などを定義している（適当
"""
from CloudletSimulator.simulator.oldmodels import Point
from typing import List
import math
import random


def adjacency(p: Point, base_p: Point) -> bool:
    """
    pがbase_pに隣接しているか調べる
    :param p: 
    :param base_p: 
    :return: 
    """
    if base_p.x == p.x and math.fabs(base_p.y - p.y) == 1:
        return True
    if math.fabs(base_p.x - p.x) == 1 and base_p.y == p.y:
        return True
    return False


def continuity(p_list: List[Point]) -> bool:
    """
    targetが持つ経路が上下左右いずれかで連続しているかを調べる
    :param p_list: 検査経路
    :return: 連続している場合True，していない場合False
    """
    prev = None  # type:Point
    for current in p_list:
        if prev is None:
            # 最初の一個目の場合
            prev = current
            continue
        if adjacency(current, prev):
            prev = current
        else:
            return False
    return True


def distance(p1: Point, p2: Point) -> int:
    """
    2点間の距離を返す
    :param p1: 
    :param p2: 
    :return: 距離
    """
    return int(math.fabs(p2.x - p1.x)) + int(math.fabs(p2.y - p1.y))


def extract(p: Point, d_max: int, d_min: int=0, p_min: Point=None, p_max: Point=None, ) -> List[Point]:
    """
    pを中心とした指定範囲の座標を抽出する。
    :param p: 中心となる座標
    :param d_max: 距離の最大値
    :param d_min: 距離の最小値
    :param p_max: 指定範囲を形成する座標の最大値
    :param p_min: 指定範囲を形成する座標の最小値
    :return: 条件を満たす座標のリスト
    """
    if p_max is None:
        p_max = Point(p.x + d_max, p.y + d_max)
    if p_min is None:
        p_min = Point(p.x - d_max, p.y - d_max)

    ret = []  # type:List[Point]
    for y in range(p_min.y, p_max.y + 1):
        for x in range(p_min.x, p_max.x + 1):
            pp = Point(x, y)
            if d_min <= distance(p, pp) <= d_max:
                ret.append(pp)
    return ret


def random_two_point(d: int, p_min: Point, p_max: Point) -> (Point, Point):
    """
    指定した範囲の中から指定した距離の２点をランダムに取得する
    :param d: 2点間の距離
    :param p_max: 指定範囲を形成する座標の最大値
    :param p_min: 指定範囲を形成する座標の最小値
    :return: ランダムに取得した二点
    """
    p1 = Point(random.randint(p_min.x, p_max.x), random.randint(p_min.y, p_max.y))  # type:Point
    points = extract(p1, d, d_min=d, p_min=p_min, p_max=p_max, )  # type:List[Point]
    if len(points) == 0:
        raise Exception("距離、もしくは範囲の指定が不正です。")
    p2 = points[random.randint(0, len(points) - 1)]  # type:Point
    return p1, p2


def route(start: Point, goal: Point) -> List[Point]:
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
