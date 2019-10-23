from simulator.model.cloudlet import Cloudlet, Cloudlets, AllTimeCloudlets
from simulator.model.point import Point3D


def plane(t_len: int, x_len: int, y_len: int, r: int=5) -> AllTimeCloudlets:
    all_time_cloudlets = [[[Cloudlet(r, Point3D(i, j, k)) for i in range(x_len)]
                           for j in range(y_len)]
                          for k in range(t_len)]     # type: AllTimeCloudlets
    return all_time_cloudlets

