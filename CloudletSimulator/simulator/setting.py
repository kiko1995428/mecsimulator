"""
「プログラムの概要」
シュミレータに関する基本的な情報を定義している。
"""

# AllTimeCloudlets settings
t_length = 60
x_length = 30
y_length = 30

# AllTimeCloudlets Create
default_all_time_cloudlets_create_algorithm = "plane"
default_use_resource_of_plane_cloudlets = 3

#number of device
number_of_device = 100

#device uses resorce
use_resource = 5

# Device Create Algorithm
default_device_create_algorithm = "cross"

# Inputdata Directory
# 自分のPCに合うように書き直す必要あり
inputdata_directory = "/Users/sugimurayuuki/Desktop/CloudletSimulator/inputdata/"
outputdata_directory = "/Users/sugimurayuuki/Desktop/CloudletSimulator/outputdata/"

# run
run_setting = False #初期状態はオフ
allocation_algorithm = "nearby_searchable_ffd" #最近傍選択割り当て（cloudletの割り当て）
inputdata_file = inputdata_directory + "planequatro_cross2017-07-26-15-12-36.data"

# target
targets = [
    "simple", "increasing", "decreasing",
    "ffi_max", "ffd_max"
]
