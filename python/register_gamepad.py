import time
import vgamepad as vg
import os
import json

gamepad = vg.VX360Gamepad()

def read_json(file):
    with open(os.path.abspath(file), 'r') as f:
        data = json.loads(f.read())
    return data

def press_and_release(button):
    gamepad.press_button(button=eval(buttons[button]))
    gamepad.update()
    time.sleep(0.1)
    gamepad.release_button(button=eval(buttons[button]))
    gamepad.update()

buttons = read_json("./settings.json")["buttons"]

for i in range(3,0,-1):
    print(i)
    time.sleep(1)

press_and_release("A")
time.sleep(1)