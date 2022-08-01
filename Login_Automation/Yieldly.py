## Yieldly.py is a tool for ensuring instant compounding of daily rewards
#  Program navigates to staking page, collects available reward and re-stakes
#  Added to scheduled tasks for every day at 1AM - CURRENTLY DISABLED UNTIL RESTAKING IS SOLVED
import time
import webbrowser
import pynput
from pynput import mouse, keyboard
from pynput.mouse import Button, Controller
from pynput.keyboard import Key, Controller

# instantiate mouse and keyboard as Controller
user_mouse = mouse.Controller()
user_keyboard = keyboard.Controller()

# go to Yieldly prize game page to collect Yieldly rewards for ALGO stake
webbrowser.open_new_tab("https://app.yieldly.finance/prize-games")

# # # find position of mouse ---> 
# print('The current pointer position is {0}'.format(user_mouse.position))
# set cursor to 'Connect Wallet' button
user_mouse.position = (1744, 135)
time.sleep(5)
user_mouse.click(Button.left, 1)
time.sleep(2)


#### LOGIN ###
# login process - tab tab tab enter
for i in range(3):
    user_keyboard.tap(Key.tab)
user_keyboard.tap(Key.enter)
time.sleep(2)
##################################


### CLAIM REWARD ###
# scroll down to show 'Claim' button
for i in range(6):
    user_keyboard.tap(Key.down)
# move to 'Claim' button and click
user_mouse.position = (1658, 901)
time.sleep(2)
user_mouse.click(Button.left, 1)
# click 'Next'
user_mouse.position = (886, 760)
time.sleep(2)
user_mouse.click(Button.left, 1)
# move to 'Confirm' button
user_mouse.position = (1044, 827)
time.sleep(2)
user_mouse.click(Button.left, 1)
# move to Password button (autofill)
user_mouse.position = (1053, 718)
time.sleep(2)
user_mouse.click(Button.left, 1)
# wait 20 seconds for transaction to clear
time.sleep(20)
# press Return to close 'Weekly Prize Game' dialog
user_mouse.position = (846, 734)
time.sleep(2)
user_mouse.click(Button.left, 1)



### RE-STAKE ###
# navigate to Yieldly staking page to stake claimed reward
user_mouse.position = (94, 257)
time.sleep(2)
user_mouse.click(Button.left, 1)
time.sleep(3)
user_mouse.click(Button.left, 1)
time.sleep(2)
# navigate to 'Stake' button
user_mouse.position = (1672, 377)
time.sleep(2)
user_mouse.click(Button.left, 1)
# navigate to '100%' button
user_mouse.position = (968, 680)
time.sleep(2)
user_mouse.click(Button.left, 1)
# navigate to 'Next' button
user_mouse.position = (888, 776)
time.sleep(2)
user_mouse.click(Button.left, 1)
# navigate to 'Continue' button
user_mouse.position = (1054, 830)
time.sleep(2)
user_mouse.click(Button.left, 1)
# navigate to 'Sign' button
user_mouse.position = (1056, 720)
time.sleep(2)
user_mouse.click(Button.left, 1)


# wait 20 seconds for transaction to clear
time.sleep(20)

# close tab
user_keyboard.press(Key.ctrl)
time.sleep(1)
user_keyboard.tap('w')
user_keyboard.release(Key.ctrl)
