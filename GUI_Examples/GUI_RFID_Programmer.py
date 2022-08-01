#!/usr/bin/env python3

########################################################################################################
# Program: GUI_Programmer.py
# Author: Tyler Tevis
# Created: 04/06/2020
# Build: 04/30/2020 @ 10:30AM
# Description: GUI Tool for NBC Production for programming Panosol 3D RFID Tags
########################################################################################################
# Notes:


import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

import os
import os.path
from os import path
import time
import sys
import signal
from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO


SN = str('P3D#')
requested_record = " "
yes_no_condition = 0
error_code = 0
alert_code = 0
bulbs = 10
CS = 0


class MainWindow(Gtk.Window):

	def __init__(self):
		Gtk.Window.__init__(self, title="P3D RFID Tag Programmer")
		self.set_border_width(20)
#		self.fullscreen()

		grid = Gtk.Grid()
		self.add(grid)

		program_button = Gtk.Button.new_with_label("PROGRAM UNIT")
		program_button.connect("clicked", self.program_button_clicked)
		grid.attach(program_button, 0, 0, 8, 3)

		read_button = Gtk.Button.new_with_label("READ A TAG")
		read_button.connect("clicked", self.read_button_clicked)
		grid.attach_next_to(read_button, program_button, 3, 8, 3)

		view_button = Gtk.Button.new_with_label("VIEW TAGS")
		view_button.connect("clicked", self.view_button_clicked)
		grid.attach_next_to(view_button, read_button, 3, 8, 3)

		exit_button = Gtk.Button.new_with_label("EXIT")
		exit_button.connect("clicked", self.exit_button_clicked)
		grid.attach_next_to(exit_button, view_button, 3, 8, 3)


	def program_button_clicked(self, widget):
		global yes_no_condition
		yes_no_condition = 1
		win = EnterSerialNumberWindow()
		win.connect("delete-event", self.destroy)
		win.show_all()


	def read_button_clicked(self, widget):
		# open window with this information on it
		global alert_code
		alert_code = 1
		win = AlertWindow()
		win.connect("delete-event", self.destroy)
		win.show_all()

	def view_button_clicked(self, widget):
		global yes_no_condition
		yes_no_condition = 2
		win = EnterSerialNumberWindow()
		win.connect("delete-event", self.destroy)
		win.show_all()

	def exit_button_clicked(self, widget):
		sys.exit(0)
		# os.system("sudo shutdown now")

	def select_device_write(self, CS, SerialNumber, Hours):
		data = str(SerialNumber + ':' + Hours)
		reader = SimpleMFRC522(CS)
		time.sleep(.25)
		reader.write(data)















class EnterSerialNumberWindow(Gtk.Window):

	def __init__(self):
		Gtk.Window.__init__(self, title="Enter Serial #")
		self.set_border_width(30)
#		self.fullscreen()


		grid = Gtk.Grid()
		self.add(grid)

		global SN
		SN = "P3D#"

		typed = Gtk.Button.new_with_label(SN)	# only shows initial value ("P3D#"), does not update
		typed.connect("clicked", self.typed_handler)
		grid.attach(typed, 0, 0, 3, 1)

		button_1 = Gtk.Button.new_with_label("  1  ")
		button_1.connect("clicked", self.button_1_clicked)
		grid.attach(button_1, 0, 1, 1, 1)

		button_2 = Gtk.Button.new_with_label("  2  ")
		button_2.connect("clicked", self.button_2_clicked)
		grid.attach_next_to(button_2, button_1, 1, 1,1)

		button_3 = Gtk.Button.new_with_label("  3  ")
		button_3.connect("clicked", self.button_3_clicked)
		grid.attach_next_to(button_3, button_2, 1, 1,1)

		button_4 = Gtk.Button.new_with_label("  4  ")
		button_4.connect("clicked", self.button_4_clicked)
		grid.attach_next_to(button_4, button_1, 3, 1,1)

		button_5 = Gtk.Button.new_with_label("  5  ")
		button_5.connect("clicked", self.button_5_clicked)
		grid.attach_next_to(button_5, button_4, 1, 1,1)

		button_6 = Gtk.Button.new_with_label("  6  ")
		button_6.connect("clicked", self.button_6_clicked)
		grid.attach_next_to(button_6, button_5, 1, 1,1)

		button_7 = Gtk.Button.new_with_label("  7  ")
		button_7.connect("clicked", self.button_7_clicked)
		grid.attach_next_to(button_7, button_4, 3, 1,1)

		button_8 = Gtk.Button.new_with_label("  8  ")
		button_8.connect("clicked", self.button_8_clicked)
		grid.attach_next_to(button_8, button_7, 1, 1,1)

		button_9 = Gtk.Button.new_with_label("  9  ")
		button_9.connect("clicked", self.button_9_clicked)
		grid.attach_next_to(button_9, button_8, 1, 1,1)

		button_0 = Gtk.Button.new_with_label("  0  ")
		button_0.connect("clicked", self.button_0_clicked)
		grid.attach_next_to(button_0, button_8, 3, 1,1)



		clear_button = Gtk.Button.new_with_label("CLEAR")
		clear_button.connect("clicked", self.clear_button_clicked)
		grid.attach(clear_button, 0, 4, 1, 1)

		enter_button = Gtk.Button.new_with_label("ENTER")
		enter_button.connect("clicked", self.enter_button_clicked)
		grid.attach(enter_button, 2, 4, 1, 1)


		exit_button = Gtk.Button.new_with_label("EXIT")
		exit_button.connect("clicked", self.exit_button_clicked)
		grid.attach_next_to(exit_button, clear_button, 3, 3, 1)


	def typed_handler(self, widget):
		print("test")

	def button_1_clicked(self, widget):
		global SN
		SN = SN + "1"
	def button_2_clicked(self, widget):
		global SN
		SN = SN + "2"
	def button_3_clicked(self, widget):
		global SN
		SN = SN + "3"
	def button_4_clicked(self, widget):
		global SN
		SN = SN + "4"
	def button_5_clicked(self, widget):
		global SN
		SN = SN + "5"
	def button_6_clicked(self, widget):
		global SN
		SN = SN + "6"
	def button_7_clicked(self, widget):
		global SN
		SN = SN + "7"
	def button_8_clicked(self, widget):
		global SN
		SN = SN + "8"
	def button_9_clicked(self, widget):
		global SN
		SN = SN + "9"
	def button_0_clicked(self, widget):
		global SN
		SN = SN + "0"

	def clear_button_clicked(self, widget):
		global SN
		SN = "P3D#"
		print(SN)

	def enter_button_clicked(self, widget):
		Gtk.Window.destroy(self)
		win = YesNoBox()
		win.connect("delete-event", self.destroy)
		win.show_all()

	def exit_button_clicked(self, widget):
		Gtk.Window.destroy(self)














class YesNoBox(Gtk.Window):

	def __init__(self):

		global SN, yes_no_condition

		self.directionLabel = Gtk.Label()
		self.infoLabel = Gtk.Label()
		info = " "

		# Serial Number entered to assign tags or view product's record
		windowTitle = "Confirm Serial Number: "
		info = "Serial Number: " + SN

		self.directionLabel.set_text(windowTitle)
		self.infoLabel.set_text(info)

		Gtk.Window.__init__(self, title=windowTitle)
		#self.fullscreen()


		no_button = Gtk.Button.new_with_label("  NO  ")
		no_button.connect("clicked", self.no_button_clicked)

		yes_button = Gtk.Button.new_with_label("  YES  ")
		yes_button.connect("clicked", self.yes_button_clicked)

		grid = Gtk.Grid()
		grid.attach(self.directionLabel, 0, 0, 3, 1)
		grid.attach(self.infoLabel, 0, 2, 3, 2)
		grid.attach(no_button, 0, 4, 1, 1)
		grid.attach(yes_button, 2, 4, 2, 1)
		self.add(grid)


	def no_button_clicked(self, widget):
		global SN, yes_no_condition
		SN = "P3D#"
		win = EnterSerialNumberWindow()
		win.connect("delete-event", self.destroy)
		win.show_all()
		Gtk.Window.destroy(self)

	def yes_button_clicked(self, widget):
		global SN, yes_no_condition, requested_record, bulbs, error_code, CS, alert_code
		# Serial Number confirmed for programming/assigning tags
		if yes_no_condition == 1:
				if SN == "P3D#":
					error_code = 1
					Gtk.Window.destroy(self)
					win = ErrorWindow()
					win.connect("delete-event", self.destroy)
					win.show_all()
				else:
					newRecord = "./ProgramFiles/" + SN + ".txt"
					try:
						alert_code = 2
						fWrite = open(newRecord, 'w+')
						for i in range(bulbs):
							self.select_device_write(CS, SN, "250.00")
							tag = self.select_device_read(CS)
							tid = self.get_ID(tag)
							data = self.get_data(tag)
							convert = ' ' + data + '\n'
							fWrite.write(str(tid))
							fWrite.write(convert)
							time.sleep(1)
							print("tag programmed -- implement alert window")
					finally:
						id_list = []
						fWrite.close()
						Gtk.Window.destroy(self)


		# Serial Number confirmed to view record of that unit
		if yes_no_condition == 2:
			requested_record = "./ProgramFiles/" + SN + ".txt"
			if path.exists(requested_record) == True:
				valid_SN = True
			else:
				valid_SN = False

			if valid_SN == True:
				Gtk.Window.destroy(self)
				win = RecordViewWindow()
				win.connect("delete-event", self.destroy)
				win.show_all()

			elif valid_SN == False:
				error_code = 2
				Gtk.Window.destroy(self)
				win = ErrorWindow()
				win.connect("delete-event", self.destroy)
				win.show_all()

	def get_ID(self, tag):
		id = int(tag[0])
		return id

	def get_data(self, tag):
		data = str(tag[1])
		data = data.rstrip()
		return data

	def select_device_read(self, CS):
		reader = SimpleMFRC522(CS)
		time.sleep(.25)
		tid, data = reader.read()
		tag = [tid, data]
		return tag

	def select_device_write(self, CS, SerialNumber, Hours):
		data = str(SerialNumber + ':' + Hours)
		reader = SimpleMFRC522(CS)
		time.sleep(.25)
		reader.write(data)
















class RecordViewWindow(Gtk.Window):

	def __init__(self):

		global requested_record
		Gtk.Window.__init__(self, title="Record File")
		self.set_default_size(800,400)
		self.box = Gtk.VBox()
		self.add(self.box)
#		self.fullscreen()

		scrolledWindow = Gtk.ScrolledWindow()
		scrolledWindow.set_hexpand(True)
		scrolledWindow.set_vexpand(True)

		self.textview = Gtk.TextView()
		self.textbuffer = self.textview.get_buffer()

		menu_button = Gtk.Button(label="RETURN TO MENU")
		menu_button.connect("clicked", self.menu_clicked)

		with open(requested_record, 'r') as f:
			data = f.read()
			self.textbuffer.set_text(data)

			scrolledWindow.add(self.textview)
			self.box.pack_start(scrolledWindow, True, True, 0)
			self.box.pack_end(menu_button, False, False, 5)


	def menu_clicked(self, widget):
#		win = MainWindow()
#		win.connect("delete-event", self.destroy)
#		win.show_all()
		Gtk.Window.destroy(self)














class AlertWindow(Gtk.Window):

	def __init__(self):
		global alert_code
		Gtk.Window.__init__(self, title="Alert")
		self.set_border_width(20)
        #self.fullscreen()

		self.alert = Gtk.Label()

		if alert_code == 1:
			text = "	Tag ID		S/N		Hours\n"
			read_tag = self.select_device_read(0)
			read_id = self.get_ID(read_tag)
			read_data = self.get_data(read_tag)
			to_display = text + str(read_id) + " " + read_data
			self.alert.set_text(to_display)


		if alert_code == 2:
			self.alert.set_text("Scan Next Tag")

		hbox = Gtk.Box(spacing=6)
		self.add(hbox)
		hbox.pack_start(self.alert, False, False, 0)

		ok_button = Gtk.Button.new_with_label("OK")
		ok_button.connect("clicked", self.ok_button_clicked)
		hbox.pack_start(ok_button, False, False, 0)

	def ok_button_clicked(self, widget):
		Gtk.Window.destroy(self)

	def get_ID(self, tag):
		id = int(tag[0])
		return id

	def get_data(self, tag):
		data = str(tag[1])
		data = data.rstrip()
		return data

	def select_device_read(self, CS):
		reader = SimpleMFRC522(CS)
		time.sleep(.25)
		tid, data = reader.read()
		tag = [tid, data]
		return tag



class ErrorWindow(Gtk.Window):

	def __init__(self):
		global error_code
		Gtk.Window.__init__(self, title="Error")
		self.set_border_width(20)
        # self.fullscreen()

		self.warning = Gtk.Label()

		# No serial number entered
		if error_code == 1:
			self.warning.set_text("No Serial Number Entered")

        # serial number not found  -> re-enter serial number
		if error_code == 2:
			self.warning.set_text("Serial Number Not Found")

		hbox = Gtk.Box(spacing=6)
		self.add(hbox)
		hbox.pack_start(self.warning, False, False, 0)

		ok_button = Gtk.Button.new_with_label("OK")
		ok_button.connect("clicked", self.ok_button_clicked)
		hbox.pack_start(ok_button, False, False, 0)


	def ok_button_clicked(self, widget):
		global SN, error_code
		if error_code == 1:
			win = EnterSerialNumberWindow()
			win.connect("delete-event", self.destroy)
			win.show_all()
#		if error_code == 2:
#			win = MainWindow()
#			win.connect("delete-event", self.destroy)
#			win.show_all()
		Gtk.Window.destroy(self)














#######################################################################
# MAIN -- JUST USED FOR LAUNCHING GTK.MainWindow
#######################################################################
win = MainWindow()
win.show_all()
Gtk.main()
#######################################################################
