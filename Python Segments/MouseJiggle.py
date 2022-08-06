#!/usr/bin/env python
# This script activates a servo motor to swing 120 degrees every 30 seconds to move a computer mouse
import RPi.GPIO as GPIO					# importing general purpose in/out (GPIO) library
import time						# import time library for sleep (delay)

servoPIN = 18						# enable/signal pins of servo, button and led mapped with variables.

GPIO.cleanup()
GPIO.setmode(GPIO.BOARD)				# declares numbering convention for GPIO ports on Raspberry Pi
GPIO.setup(servoPIN, GPIO.OUT)				# set servo motor as an output

GPIO.setwarnings(False)					# disables warnings from stopping program/breaking recursion

p = GPIO.PWM(servoPIN, 50)


while True:						# jiggles mouse every 30 seconds
	time.sleep(30)
	print("jiggle jiggle")
	p.start(7.5)
	time.sleep(2)
	p.ChangeDutyCycle(3.6)			# 3.6 duty cycle to move to squeezing position
	time.sleep(2)				# hold squeeze for 0.9 seconds
	p.ChangeDutyCycle(8.0)			# reset back to 90 degrees
	time.sleep(2)
	p.ChangeDutyCycle(3.6)
	p.stop()


#	GENERAL INSTRUCTIONS:
#  To run program at startup:
#	1. Open terminal with Ctrl+Alt+T
#	2. type "sudo nano /etc/rc.local"
#	3. before "exit 0" line, add "sudo python /home/pi/Dispenser/DISPENSER.py" (or whatever the file path is for the new device/Raspberry Pi where this program is located)
#	4. hit Ctrl+X then ENTER to save/exit.
#	5. type "sudo reboot now" to test if Dispenser program begins at startup.
#
#  Physical Pin Map:
#	Servo Motor (3 wires: red, brown, yellow):
#		Red (power): red wire to either of Raspberry Pi's 5V connections (pin 2 or 4)
#		Brown (GND): brown wire to any of Raspberry Pi's GND pins (pin 6, 9, 14, 20, 25, 30, 34 or 39)
#		Yellow (signal): yellow wire to GPIO 24 (pin 18)
