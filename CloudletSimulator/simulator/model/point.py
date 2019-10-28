import collections
import math
import random
from typing import List


Point = collections.namedtuple('Point', ('x', 'y'))
Point3D = collections.namedtuple('Point3D', ('x', 'y', 'time'))


def point3d_to_point(p3d: Point3D) -> Point:
    return Point(p3d.x, p3d.y)


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


def near_points(center: Point, d_max: int, p_max: Point, p_min: Point) -> List[Point]:
    """
    指定した座標周辺の座標を取得する
    例えば、centerが(2, 2)でd_maxが2のとき、
                    (2, 0), 
            (1, 1), (2, 1), (3, 1), 
    (0, 2), (1, 2), (2, 2), (3, 2), (4, 2),
            (1, 3), (2, 3), (3, 3), 
                    (2, 4)
    が得られる
    :param center: 中心座標
    :param d_max: 最小距離
    :param p_max: 最大座標
    :param p_min: 最小座標
    :return: 範囲内の座標リスト
    """
    res = []  # type: List[Point]
    for y in [y for y in range(center.y - d_max, center.y + d_max + 1) if p_min.y <= y <= p_max.y]:
        f = int(math.fabs(center.y - y))
        for x in [x for x in range(center.x - (d_max - f), center.x + (d_max - f) + 1) if p_min.x <= x <= p_max.x]:
            p = Point(x, y)
            res.append(p)
    return res
