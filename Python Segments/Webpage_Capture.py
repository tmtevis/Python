# this script is meant to navigate to a webpage and capture its source code into a time-date stamped text file
import time
import webbrowser
import pynput
from pynput.keyboard import Key, Controller
from datetime import datetime

# get time
now = datetime.now()
test_page_soure = now.strftime("%m_%d_%Y_%H_%M")
print(test_page_soure)

# instantiate keyboard as Controller class
keyboard = Controller()

# go to allagent website
webbrowser.open_new_tab("https://sample.com")

# arrive at website (login status unknown)
time.sleep(1)
keyboard.press(Key.ctrl)
keyboard.tap('u')           # CTRL + U for source code
time.sleep(0.5)
keyboard.tap('a')           # CTRL + A select all
keyboard.tap('c')           # CTRL + C copy to clipboard

keyboard.tap(Key.esc)       # CTRL + ESC open Start menu
time.sleep(0.5)
keyboard.release(Key.ctrl)
keyboard.type('notepad')
time.sleep(0.5)
keyboard.tap(Key.enter)     # type 'notepad' and open program


time.sleep(0.5)
keyboard.press(Key.ctrl)
keyboard.tap('v')           # CTRL + V to paste source code
time.sleep(0.5)
keyboard.tap('s')           # CTRL + S to save doc
time.sleep(0.5)

# SAVE AS MM_DD_YYYY_HH_MM.txt
keyboard.release(Key.ctrl)
keyboard.type(test_page_soure)
time.sleep(0.5)
keyboard.tap(Key.enter)
time.sleep(0.5)

