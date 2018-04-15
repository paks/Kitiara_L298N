#!/usr/bin/env python
'''
**********************************************************************
* Filename    : speed_increase.py
* Description : a test script for SunFounder_L298N module
* Author      : Cavon
* Brand       : SunFounder
* E-mail      : service@sunfounder.com
* Website     : www.sunfounder.com
* Update      : Cavon    2016-09-23    New release
**********************************************************************
'''

import time
from Kitiara_L298N import L298N
from SunFounder_PCA9685 import PCA9685

def main():
	print "********************************************"
	print "*                                          *"
	print "*            Kitiara L298N                 *"
	print "*                                          *"
	print "*          Connect MA to BCM17             *"
	print "*          Connect MB to BCM18             *"
	print "*         Connect PWMA to BCM27            *"
	print "*         Connect PWMB to BCM12            *"
	print "*                                          *"
	print "********************************************"
	pwm = PCA9685.PWM()
	pwm.debug = True
	pwm.frequency = 60

	def a_speed(value):
		pwm.write(0,0,value)

	def b_speed(value):
		pwm.write(3,0,value)

	motorA = L298N.Motor(5, 6)
	motorB = L298N.Motor(13, 19)
	motorA.set_debug(True)
	motorB.set_debug(True)
	motorA.pwm = a_speed
	motorB.pwm = b_speed
	

	delay = 0.05

	motorA.forward()
	for i in range(0, 101):
		motorA.set_speed(i)
		time.sleep(delay)
	for i in range(100, -1, -1):
		motorA.set_speed(i)
		time.sleep(delay)

	motorA.backward()
	for i in range(0, 101):
		motorA.set_speed(i)
		time.sleep(delay)
	for i in range(100, -1, -1):
		motorA.set_speed(i)
		time.sleep(delay)

	motorB.forward()
	for i in range(0, 101):
		motorB.set_speed(i)
		time.sleep(delay)
	for i in range(100, -1, -1):
		motorB.set_speed(i)
		time.sleep(delay)

	motorB.backward()
	for i in range(0, 101):
		motorB.set_speed(i)
		time.sleep(delay)
	for i in range(100, -1, -1):
		motorB.set_speed(i)
		time.sleep(delay)

def destroy():
	motorA.stop()
	motorB.stop()

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		destroy()