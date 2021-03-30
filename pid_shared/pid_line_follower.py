from SunFounder_Line_Follower import Line_Follower
from picar import front_wheels
from picar import back_wheels
import picar

import ctypes
import os

BASE_SPEED = 50
BASE_ANGLE = 90
ANGLE_OFFSET = 15
THRESHOLD = 150


def wrap_func(f, restype, argtypes):
	f.restype = restype
	f.argtypes = argtypes

def stop():
	bw.stop()
	fw.turn_straight()
	current_angle = 90

def get_sensor_readings():
	analog = lf.read_analog()
	digital = []
	for value in analog:
		if value < THRESHOLD: digital.append(1)
		else: digital.append(0)
	return digital

def follow_line():
	bw.speed = BASE_SPEED

	while True:
		sensor_reading = get_sensor_readings()
		sensor_data = (ctypes.c_int * 5)(*sensor_reading)
		angle = pid_lib.pid_compute(sensor_data, 5)

		# Write to servo
		if angle > 0: angle += ANGLE_OFFSET
		fw.turn(BASE_ANGLE + angle)


if __name__ == '__main__':
	picar.setup()
	lf = Line_Follower.Line_Follower()
	fw = front_wheels.Front_Wheels(db='config')
	bw = back_wheels.Back_Wheels(db='config')

	pid_lib_name = os.path.abspath(".") + "/" + "pid.so"
	pid_lib = ctypes.CDLL(pid_lib_name)

	wrap_func(pid_lib.pid_init_gains, ctypes.c_int, [ctypes.c_float, ctypes.c_float, ctypes.c_float])
	wrap_func(pid_lib.pid_set_limits, ctypes.c_int, [ctypes.c_float, ctypes.c_float])
	wrap_func(pid_lib.pid_compute, ctypes.c_float, [ctypes.POINTER(ctypes.c_int), ctypes.c_int])

	pid_lib.pid_init_gains(5, 0.01, 0.1)
	pid_lib.pid_set_limits(-20, 20)

	try:
		stop()
		follow_line()
	except KeyboardInterrupt:
		stop()


