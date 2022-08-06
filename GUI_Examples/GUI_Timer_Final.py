#!/usr/bin/env python3

########################################################################################################
# Program: Merge_GUI.py
# Author: Tyler Tevis
# Created: 03/21/2020
# Build: 4/30/20 @ 10:00 AM
# Description: Merges several GUI files into one to make a functional program.
########################################################################################################
# Notes:
# Create timeout feature to prevent program hang if SPI stops working



# Global Variables:
# yes_no_condition
# 1 - Confirming Treatment
# 2 - Confirming Serial Number
# 3 - Proceed with unrecognized bulbs

# error_code
# 1 - Treatment entered is 0:00
# 2 - File not found

# alert_code
# 1 - Finished programming after reset


import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango, GObject
import threading
import os
import os.path
from os import path
import datetime
import time
import sys
import signal
from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO

# Global Variables #
SN = str('P3D#1234')
valid_SN = False
bulbs = 1
alert_code = 0
yes_no_condition = 0
install = False
firmware = "1.0.3"
current_bulb_num = 0
selected_file = " "











class InitialWindow(Gtk.Window):

	def __init__(self):
		Gtk.Window.__init__(self, title="Warning")
#		self.fullscreen()

		global bulbs
		bulbs = self.get_num_bulbs()

		grid = Gtk.Grid()
		self.add(grid)

		self.message = Gtk.Label()
		self.message.set_text("1TM-XXX TIMER PROTOTYPE v1.0\n\nWARNING: ULTRAVIOLET RADIATION -\nFOLLOW INSTRUCTIONS. FAILURE TO USE\nPROTECTIVE EYEWEAR MAY RESULT IN\nSEVERE BURNS OR OTHER EYE INJURY.\nIF DISCOMFORT DEVELOPS, DISCONTINUE\nUSE AND CONSULT A PHYSICIAN.\n\nAN ATTENDANT IS TO BE PRESENT WHEN\nTHIS DEVICE IS IN OPERATION.\nTHIS DEVICE IS TO BE USED BY ONE (1)\nPERSON PER TREATMENT.\n\nCAUTION: FEDERAL LAW RESTRICTS THIS\nDEVICE TO SALE BY OR ON THE\nORDER OF A PHYSICIAN.\n")
		grid.attach(self.message, 1, 0, 4, 1)

		space_label = Gtk.Label()
		space_label.set_text("                      ")
		grid.attach(space_label, 1, 1, 4, 1)

		check_box = Gtk.CheckButton.new_with_label(label="I Understand")
		check_box.connect("toggled", self.check_box_toggled)
		grid.attach_next_to(check_box, space_label, 3, 4, 1)

		ok_button = Gtk.Button.new_with_label("BEGIN TREATMENT")
		ok_button.connect("clicked", self.ok_button_clicked)
		grid.attach_next_to(ok_button, check_box, 3, 4, 2)
		self.agree = False


	def get_num_bulbs(self):
		global SN
		fName = "./ProgramFiles/" + SN + ".txt"
		try:
			f = open(fName, 'r+')
			count = 0
			for line in f:
				count = count + 1
		finally:
			f.close()
		print("\nNUMBER OF TAGS REGISTERED: ", count)
		return count

	def check_box_toggled(self, widget):

		if self.agree == False:
			self.agree = True
		elif self.agree == True:
			self.agree = False

	def ok_button_clicked(self, widget):
		valid = False
		passed = False
                                                # Performing BulbCheck
		if self.agree == True:					# agree box is checked
			for i in range(bulbs):				# determines number of readers to poll; defined by the global variable 'bulbs'
				checked = self.check_tag(i)		# checked returns result of check_tag function for the reader in the i-th position
				time.sleep(.25)
				if checked == True:
					passed = True
					continue
				elif checked == False:
					passed = False
					break

		if passed == False and self.agree == True:
			global yes_no_condition
			yes_no_condition = 3
			win = YesNoBox()
			win.connect("delete-event", self.destroy)
			win.show_all()
			Gtk.Window.destroy(self)

		if passed == True and self.agree == True:
			win = MainMenu()
			win.connect("delete-event", self.destroy)
			win.show_all()
			Gtk.Window.destroy(self)


	def select_device_read(self, CS):
		reader = SimpleMFRC522(CS)
		time.sleep(.25)
		tid, data = reader.read()
		tag = [tid, data]
		return tag

	def get_ID(self, tag):
		id = int(tag[0]) # takes first element of tag object for tag id
		return id

	def get_data(self, tag):
		data = str(tag[1]) # cast second element of tag object as string
		data = data.rstrip() # return copy of string without trailing characters (gets rid of spaces)
		return data


	def check_tag(self, CS):
		global SN
		result = False
		fileName = "./ProgramFiles/" + SN + ".txt"

		read_tag = self.select_device_read(CS)			# get tag info as TAG object from selected CS
		read_tag_id = self.get_ID(read_tag)				# parse TAG object for ID
		f= open(fileName, 'r+')

		for line in f:									# for each line in the record file
			tag_from_record = [line.split()] 			# get a line and break it up into the format [ 'tag id' , 'data' ]
			tag_from_record_id = int(tag_from_record[0][0]) 	# pull TAG ID from created tag object
			if (tag_from_record_id == read_tag_id): 	# TAG ID matches records
				result = True							# result set to true; break and return result as True to prevent it from continuing after match
				break
			elif (tag_from_record_id != read_tag_id): # TAG ID does not match records
				continue								# try next line; will eventually fall out with result still being False
		f.close()
		return result














class MainMenu(Gtk.Window):

	def __init__(self):
		Gtk.Window.__init__(self, title="P3D Timer")
		self.set_border_width(30)
        #self.fullscreen()

		grid = Gtk.Grid()
		self.add(grid)

		treat_button = Gtk.Button.new_with_label("BEGIN TREATMENT")
		treat_button.connect("clicked", self.treat_button_clicked)
		grid.attach(treat_button, 0, 0, 8, 2)

#		view_button = Gtk.Button.new_with_label("VIEW BULB LIFE")
#		view_button.connect("clicked", self.view_button_clicked)
#		grid.attach_next_to(view_button, treat_button, 3, 4, 2)

		past_button = Gtk.Button.new_with_label("PAST TREATMENTS")
		past_button.connect("clicked", self.past_button_clicked)
		grid.attach_next_to(past_button, treat_button, 3, 4, 2)

		maint_button = Gtk.Button.new_with_label("MAINTENANCE MODE")
		maint_button.connect("clicked", self.maint_button_clicked)
		grid.attach_next_to(maint_button, past_button, 1, 4, 2)

		order_button = Gtk.LinkButton.new_with_label("http://www.nationalbiological.com", "Order New Bulbs")
		grid.attach_next_to(order_button, past_button, 3, 8, 2)

		exit_button = Gtk.Button.new_with_label("SHUT DOWN UNIT")
		exit_button.connect("clicked", self.exit_button_clicked)
		grid.attach_next_to(exit_button, order_button, 3, 8, 2)

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

	def treat_button_clicked(self, widget):
		# check bulb tags (get amount of bulbs utilizted from initial state) --> count entries in .txt file
		# open window to input treatment time in the format 00:00  --> use one of those +/- boxes
		win = SetTreatmentTimeWindow()
		win.connect("delete-event", self.destroy)
		win.show_all()

		# close out to main menu


	def maint_button_clicked(self, widget):
		win = EnterSerialNumberWindow()
		win.connect("delete-event", self.destroy)
		win.show_all()

	def view_button_clicked(self, widget):
		# open window with average time remaining of bulb set or individually
		# click okay to close and go back to main menu
		win = FetchingBulbInfoWindow()
		win.connect("delete-event", self.destroy)
		win.show_all()
		Gtk.Window.destroy(self)


	def past_button_clicked(self, widget):
		dialog = Gtk.FileChooserDialog(
			title="Please Choose a File",
			parent=self,
			action=Gtk.FileChooserAction.OPEN,
			buttons=(
			Gtk.STOCK_CANCEL,
			Gtk.ResponseType.CANCEL,
			Gtk.STOCK_OPEN,
			Gtk.ResponseType.OK,
			),
		)
		self.add_filters(dialog)
		# restrict to local directory
#		self.set_local_only()

		response = dialog.run()

		if response == Gtk.ResponseType.OK:
			print("Open Clicked")
			print("File Selected: " + dialog.get_filename())
			global selected_file
			selected_file =  dialog.get_filename()
			win = RecordViewWindow()
			win.connect("delete-event", self.destroy)
			win.show_all()
			Gtk.Window.destroy(self)

		elif response == Gtk.ResponseType.CANCEL:
			print("Cancel Clicked")
		dialog.destroy()


	def add_filters(self, dialog):
		filter_text = Gtk.FileFilter()
		filter_text.set_name("Text files")
		filter_text.add_mime_type("text/plain")
		dialog.add_filter(filter_text)


	def menu_clicked(self, widget):
		win = MainMenu()
		win.connect("delete-event", self.destroy)
		win.show_all()
		Gtk.Window.destroy(self)


	def exit_button_clicked(self, widget):
		# should shut down unit when moved outside of testing environment
		# os.system("sudo shutdown now")
		sys.exit(0)














class SetTreatmentTimeWindow(Gtk.Window):

	def __init__(self):
		Gtk.Window.__init__(self, title="Set Treatment Time")
		self.set_border_width(10)
        #self.fullscreen()

		min_adj = Gtk.Adjustment(value=0, lower=0, upper=5, step_increment=1, page_increment=5, page_size=0)
		sec_adj = Gtk.Adjustment(value=0, lower=0, upper=60, step_increment=1, page_increment=5, page_size=0)

		self.spin_min = Gtk.SpinButton(adjustment=min_adj, climb_rate=1, digits=0)
		self.spin_min.set_adjustment(min_adj)

		self.spin_sec = Gtk.SpinButton(adjustment=sec_adj, climb_rate=1, digits=0)
		self.spin_sec.set_adjustment(sec_adj)

		self.instruction_label = Gtk.Label()
		self.instruction_label.set_text("Enter Treatment Time")

		self.min_label = Gtk.Label()
		self.min_label.set_text(" min")

		self.sec_label = Gtk.Label()
		self.sec_label.set_text(" sec")

		self.cancel_button = Gtk.Button.new_with_label("CANCEL")
		self.cancel_button.connect("clicked", self.cancel_clicked)

		self.enter_button = Gtk.Button.new_with_label("ENTER")
		self.enter_button.connect("clicked", self.enter_clicked)

		grid = Gtk.Grid()
		grid.attach(self.instruction_label, 0, 0, 4, 1)
		grid.attach(self.spin_min, 0, 1, 1, 1)
		grid.attach(self.min_label,1, 1, 1, 1)
		grid.attach(self.spin_sec, 2, 1, 1, 1)
		grid.attach(self.sec_label,3, 1, 1, 1)
		grid.attach_next_to(self.cancel_button, self.spin_min, 3, 4, 1)
		grid.attach_next_to(self.enter_button,self.cancel_button, 3, 4, 1)
		self.add(grid)

	def cancel_clicked(self, Widget):
		Gtk.Window.destroy(self)

	def enter_clicked(self, Widget):
		global min_chosen, sec_chosen
		global yes_no_condition, error_code
		yes_no_condition = 1

		min_chosen = self.spin_min.get_value_as_int()
		sec_chosen = self.spin_sec.get_value_as_int()
		print("Treatment Time --> Minutes: ",min_chosen, "  Seconds: ", sec_chosen)

		if min_chosen == 0 and sec_chosen == 0:
		# Treatment cannot be 0:00 Error
			error_code = 1
			Gtk.Window.destroy(self)
			win = ErrorWindow()
			win.connect("delete-event", self.destroy)
			win.show_all()
		else:
			Gtk.Window.destroy(self)
			win = YesNoBox()
			win.connect("delete-event", self.destroy)
			win.show_all()














class TreatmentWindow(Gtk.Window):

	def __init__(self):
		global min_chosen, sec_chosen
		self.min_remaining = min_chosen
		self.sec_remaining = sec_chosen

		self.treatment_seconds = (self.min_remaining * 60) + self.sec_remaining


		# SETUP LED FOR USE IN TESTING #
		self.LEDpin = 37
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(self.LEDpin, GPIO.OUT)

		self.timer = None
		self.event = None

		if sec_chosen > 9:
			sec_printed = str(sec_chosen)
		if sec_chosen < 10:
			sec_printed = "0" + str(sec_chosen)

		self.clock = str(min_chosen) + ":" + sec_printed

		Gtk.Window.__init__(self, title="Treatment")
		self.set_border_width(20)
        # self.fullscreen()

		self.start_button = Gtk.Button(label="Start")
		self.start_button.connect("clicked", self.start_timer)

		self.stop_button = Gtk.Button(label="STOP")
		self.stop_button.connect("clicked", self.stop_timer)

		self.exit_button = Gtk.Button(label="EXIT")
		self.exit_button.connect("clicked", self.exit_clicked)

		self.status = Gtk.Label()
		self.status.set_text(self.clock)
        # TEST THIS
		FONT = "Tahoma 48"
		description = Pango.font_description_from_string(FONT)
		self.status.override_font(description)

		self.vbox = Gtk.VBox()

		self.vbox.pack_start(self.start_button, False, False, 5)
		self.vbox.pack_end(self.status, True, True, 5)
		self.vbox.pack_start(self.stop_button, False, False, 5)
		self.vbox.pack_start(self.exit_button, False, False, 5)

		self.add(self.vbox)


	def update_time(self, seconds):
		self.status.set_text(self.clock)


	def get_time(self):
		self.update_treatment_time()
		while not self.event.is_set() and self.min_remaining >= 0 and self.sec_remaining >= 0:
			time.sleep(1)
			self.treatment_seconds -= 1
			print(self.treatment_seconds)
			self.clock = str(datetime.timedelta(seconds = self.treatment_seconds))
			self.update_time(self.treatment_seconds)

			if self.treatment_seconds == 0:
				self.min_remaining = 0
				self.sec_remaining = 0
				GPIO.output(self.LEDpin, GPIO.LOW)		# TURN LED OFF
				self.finished()
				self.event.set()
		if self.min_remaining == 0 and self.sec_remaining == 0:
			self.event.set()


	def update_treatment_time(self):

		print("Treatment Seconds Remaining: ", self.treatment_seconds)
		print("Initial Min Value: ", self.min_remaining)
		print("Initial Sec Value: ", self.sec_remaining)

		if self.treatment_seconds / 60 > 0:
			self.min_remaining = (self.treatment_seconds // 60)
			self.sec_remaining = self.treatment_seconds - (self.min_remaining * 60)
		else:
			self.min_remaining = 0
			self.sec_remaining = self.treatment_seconds

		print("Minutes Remaining: ", self.min_remaining)
		print("Seconds Remaining: ", self.sec_remaining)




	def start_timer(self, button):
		if self.min_remaining >= 0 and self.sec_remaining > 0:
			GPIO.output(self.LEDpin, GPIO.HIGH)
			# TURN LED ON
			self.timer = threading.Thread(target=self.get_time)
			self.event = threading.Event()
			self.timer.daemon=True
			self.timer.start()

		else:
			print("test")


	def stop_timer(self, button):
		GPIO.output(self.LEDpin, GPIO.LOW)		# TURN LED OFF
		self.event.set()
#		self.timer = None


	def exit_clicked(self, button):
		GPIO.output(self.LEDpin, GPIO.LOW)		# TURN LED OFF
		Gtk.Window.destroy(self)

	def finished(self):
		self.event.set()
		self.timer = None
		global firmware, min_chosen, sec_chosen, SN, bulbs

		date = time.strftime("%m_%d_%Y")
		daytime = time.strftime("%X")

		if bulbs == 10:
			configuration = "\nConfiguration: 10 Lamps - Full Array"
		elif bulbs == 4:
			configuration = "\nConfiguration: 4 Lamps - Doors Only"
		elif bulbs == 2:
			configuration = "\nConfiguration: 2 Lamps - Testing Virtual CS"
		elif bulbs == 1:
			configuration = "\nConfiguration: 1 Lamp - Testing"

		current_hours = self.get_hours(self.select_device_read(0))
		current_seconds = current_hours * 3600
		treatment_in_seconds = (min_chosen * 60) + sec_chosen
		hours_remaining = (current_seconds - treatment_in_seconds) / 3600
		hours_remaining_rounded = round(hours_remaining, 3)
		str_hours_remaining = str(hours_remaining_rounded)
		print("Hours Remaining: ", hours_remaining_rounded)

   		# National Biological Corporation
		# Panosol 3D Enhanced Edition
		# Firmware Version: 1.00
		# Treatment Date: 04/15/2020
		# Treatment Time: 2:17 PM
		# Duration: 2 minute(s) 34 second(s)
		# Configuration: Directional 6-Bulb
		# Bulb Information (Left to Right):
        	# Tag ID	   S/N	   Hours
		to_write = "National Biological Corporation\nPanosol 3D Enhanced Edition\nFirmware Version " + firmware + "\nTreatment Date: " + date + "\nTreatment Time: " + daytime + "\nDuration: " + str(min_chosen) + " minute(s) " + str(sec_chosen) + " second(s)" + configuration + "\nBulb Information (Indexed From Left to Right)\n\n  #       Tag ID         S/N          Hours\n____________________________________\n"
		record_name = "./Logs/Treatment_" + date + "_" + daytime + ".txt"

#		try:
		f = open(record_name, "w+")
		f.write(to_write)
		for i in range(bulbs):
			read_id = self.get_ID(self.select_device_read(i))
			time.sleep(.5)
			self.select_device_write(i, SN, str_hours_remaining)
			to_file = str(i+1) + " - " + str(read_id) + " " + SN + ":" + str_hours_remaining + "\n"
			f.write(to_file)
#		finally:
		global alert_code
		alert_code = 5
		f.close()

		# 26668714735 P3D#1234:999.95
		# 72666871475 P3D#1234:999.95
		# 72666871475 P3D#1234:999.95
		# 72666871475 P3D#1234:999.95
		# 72666871475 P3D#1234:999.95
		# 72666871475 P3D#1234:999.95

	def select_device_write(self, CS, SerialNumber, Hours):
		data = str(SerialNumber + ':' + Hours)
		reader = SimpleMFRC522(CS)
		time.sleep(.25)
		reader.write(data)

	def select_device_read(self, CS):
		reader = SimpleMFRC522(CS)
		time.sleep(.25)
		tid, data = reader.read()
		tag = [tid, data]
		return tag

	def get_ID(self, tag):
		id = int(tag[0])
		return id

	def get_data(self, tag):
		data = str(tag[1])
		data = data.rstrip()
		return data

	def get_hours(self, tag):
		data = self.get_data(tag)
		split = data.rsplit(':', 1)
		hours = float(split[1])
		return hours














class FetchingBulbInfoWindow(Gtk.Window):
	def __init__(self):
		Gtk.Window.__init__(self, title="Opening...")
		self.set_border_width(10)

		text = "Fetching Bulb Information"
		self.message = Gtk.Label()
		self.message.set_text(text)

		vbox = Gtk.VBox()
		self.vbox.pack_start(self.message, True, True, 0)
		self.add(self.vbox)

		#time.sleep(1)
		#text = text + "."

		time.sleep(3)
		win = ViewBulbLifeWindow()
		win.connect("delete-event", self.destroy)
		win.show_all()
		Gtk.Window.destroy(self)














class ViewBulbLifeWindow(Gtk.Window):
	def __init__(self):

		global SN
		serialTitle = SN
		Gtk.Window.__init__(self, title=serialTitle)
		self.set_border_width(10)
		#self.fullscreen()
		vbox = Gtk.VBox(orientation=Gtk.Orientation.VERTICAL, spacing=6)
		self.add(vbox)

		self.percentbar = Gtk.ProgressBar()
		percentage = self.get_life_percentage()
		self.percentbar.set_fraction(percentage)
		self.vbox.pack_start(self.progress_bar, True, True, 0)

		self.message = Gtk.Label()
		message_contents = "Remaining Bulb Life: " + str(percentage) + "%"
		self.message.set_text(message_contents)
		self.vbox.pack_start(self.message, True, True, 0)


	def get_life_percentage(self):
		try:
			hours = self.get_hours(self.select_device_read(0))
		finally:
			remaining = float(hours / 1000.00)
			return remaining

	def select_device_read(self, CS):
		reader = SimpleMFRC522(CS)
		time.sleep(.25)
		tid, data = reader.read()
		tag = [tid, data]
		return tag

	def get_data(self, tag):
		data = str(tag[1])
		data = data.rstrip()
		return data

	def get_hours(self, tag):
		data = get_data(tag)
		split = data.rsplit(':', 1)
		hours = float(split[1])
		return hours













class RecordViewWindow(Gtk.Window):

	def __init__(self):
		global selected_file

		Gtk.Window.__init__(self, title="Record File")
		self.set_default_size(800,400)
		self.box = Gtk.VBox()
		self.add(self.box)

		menu_button = Gtk.Button(label="MENU")
		menu_button.connect("clicked", self.menu_clicked)

		scrolledwindow = Gtk.ScrolledWindow()
		scrolledwindow.set_hexpand(True)
		scrolledwindow.set_vexpand(True)

		self.textview = Gtk.TextView()
		self.textbuffer = self.textview.get_buffer()

		with open(selected_file, 'r') as f:
			data = f.read()
			self.textbuffer.set_text(data)

		scrolledwindow.add(self.textview)
		self.box.pack_start(scrolledwindow, True, True, 0)
		self.box.pack_end(menu_button, False, False, 5)


	def menu_clicked(self, widget):
		win = MainMenu()
		win.connect("delete-event", self.destroy)
		win.show_all()
		Gtk.Window.destroy(self)














class MaintenanceWindow(Gtk.Window):

	def __init__(self):
		Gtk.Window.__init__(self, title="Maintenance")
		self.vbox = Gtk.VBox(spacing=6)
        #self.fullscreen()

		self.message = Gtk.Label()
		self.message.set_text("1TM-XXX Timer Maintenance Mode\n")

		self.relamp_button = Gtk.Button(label="Relamp Unit")
		self.relamp_button.connect("clicked", self.relamp_clicked)

		check_door_lamps = Gtk.CheckButton.new_with_label(label="Door Lamps Only (4)")
		check_door_lamps.connect("toggled", self.check_doors_toggled)

		check_all_lamps = Gtk.CheckButton.new_with_label(label="All Lamps (10)")
		check_all_lamps.connect("toggled", self.check_all_toggled)

		reset_hours = Gtk.Button(label="Reset Lamp Hours")
		reset_hours.connect("clicked", self.reset_clicked)

		exit_button = Gtk.Button.new_with_label("EXIT")
		exit_button.connect("clicked", self.exit_button_clicked)

		self.door_lamps = False
		self.all_lamps = True

		self.vbox.pack_start(self.message, False, False, 5)
		self.vbox.pack_start(self.relamp_button, False, False, 5)
		self.vbox.pack_start(check_door_lamps, False, False, 5)
		self.vbox.pack_start(check_all_lamps, False, False, 5)
		self.vbox.pack_start(reset_hours, False, False, 5)
		self.vbox.pack_start(exit_button, False, False, 5)

		self.add(self.vbox)

	def select_device_write(self, CS, SerialNumber, Hours):
		data = str(SerialNumber + ':' + Hours)
		reader = SimpleMFRC522(CS)
		time.sleep(.25)
		reader.write(data)

	def check_doors_toggled(self, widget):
		global bulbs
		bulbs = 4

	def check_all_toggled(self, widget):
		global bulbs
		bulbs = 10

	def relamp_clicked(self, widget):
		global alert_code
		alert_code = 2
		Gtk.Window.destroy(self)
		win = AlertWindow()
		win.connect("delete-event", self.destroy)
		win.show_all()
		Gtk.Window.destroy(self)

	def reset_clicked(self, widget):
		global SN, bulbs, alert_code
		for i in range(bulbs):
			self.select_device_write(i, SN, '250.00')

		alert_code = 1
		win = AlertWindow()
		win.connect("delete-event", self.destroy)
		win.show_all()
		Gtk.Window.destroy(self)

	def exit_button_clicked(self, widget):
		Gtk.Window.destroy(self)














class EnterSerialNumberWindow(Gtk.Window):

	def __init__(self):
		Gtk.Window.__init__(self, title="Enter Serial Number")
        #self.fullscreen()
		grid = Gtk.Grid()
		self.add(grid)

		global SN
		SN = "P3D#"
		typed = Gtk.Button.new_with_label(SN)
		typed.connect("clicked", self.typed_handler)
		grid.attach(typed, 0, 0, 3, 1)

		button_1 = Gtk.Button.new_with_label("1")
		button_2 = Gtk.Button.new_with_label("2")
		button_3 = Gtk.Button.new_with_label("3")
		button_4 = Gtk.Button.new_with_label("4")
		button_5 = Gtk.Button.new_with_label("5")
		button_6 = Gtk.Button.new_with_label("6")
		button_7 = Gtk.Button.new_with_label("7")
		button_8 = Gtk.Button.new_with_label("8")
		button_9 = Gtk.Button.new_with_label("9")
		button_0 = Gtk.Button.new_with_label("0")

		space_label = Gtk.Label()
		space_label.set_text("                      ")
		ok_button = Gtk.Button.new_with_label("OK")
		exit_button = Gtk.Button.new_with_label("EXIT")

		button_1.connect("clicked", self.button_1_clicked)
		button_2.connect("clicked", self.button_2_clicked)
		button_3.connect("clicked", self.button_3_clicked)
		button_4.connect("clicked", self.button_4_clicked)
		button_5.connect("clicked", self.button_5_clicked)
		button_6.connect("clicked", self.button_6_clicked)
		button_7.connect("clicked", self.button_7_clicked)
		button_8.connect("clicked", self.button_8_clicked)
		button_9.connect("clicked", self.button_9_clicked)
		button_0.connect("clicked", self.button_0_clicked)
		ok_button.connect("clicked", self.ok_button_clicked)
		exit_button.connect("clicked", self.exit_button_clicked)

		grid.attach(button_1, 0, 1, 1, 1)
		grid.attach_next_to(button_2, button_1, 1, 1, 1)
		grid.attach_next_to(button_3, button_2, 1, 1, 1)
		grid.attach_next_to(button_4, button_1, 3, 1, 1)
		grid.attach_next_to(button_5, button_4, 1, 1, 1)
		grid.attach_next_to(button_6, button_5, 1, 1, 1)
		grid.attach_next_to(button_7, button_4, 3, 1, 1)
		grid.attach_next_to(button_8, button_7, 1, 1, 1)
		grid.attach_next_to(button_9, button_8, 1, 1, 1)
		grid.attach_next_to(button_0, button_8, 3, 1, 1)

		grid.attach(space_label, 0, 4, 3, 1)
		grid.attach_next_to(ok_button, space_label, 3, 3, 3)
		grid.attach_next_to(exit_button, ok_button, 3, 3, 3)

	def typed_handler(self, widget):
		print("test")
		# try to find a way to update as numbers are being typed

	def button_0_clicked(self, widget):
		global SN
		SN = SN + "0"
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

	def ok_button_clicked(self, widget):
		global SN, yes_no_condition
		if SN == "P3D#":
			print("no SN entered")
		else:
			yes_no_condition = 2
			Gtk.Window.destroy(self)
			win = YesNoBox()
			win.connect("delete-event", self.destroy)
			win.show_all()

	def exit_button_clicked(self, widget):
		global SN
		SN = str('P3D#')
		Gtk.Window.destroy(self)














class AlertWindow(Gtk.Window):

	def __init__(self):
		global alert_code
		Gtk.Window.__init__(self, title="Alert")
		self.set_border_width(20)
        #self.fullscreen()

		self.alert = Gtk.Label()

		if alert_code == 1:
			self.alert.set_text("RFID Tag Operation Complete")

		if alert_code == 2:
			self.alert.set_text("Remove Lamps Now")

		if alert_code == 3:
			self.alert.set_text("Install New Lamps and Press OK to Continue")

		if alert_code == 4:
			self.alert.set_text("Tag Already Registered. Press OK to Scan Another")
			alert_code = 3

		if alert_code == 5:
			self.alert.set_text("Treatment Complete")


		hbox = Gtk.Box(spacing=6)
		self.add(hbox)
		hbox.pack_start(self.alert, False, False, 0)

		ok_button = Gtk.Button.new_with_label("OK")
		ok_button.connect("clicked", self.ok_button_clicked)
		hbox.pack_start(ok_button, False, False, 0)


	def ok_button_clicked(self, widget):
		global alert_code, install
		go = True
		while go:

			if alert_code == 1:
				win = MaintenanceWindow()
				win.connect("delete-event", self.destroy)
				win.show_all()
				go = False

			if alert_code == 2:
				alert_code = 3
				win = AlertWindow()
				win.connect("delete-event", self.destroy)
				win.show_all()
				go = False
				break

			if alert_code == 3:
				global bulbs, SN
				fName = "./ProgramFiles/" + SN + ".txt"

				for i in range(bulbs):
					self.add_tag(i, './temp.txt')

				self.overwrite_record()
				self.delete_file('./temp.txt')
				go = False

			if alert_code == 5:
				win = MainMenu()
				win.connect("delete-event", self.destroy)
				win.show_all()
				go = False


		Gtk.Window.destroy(self)



	def get_ID(self, tag):
		id = int(tag[0])
		return id

	def get_data(self, tag):
		data = str(tag[1])
		data = data.rstrip()
		return data

	def get_hours(self, tag):
		data = self.get_data(tag)
		split = data.rsplit(':', 1)
		hours = float(split[1])
		return hours

	def select_device_read(self, CS):
		reader = SimpleMFRC522(CS)
		time.sleep(.25)
		tid, data = reader.read()
		tag = [tid, data]
		return tag

	def delete_file(self, fName):
		toDelete = open(fName, 'w+')
		toDelete.close()

	def overwrite_record(self):
		global SN
		fName = "./ProgramFiles/" + SN + ".txt"
		fRead = open('./ProgramFiles/temp.txt', 'r')
		fWrite = open(fName, 'w+')
		while True:
			line = fRead.readline()
			if line == '':
				break
			else:
				fWrite.write(line)
		fRead.close()
		fWrite.close()


	def add_tag(self, CS, fName):
		global SN, alert_code
		tag = self.select_device_read(CS)
		tid = self.get_ID(tag)
		print("READ ID: ", tid)
		data = self.get_data(tag)
		convert = ' ' + data + '\n'
		search = self.search_tag(tid)
		if search == False:
			try:
				f = open(fName, "a+")
				f.write(str(tid))
				f.write(convert)
			finally:
				f.close()

		if search == True:
			alert_code = 4
			win = AlertWindow()
			win.connect("delete-event", self.destroy)
			win.show_all()



	def search_tag(self, tag_id):
		global SN
		fName = "./ProgramFiles/" + SN + ".txt"
		try:
			f = open(fName, "r")
			for line in f:
				temp_tag = [line.split()]
				temp_id = int(temp_tag[0][0])
				if temp_id == tag_id:
					return True		# tag exists in records
		finally:
			f.close()
		return False		# tag not found










class YesNoBox(Gtk.Window):

	def __init__(self):

		global yes_no_condition
		global min_chosen, sec_chosen
		global SN

		self.directionLabel = Gtk.Label()
		self.infoLabel = Gtk.Label()
		info = " "
		# confirming treatment time
		if yes_no_condition == 1:
			windowTitle = "Confirm Treatment Time:"

			if min_chosen == 0 and sec_chosen > 1:
				info = str(sec_chosen) + " Seconds"

			if min_chosen == 1 and (sec_chosen > 1 or sec_chosen == 0):
				info = str(min_chosen) + " Minute and " + str(sec_chosen) + " Seconds"

			if min_chosen == 1 and sec_chosen == 1:
				info = str(min_chosen) + " Minute and " + str(sec_chosen) + " Second"

			if min_chosen > 1 and sec_chosen > 1:
				info = str(min_chosen) + " Minutes and " + str(sec_chosen) + " Seconds"

			if min_chosen > 1 and sec_chosen == 1:
				info = str(min_chosen) + " Minutes and " + str(sec_chosen) + " Second"

			if min_chosen > 1 and sec_chosen == 0:
				info = str(min_chosen) + " Minutes"

			if min_chosen == 0 and sec_chosen == 1:
				info = str(sec_chosen) + " Second"

			if min_chosen == 0 and sec_chosen > 1:
				info = str(sec_chosen) + " Seconds"

		# confirming serial number for maintenance mode
		if yes_no_condition == 2:
			windowTitle = "Confirm Serial Number:"
			info = "Serial Number: " + str(SN)

        # proceed with unknown bulbs?
		if yes_no_condition == 3:
			windowTitle = "Unrecognized UVB bulb(s). Continue and risk DEATH AND DISMEMBERMENT?"
			info = " "

		self.directionLabel.set_text(windowTitle)
		self.infoLabel.set_text(info)

		Gtk.Window.__init__(self, title=windowTitle)
		self.set_border_width(20)
        #self.fullscreen()

		no_button = Gtk.Button.new_with_label("  NO  ")
		no_button.connect("clicked", self.no_button_clicked)

		yes_button = Gtk.Button.new_with_label("  YES  ")
		yes_button.connect("clicked", self.yes_button_clicked)

		grid = Gtk.Grid()
		grid.attach(self.directionLabel, 0, 0, 3, 1)
		grid.attach(self.infoLabel, 0, 2, 3, 2)
		grid.attach(no_button, 0, 4, 1, 1)
		grid.attach(yes_button,2, 4, 1, 1)
		self.add(grid)

	def no_button_clicked(self, widget):
		global SN, yes_no_condition
		SN = "P3D#"
		Gtk.Window.destroy(self)

		if yes_no_condition == 1:
			win = SetTreatmentTimeWindow()
			win.connect("delete-event", self.destroy)
			win.show_all()
		if yes_no_condition == 2:
			win = EnterSerialNumberWindow()
			win.connect("delete-event", self.destroy)
			win.show_all()
		if yes_no_condition == 3:
			sys.exit(0)
			# should shut down unit when moved outside of testing environment
			# os.system("sudo shutdown now")


	def yes_button_clicked(self, widget):
		global SN, yes_no_condition, valid_SN, error_code
		if yes_no_condition == 1:
			Gtk.Window.destroy(self)
			win = TreatmentWindow()
			win.connect("delete-event", self.destroy)
			win.show_all()


		if yes_no_condition == 2:
			# look in active directory for file named SN.txt (e.g. P3D#1234.txt)
			file_to_check = "./ProgramFiles/" + SN + ".txt"
			if path.exists(file_to_check) == True:
				valid_SN = True
			else:
				valid_SN = False

			if valid_SN == True:
				Gtk.Window.destroy(self)
				win = MaintenanceWindow()
				win.connect("delete-event", self.destroy)
				win.show_all()
			elif valid_SN == False:
				error_code = 2
				Gtk.Window.destroy(self)
				win = ErrorWindow()
				win.connect("delete-event", self.destroy)
				win.show_all()


		if yes_no_condition == 3:
			Gtk.Window.destroy(self)
			win = MainMenu()
			win.connect("delete-event", self.destroy)
			win.show_all()
		Gtk.Window.destroy(self)














class ErrorWindow(Gtk.Window):

	def __init__(self):
		global error_code
		Gtk.Window.__init__(self, title="Error")
		self.set_border_width(20)
        # self.fullscreen()

		self.warning = Gtk.Label()

		# treatment time entered is 0:00  -> re-enter treatment time
		if error_code == 1:
			self.warning.set_text("Treatment Cannot Be 0:00")
        # serial number not found  -> re-enter serial number
		if error_code == 2:
			self.warning.set_text("Invalid Serial Number")

		hbox = Gtk.Box(spacing=6)
		self.add(hbox)
		hbox.pack_start(self.warning, False, False, 0)

		ok_button = Gtk.Button.new_with_label("OK")
		ok_button.connect("clicked", self.ok_button_clicked)
		hbox.pack_start(ok_button, False, False, 0)


	def ok_button_clicked(self, widget):
		global SN, error_code
		if error_code == 1:
			win = SetTreatmentTimeWindow()
			win.connect("delete-event", self.destroy)
			win.show_all()
		if error_code == 2:
			SN = "P3D#"
			win = EnterSerialNumberWindow()
			win.connect("delete-event", self.destroy)
			win.show_all()
		Gtk.Window.destroy(self)











#######################################################################
# MAIN -- JUST USED FOR LAUNCHING GTK.MainWindow
#######################################################################
win = InitialWindow()
win.show_all()
Gtk.main()
#######################################################################
