#!/usr/bin/env python3

import RPi.GPIO as GPIO					# importing general purpose in/out (GPIO) library
import time						# import time library for sleep (delay)
import signal
import sys

def signal_handler(sig, frame):
	print("\nExiting Program...")
	sys.exit(0)

servoPIN = 11						# enable/signal pins of servo, button and led mapped with variables.

GPIO.setmode(GPIO.BOARD)				# declares numbering convention for GPIO ports on Raspberry Pi
GPIO.setup(servoPIN, GPIO.OUT)				# set servo motor as an output

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


GPIO.setwarnings(False)					# disables warnings from stopping program/breaking recursion

while True:
	try:
		p = GPIO.PWM(servoPIN, 50)		# start pulse width modulation for servo motor at 50Hz
		p.start(7.5)				# 7.5 duty cycle to start at 90 degrees
		time.sleep(2)				# delay to allow servo to settle
		p.ChangeDutyCycle(3.6)			# 3.6 duty cycle to move to squeezing position
		time.sleep(0.9)				# hold squeeze for 0.9 seconds
		p.ChangeDutyCycle(7.5)			# reset back to 90 degrees
		time.sleep(1)				# delay to allow servo to settle
		p.stop()				# stop servo
		GPIO.OUTPUT(ledPIN, GPIO.LOW)		# turn off LED when finished and ready for another button press
	finally:
		GPIO.cleanup()
		sys.exit(0)


#	Servo Motor (3 wires: red, brown, yellow):
#		Red (power): red wire to either of Raspberry Pi's 5V connections (pin 2 or 4)
#		Brown (GND): brown wire to any of Raspberry Pi's GND pins (pin 6, 9, 14, 20, 25, 30, 34 or 39)
#		Yellow (signal): yellow wire to GPIO 24 (pin 18)
