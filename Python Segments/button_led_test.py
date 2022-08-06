#!/usr/bin/env python3

import RPi.GPIO as GPIO					# importing general purpose in/out (GPIO) library
import time						# import time library for sleep (delay)
import signal
import sys

GPIO.setwarnings(False)

def signal_handler(sig, frame):
	print("\nProgram Successfully Terminated")
	GPIO.cleanup()
	sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

btnPIN = 16
ledPIN = 18

GPIO.setmode(GPIO.BOARD)				# declares numbering convention for GPIO ports on Raspberry Pi
GPIO.setup(btnPIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)	# set up button as resistive pull-down (connect to RPi's 3.3V pin)
GPIO.setup(ledPIN, GPIO.OUT)				# set LED as output
try:
	while True:						# continuous loop to keep checking for button press
		if GPIO.input(btnPIN) == GPIO.HIGH:		# if the button is pressed:
			GPIO.output(ledPIN, GPIO.HIGH)		# turn on the LED to let operator know device is busy
			time.sleep(2)				# delay to allow servo to settle
			GPIO.output(ledPIN, GPIO.LOW)		# turn off LED when finished and ready for another button press
			sys.exit(0)
finally:
	GPIO.cleanup()
