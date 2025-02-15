import os
from PIL import ImageGrab, Image
from datetime import datetime
from pytz import timezone
import imagehash
import time
import pydirectinput
import json
from discord_webhook import DiscordWebhook, DiscordEmbed

def read_json(file):
    f = open (file, "r")
    data = json.loads(f.read())
    f.close()
    return data

def write_json(file, object):
    f = open (file, "w")
    json.dump(object, f)
    f.close()

should_run = True
count_towards_resets = True
possible_encounters = 2

json_time = read_json("resets.json")["total_seconds"]
json_time2 = read_json("resets.json")["total_seconds_since_last_shiny"]

hour = datetime.now(timezone('US/Central')).hour
minute = datetime.now(timezone('US/Central')).minute
second = datetime.now(timezone('US/Central')).second
start_time = (hour*60**2) + (minute*60) + second

bubble_image = 'img/bubble.png'
img = Image.open(bubble_image)
bubble_hash = imagehash.whash(img)
img.close()

tooSlow_image = 'img/tooSlow.png'
img = Image.open(tooSlow_image)
tooSlow_hash = imagehash.whash(img)
img.close()

print("Make sure the window is focused on")
time.sleep(3)

while should_run:
    try:
        os.remove("img/screenshot.png")
    except:
        pass
    similarity = 100
    pydirectinput.press('x')
    while similarity > 10:
        time.sleep(0.005)
        # !! bubble
        screenshot = ImageGrab.grab(bbox=(1406, 247, 1468, 308))
        screenshot_hash = imagehash.whash(screenshot)
        similarity = bubble_hash - screenshot_hash
        screenshot.close()
    pydirectinput.press('a')
    time.sleep(3)
    screenshot = ImageGrab.grab(bbox=(1092,416,1851,528))
    screenshot_hash = imagehash.whash(screenshot)
    similarity = tooSlow_hash - screenshot_hash
    print(similarity)
    screenshot.close()

    if similarity > 15:
        if count_towards_resets:
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

        time.sleep(3.2)
        encounter = ImageGrab.grab(bbox=(1139,467,1231,501)) #Nameplate
        #encounter = ImageGrab.grab(bbox=(0,0,1920,1080)) #Full Screen
        #encounter = ImageGrab.grab(bbox=(1025,53,1855,551)) #Full encounter
        #encounter = ImageGrab.grab(bbox=(1348,146,1618,416)) #Box
        screenshot_hash = imagehash.whash(encounter)

        matched_encounter = False
        index = 99
        for i in range(possible_encounters):
            try:
                encounter_image = f'img/encounter{i+1}.png'
                img = Image.open(encounter_image)
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
                encounter.save(f'img/encounter{index+1}.png')
        
        index = 99
        for i in range(possible_encounters):
            try:
                encounter_image = f'img/encounter{i+1}.png'
                img = Image.open(encounter_image)
                encounter_hash = imagehash.whash(img)
                img.close()
            except:
                index = i
                break

        if index == 99:
            should_run = False
            print("Done!")
            webhook = DiscordWebhook(url="", username="Sparkles")
            embed = DiscordEmbed(title=f"Done Capturing Encounters", description=f"I finished lol", color="FCDE3A")
            webhook.add_embed(embed)
            response = webhook.execute()

        else:
            #encounter.save("img/screenshot.png")
            encounter.close()
            time.sleep(6)
            pydirectinput.press('down')
            #time.sleep(0.2)
            pydirectinput.press('right')
            #time.sleep(0.2)
            pydirectinput.press('a')
            time.sleep(6)
    else:
        if count_towards_resets:
            resets = read_json("resets.json")
            resets["chain"] = 0
            write_json("resets.json", resets)
        pydirectinput.press('a')
        time.sleep(1)