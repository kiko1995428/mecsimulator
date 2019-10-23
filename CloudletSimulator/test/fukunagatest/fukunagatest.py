
from simulator.model.cloudlet import Cloudlet, create_all_time_cloudlets


def ari():
    t_len = 30
    x_len = 30
    y_len = 30

    atcs = create_all_time_cloudlets(t_len, x_len, y_len)


    print(atcs[3][3][1])

def iu():
    print ("a")
