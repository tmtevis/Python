#  Program navigates to Algorand Faucet website, submits request and solves capcha
#  Added to scheduled tasks to repeat every 3 hours and 10 minutes indefinitely
import time
import webbrowser
import pynput
from pynput import mouse, keyboard
from pynput.mouse import Button, Controller
from pynput.keyboard import Key, Controller

# instantiate mouse and keyboard as Controller
user_mouse = mouse.Controller()
user_keyboard = keyboard.Controller()
user_keyboard = keyboard.Controller()

# go to Yieldly prize game page to collect Yieldly rewards for ALGO stake
webbrowser.open_new_tab("https://www.algorandfaucet.com/")

# find position of mouse ---> 
print('The current pointer position is {0}'.format(user_mouse.position))
user_mouse.position = (159, 268)
time.sleep(10)
user_mouse.click(Button.left, 1)
time.sleep(2)

user_mouse.position = (233, 317)
time.sleep(3)
user_mouse.click(Button.left, 1)
time.sleep(2)

user_mouse.position = (101, 331)
time.sleep(3)
user_mouse.click(Button.left, 1)
time.sleep(2)

user_mouse.position = (426, 326)
time.sleep(3)
user_mouse.click(Button.left, 1)
time.sleep(10)

# # close tab
user_keyboard.press(Key.ctrl)
user_keyboard.tap('w')
user_keyboard.release(Key.ctrl)
