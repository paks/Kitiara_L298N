#!/usr/bin/env python
'''
**********************************************************************
* Filename    : L298N.py
* Description : A driver module for L298N
* Author      : Cavon
* Brand       : SunFounder
* E-mail      : service@sunfounder.com
* Website     : www.sunfounder.com
* Update      : Cavon    2016-09-23    New release
**********************************************************************
'''
import RPi.GPIO as GPIO

class Motor(object):
	''' Motor driver class
		Set direction_channel_a to the GPIO channel which connect to MA, 
		Set motor_B to the GPIO channel which connect to MB,
		Both GPIO channel use BCM numbering;
		Set pwm_channel to the PWM channel which connect to PWMA,
		Set pwm_B to the PWM channel which connect to PWMB;
		PWM channel using PCA9685, Set pwm_address to your address, if is not 0x40
		Set debug to True to print out debug informations.
	'''
	_DEBUG = False
	_DEBUG_INFO = 'DEBUG "L298N.py":'

	def __init__(self, direction_channel_a, direction_channel_b, pwm=None, offset=True):
		'''Init a motor on giving dir. channel and PWM channel.'''
		if self._DEBUG:
			print self._DEBUG_INFO, "Debug on"
		self.direction_channel_a = direction_channel_a
		self.direction_channel_b = direction_channel_b
		self._offset = offset
		self.forward_offset = self._offset
		self.backward_offset = not self.forward_offset
		self._pwm = pwm
		self._speed = 0

		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BCM)

		if self._DEBUG:
			print self._DEBUG_INFO, 'setup motor direction channel at', direction_channel_a
			print self._DEBUG_INFO, 'setup motor pwm channel as', self._pwm.__name__
		GPIO.setup(self.direction_channel_a, GPIO.OUT)
		GPIO.setup(self.direction_channel_b, GPIO.OUT)

	@property
	def offset(self):
		return self._offset

	@offset.setter
	def offset(self, value):
		''' Set offset for much user-friendly '''
		if value not in (True, False):
			raise ValueError('offset value must be Bool value, not"{0}"'.format(value))
		self.forward_offset = value
		self.backward_offset = not self.forward_offset
		if self._DEBUG:
			print self._DEBUG_INFO, 'Set offset to %d' % self._offset

	@property
	def speed(self):
		return self._speed

	@speed.setter
	def speed(self, speed):
		''' Set Speed with giving value '''
		if speed not in range(0, 101):
			raise ValueError('speed ranges fron 0 to 100, not "{0}"'.format(speed))
		if not callable(self._pwm):
			raise ValueError('pwm is not callable, please set Motor.pwm to a pwm control function with only 1 veriable speed')
		if self._DEBUG:
			print self._DEBUG_INFO, 'Set speed to: ', speed
		self._speed = speed
		self._pwm(self._speed)

	def forward(self):
		''' Set the motor direction to forward '''
		GPIO.output(self.direction_channel_a, not self.forward_offset)
		GPIO.output(self.direction_channel_b, self.forward_offset)
		self.speed = self._speed
		if self._DEBUG:
			print self._DEBUG_INFO, 'Motor moving forward (%s)' % str((GPIO.LOW, GPIO.HIGH))

	def backward(self):
		''' Set the motor direction to backward '''
		GPIO.output(self.direction_channel_a, not self.backward_offset)
		GPIO.output(self.direction_channel_b, self.backward_offset)
		self.speed = self._speed
		if self._DEBUG:
			print self._DEBUG_INFO, 'Motor moving backward (%s)' % str((GPIO.HIGH, GPIO.LOW))

	def stop(self):
		''' Stop the motor by giving a 0 speed '''
		if self._DEBUG:
			print self._DEBUG_INFO, 'Motor stop'
		self.speed = 0
		GPIO.output(self.direction_channel_a, GPIO.LOW)
		GPIO.output(self.direction_channel_b, GPIO.LOW)

	@property
	def debug(self, debug):
		return self._DEBUG

	@debug.setter
	def debug(self, debug):
		''' Set if debug information shows '''
		if debug in (True, False):
			self._DEBUG = debug
		else:
			raise ValueError('debug must be "True" (Set debug on) or "False" (Set debug off), not "{0}"'.format(debug))

		if self._DEBUG:
			print self._DEBUG_INFO, "Set debug on"
		else:
			print self._DEBUG_INFO, "Set debug off"

	@property
	def pwm(self):
		return self._pwm

	@pwm.setter
	def pwm(self, pwm):
		if self._DEBUG:
			print self._DEBUG_INFO, 'pwm set'
		self._pwm = pwm


def test():
	import time

	print "********************************************"
	print "*                                          *"
	print "*                 L298N                    *"
	print "*                                          *"
	print "*          Connect MA to BCM17             *"
	print "*          Connect MB to BCM18             *"
	print "*         Connect PWMA to BCM27            *"
	print "*         Connect PWMB to BCM12            *"
	print "*                                          *"
	print "********************************************"
	GPIO.setmode(GPIO.BCM)
	GPIO.setup((5, 6), GPIO.OUT)
	GPIO.setup((13, 19), GPIO.OUT)
	a = GPIO.PWM(27, 60)
	b = GPIO.PWM(22, 60)
	a.start(0)
	b.start(0)

	def a_speed(value):
		a.ChangeDutyCycle(value)

	def b_speed(value):
		b.ChangeDutyCycle(value)

	motorA = Motor(5,6)
	motorB = Motor(13,19)
	motorA.debug = True
	motorB.debug = True
	motorA.pwm = a_speed
	motorB.pwm = b_speed

	delay = 0.05

	motorA.forward()
	for i in range(0, 101):
		motorA.speed = i
		time.sleep(delay)
	for i in range(100, -1, -1):
		motorA.speed = i
		time.sleep(delay)

	motorA.backward()
	for i in range(0, 101):
		motorA.speed = i
		time.sleep(delay)
	for i in range(100, -1, -1):
		motorA.speed = i
		time.sleep(delay)

	motorB.forward()
	for i in range(0, 101):
		motorB.speed = i
		time.sleep(delay)
	for i in range(100, -1, -1):
		motorB.speed = i
		time.sleep(delay)

	motorB.backward()
	for i in range(0, 101):
		motorB.speed = i
		time.sleep(delay)
	for i in range(100, -1, -1):
		motorB.speed = i
		time.sleep(delay)


if __name__ == '__main__':
	test()