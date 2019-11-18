import csv

from CloudletSimulator.simulator.model.cloudlet import Cloudlet, create_all_time_cloudlets
from CloudletSimulator.simulator.model.device import Device
from CloudletSimulator.simulator.model.point import Point3D
from CloudletSimulator.simulator.model.angle import Angle,Speed
from CloudletSimulator.simulator.utility.point import route
from CloudletSimulator.simulator.model.application import Application
from CloudletSimulator.simulator.utility.data import input_data_to_file
from typing import List
import pickle
import random

#deviceの作成
with open('Kuruma.csv', newline='') as csvfile:
	#csvの読み込み
	reader = csv.DictReader(csvfile)
	devices = [] # type:List[Device]
	dflag = 0
	num = 0
	for row in reader:
		d_name = row['vehicle_id']
		d_time = row['timestep_time']
		d_lon = row['vehicle_x']
		d_lat = row['vehicle_y']
		d_angle = Angle(d_time, row['vehicle_angle'])
		d_speed = Speed(d_time, row['vehicle_speed'])
		d_plan = Point3D(d_lon, d_lat, d_time)
		dflag = 0

		for d in devices:
				#情報の追加
			if d.name == d_name:
				d.append_speed(d_speed)
				d.append_plan(d_plan)
				d.append_angle(d_angle)
				dflag = 1
				break
		if dflag == 0:
			d = Device(name=d_name)
			d.startup_time=d_time
			d.append_plan(d_plan)
			d.append_speed(d_speed)
			d.append_angle(d_angle)
			d.use_resource = 1
			devices.append(d)
			num += 1
	f = open('device.binaryfile', 'wb')
	pickle.dump(devices,f)
	f.close
