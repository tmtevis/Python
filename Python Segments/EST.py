#!/usr/bin/env python
# Experimental Cat Toy (ECT)

import RPi.GPIO as GPIO					# importing general purpose in/out (GPIO) library
import time						# import time library for sleep (delay)

servoPIN = 18						# enable/signal pins of servo, button and led mapped with variables.
btnPIN = 11
ledPIN = 16

GPIO.setmode(GPIO.BOARD)				# declares numbering convention for GPIO ports on Raspberry Pi
GPIO.setup(servoPIN, GPIO.OUT)				# set servo motor as an output
GPIO.setup(btnPIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)	# set up button as resistive pull-down (connect to RPi's 3.3V pin)
GPIO.setup(ledPIN, GPIO.OUT)				# set LED as output

GPIO.setwarnings(False)					# disables warnings from stopping program/breaking recursion

while True:						# continuous loop to keep checking for button press
	if GPIO.input(btnPIN) == GPIO.HIGH:		# if the button is pressed:
		GPIO.OUTPUT(ledPIN, GPIO.HIGH)		# turn on the LED to let operator know device is busy
		p = GPIO.PWM(servoPIN, 50)		# start pulse width modulation for servo motor at 50Hz
		p.start(7.5)				# 7.5 duty cycle to start at 90 degrees
		time.sleep(2)				# delay to allow servo to settle
		p.ChangeDutyCycle(3.6)			# 3.6 duty cycle to move to squeezing position
		time.sleep(0.9)				# hold squeeze for 0.9 seconds
		p.ChangeDutyCycle(7.5)			# reset back to 90 degrees
		time.sleep(1)				# delay to allow servo to settle
		p.stop()				# stop servo
		GPIO.OUTPUT(ledPIN, GPIO.LOW)		# turn off LED when finished and ready for another button press


#	GENERAL INSTRUCTIONS:
#  To run program at startup:
#	1. Open terminal with Ctrl+Alt+T
#	2. type "sudo nano /etc/rc.local"
#	3. before "exit 0" line, add "sudo python /home/pi/Dispenser/DISPENSER.py" (or whatever the file path is for the new device/Raspberry Pi where this program is located)
#	4. hit Ctrl+X then ENTER to save/exit.
#	5. type "sudo reboot now" to test if Dispenser program begins at startup.
#
#  Physical Pin Map: (see pinout picture in TEMP-148 folder or type "pinout" in terminal)
#	Button (reversable, sides do not matter):
#		1st side: button to GPIO 11 (pin 23)
#		2nd side: button to 330 Ohm resistor to Raspberry Pi's 3.3V connection (pin 1 or pin 17)
#
#	LED (longer side is positive):
#		positive: LED to GPIO 23 (pin 16)
#		negative: LED to 330 Ohm resistor to Raspberry Pi's GND pin (pin 6, 9, 14, 20, 25, 30, 34 or 39)
#
#	Servo Motor (3 wires: red, brown, yellow):
#		Red (power): red wire to either of Raspberry Pi's 5V connections (pin 2 or 4)
#		Brown (GND): brown wire to any of Raspberry Pi's GND pins (pin 6, 9, 14, 20, 25, 30, 34 or 39)
#		Yellow (signal): yellow wire to GPIO 24 (pin 18)
