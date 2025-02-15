import os
from PIL import ImageGrab, Image
import imagehash
import time
import json
import vgamepad as vg

gamepad = vg.VX360Gamepad()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def read_json(file):
    with open(os.path.abspath(file), 'r') as f:
        data = json.loads(f.read())
    return data

def write_json(file, object):
    with open(os.path.abspath(file), 'w') as f:
        json.dump(object, f)

def press_and_release(button):
    gamepad.press_button(button=eval(buttons[button]))
    gamepad.update()
    time.sleep(0.1)
    gamepad.release_button(button=eval(buttons[button]))
    gamepad.update()

settings = read_json("./settings.json")
possible_encounters = settings["possible_encounters"]
buttons = settings["buttons"]
colors = settings["colors"]
bounding_boxes = settings["bounding_boxes"]

for i in range(3,0,-1):
    clear_screen()
    print(f"Starting in: {i}")
    time.sleep(1)

should_run = True
while should_run:
    try:
        os.remove(os.path.abspath("./screenshot.png"))
    except:
        pass
    press_and_release("Y")
    #finding the !! bubble
    #the loop ends when the !! bubble appears on screen
    while True:
        time.sleep(0.005)
        screenshot = ImageGrab.grab(bbox=settings["screen_size"])
        pixels = screenshot.load()
        screenshot.close()

        r, g, b = pixels[bounding_boxes["bubble"][0], bounding_boxes["bubble"][1]]
        if r == colors["bubble"][0] and g == colors["bubble"][1] and b == colors["bubble"][2]:
            break
    press_and_release("A")
    time.sleep(3)

    screenshot = ImageGrab.grab(bbox=settings["screen_size"])
    pixels = screenshot.load()
    screenshot.close()
    r, g, b = pixels[bounding_boxes["too_slow"][0], bounding_boxes["too_slow"][1]]
    # if rgb isnt equal to those values then you didnt miss the reel in
    if r != colors["too_slow"][0] and g != colors["too_slow"][1] and b != colors["too_slow"][2]:
        time.sleep(3.2)
        encounter = ImageGrab.grab(bbox=bounding_boxes["encounter"])
        screenshot_hash = imagehash.whash(encounter)

        matched_encounter = False
        index = 99
        for i in range(possible_encounters):
            try:
                img = Image.open(os.path.abspath(f"./encounters/encounter{i+1}.png"))
                encounter_hash = imagehash.whash(img)
                img.close()

                encounter_similarity = encounter_hash - screenshot_hash
                print(encounter_similarity)
                if encounter_similarity < 10: #if this is true, then they are the same image
                    matched_encounter = True
            except:
                index = i
                break

        if matched_encounter == False:
            if index != 99:
                encounter.save(os.path.abspath(f"./encounters/encounter{index+1}.png"))

        if index == 99:
            should_run = False
            print("Done!")
        else:
            encounter.close()
            time.sleep(6)
            press_and_release("LEFT")
            #time.sleep(0.2)
            press_and_release("RIGHT")
            #time.sleep(0.2)
            press_and_release("A")
            time.sleep(6)