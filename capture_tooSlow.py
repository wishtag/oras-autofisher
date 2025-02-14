import os
from PIL import ImageGrab, Image
import pyautogui
import time
import pydirectinput

#print("Make sure the window is focused on")
#time.sleep(3)

try:
    os.remove("img/tooSlow.png")
except:
    pass
#pydirectinput.press('x')
#time.sleep(12)
screenshot = ImageGrab.grab(bbox=(1029,416,1851,528))
screenshot.save("img/tooSlow.png")
screenshot.close()