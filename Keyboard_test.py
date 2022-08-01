# This program will copy/paste the source code of a webpage when used with webbrowser library - see Browser_test

import pynput
import time
from pynput.keyboard import Key, Controller

keyboard = Controller()

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
keyboard.release(Key.ctrl)