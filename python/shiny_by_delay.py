import os
from PIL import ImageGrab, Image
import pyautogui
import imagehash
import time
from datetime import datetime
from pytz import timezone
import json
from discord_webhook import DiscordWebhook, DiscordEmbed
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

resets = read_json("./resets.json")
settings = read_json("./settings.json")

json_time = resets["total_seconds"]
json_time2 = resets["total_seconds_since_last_shiny"]
possible_encounters = settings["possible_encounters"]
buttons = settings["buttons"]
colors = settings["colors"]
bounding_boxes = settings["bounding_boxes"]

isShiny = False

hour = datetime.now(timezone('US/Central')).hour
minute = datetime.now(timezone('US/Central')).minute
second = datetime.now(timezone('US/Central')).second
start_time = (hour*60**2) + (minute*60) + second

try:
    encounter1_image = 'img/encounter1.png'
    img = Image.open(encounter1_image)
    encounter1_hash = imagehash.whash(img)
    img.close()
except:
    encounter1_hash = 100

try:
    encounter2_image = 'img/encounter2.png'
    img = Image.open(encounter2_image)
    encounter2_hash = imagehash.whash(img)
    img.close()
except:
    encounter2_hash = 100

try:
    encounter3_image = 'img/encounter3.png'
    img = Image.open(encounter3_image)
    encounter3_hash = imagehash.whash(img)
    img.close()
except:
    encounter3_hash = 100

encounter_hashes = [encounter1_hash, encounter2_hash, encounter3_hash]
encounter_names = settings["encounter_names"]

for i in range(3,0,-1):
    clear_screen()
    print(f"Starting in: {i}")
    time.sleep(1)

try:
    os.path.abspath('./img/screenshot.png')
except:
    pass

while isShiny == False:
    delay = 0
    press_and_release("Y")
    #finding the !! bubble
    #the loop ends when the !! bubble appears on screen
    while True:
        time.sleep(0.01)
        screenshot = ImageGrab.grab(bbox=settings["screen_size"])
        pixels = screenshot.load()
        screenshot.close()

        r, g, b = pixels[bounding_boxes["bubble"][0], bounding_boxes["bubble"][1]]
        if r == colors["bubble"][0] and g == colors["bubble"][1] and b == colors["bubble"][2]:
            break
    press_and_release("A")
    time.sleep(3)

    #seeing if you missed the reel in
    #checks to see if the "No! You reeled it in too slow!"
    screenshot = ImageGrab.grab(bbox=settings["screen_size"])
    pixels = screenshot.load()
    screenshot.close()
    r, g, b = pixels[bounding_boxes["too_slow"][0], bounding_boxes["too_slow"][1]]
    # if rgb isnt equal to those values then you didnt miss the reel in
    if r != colors["too_slow"][0] and g != colors["too_slow"][1] and b != colors["too_slow"][2]:
        #finding the encounter
        #the loop ends once the pokemons name appears on screen
        try:
            encounter.close()
        except:
            pass
        
        encountered = 100
        while encountered == 100:
            time.sleep(0.01)
            delay = delay + 1
            encounter = ImageGrab.grab(bbox=bounding_boxes["encounter"])
            encounter_hash = imagehash.whash(encounter)
            for i in range(possible_encounters):
                encounter_similarity = encounter_hashes[i] - encounter_hash
                #print(f"{encounter_names[i]}: {encounter_similarity}")
                if encounter_similarity < 10:
                    print(f"{encounter_names[i]} encountered")
                    encountered = i
                    break

        hour = datetime.now(timezone('US/Central')).hour
        minute = datetime.now(timezone('US/Central')).minute
        second = datetime.now(timezone('US/Central')).second
        current_time = (hour*60**2) + (minute*60) + second
        elapsed_time = current_time - start_time
        resets = read_json("resets.json")
        resets["resets"] = resets["resets"] + 1
        resets["resets_since_last_shiny"] = resets["resets_since_last_shiny"] + 1
        resets["chain"] = resets["chain"] + 1
        resets["total_seconds"] = json_time + elapsed_time
        resets["total_seconds_since_last_shiny"] = json_time2 + elapsed_time
        write_json("resets.json", resets)
        
        #print(delay)
        encounter.close()
        

        if delay > 110:
            encounter = ImageGrab.grab(bbox=(1025,53,1855,551))
            encounter.save("img/screenshot.png")
            encounter.close()

            isShiny = True
            print("Longer delay in encounter")
            pyautogui.hotkey('ctrl', 'c')
            print("Save state created")

            resets = read_json("resets.json")

            seconds = resets["total_seconds_since_last_shiny"]
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            seconds = seconds % 60
            since_last_shiny_time_formatted = f"{hours} hours, {minutes} minutes, and {seconds} seconds"

            seconds = resets["total_seconds"]
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            seconds = seconds % 60
            time_formatted = f"{hours} hours, {minutes} minutes, and {seconds} seconds"

            webhook = DiscordWebhook(url="", username="Sparkles")
            with open("img/screenshot.png", "rb") as f:
                webhook.add_file(file=f.read(), filename="screenshot.png")
            embed = DiscordEmbed(title=f"Shiny {encounter_names[encountered]} Found", description=f"{resets['resets_since_last_shiny']} encounters since last shiny over the span of {since_last_shiny_time_formatted}, with a chain of {resets['chain']}", color="FCDE3A")
            embed.set_author(name="Shiny Found", icon_url="https://em-content.zobj.net/source/apple/391/sparkles_2728.png",)
            embed.set_image(url="attachment://screenshot.png")
            embed.add_embed_field(name="Total Encounters", value=resets['resets'])
            embed.add_embed_field(name="Total Time", value=time_formatted)
            embed.set_footer(text="Alpha Sapphire")
            embed.set_timestamp()
            webhook.add_embed(embed)
            response = webhook.execute()

            resets["total_seconds_since_last_shiny"] = 0
            resets['resets_since_last_shiny'] = 0
            resets['chain'] = 0
            write_json("resets.json", resets)
        else:
            similarity = 100
            print("Normal encounter delay")
            #waiting for the bottom screen
            #the loop ends when the bottom screen loads
            while similarity > 10:
                time.sleep(0.005)
                screenshot = ImageGrab.grab(bbox=(1108,551,1772,1050))
                screenshot_hash = imagehash.whash(screenshot)
                similarity = bottomScreen_hash - screenshot_hash
                screenshot.close()
            time.sleep(1)
            pydirectinput.press('left')
            #time.sleep(0.2)
            pydirectinput.press('right')
            #time.sleep(0.2)
            pydirectinput.press('a')
            time.sleep(6)
    else:
        print("Chain Broken")
        resets = read_json("resets.json")
        resets["chain"] = 0
        write_json("resets.json", resets)
        pydirectinput.press('a')
        time.sleep(1)