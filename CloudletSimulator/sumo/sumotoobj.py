import csv

from simulator.model.cloudlet import Cloudlet, create_all_time_cloudlets
from simulator.model.device import Device
from simulator.model.point import Point3D
from simulator.utility.point import route
from simulator.model.application import Application
from simulator.utility.data import input_data_to_file
from typing import List
import random

#deviceの作成
with open('Kuruma.csv', newline='') as csvfile:
	#csvの読み込み
	reader = csv.DictReader(csvfile)
	devices = [] # type:List[Device]
	dflag = 0
	for row in reader:
		d_name = row['vehicle_id']
		d_time = row['timestep_time']
		d_lon = row['vehicle_x']
		d_lat = row['vehicle_y']
		d_angle = row['vehicle_angle']
		dflag = 0
		for d in devices:
				#情報の追加
			if d.name == d_name:
				d.plan.append(Point3D(d_lon, d_lat, d_time))
				d.d_angle.append(d_angle)
				dflag = 1
				break
		if dflag == 0:
			d = Device(name=d_name)
			d.startup_time=d_time
			d.plan.append(Point3D(d_lon, d_lat, d_time))
			d.d_angle.append(d_angle)
			devices.append(d)

	print(devices)


