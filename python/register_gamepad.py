import time
import vgamepad as vg

gamepad = vg.VX360Gamepad()

def press_and_release(button):
    gamepad.press_button(button=button)
    gamepad.update()
    time.sleep(0.1)
    gamepad.release_button(button=button)
    gamepad.update()

for i in range(3,0,-1):
    print(i)
    time.sleep(1)

press_and_release(vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
time.sleep(1)