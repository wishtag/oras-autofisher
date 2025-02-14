import os
from PIL import ImageGrab, Image
import pyautogui
import imagehash
import time
import pydirectinput
from datetime import datetime, date
from pytz import timezone
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

json_time = read_json("resets.json")["total_seconds"]
json_time2 = read_json("resets.json")["total_seconds_since_last_shiny"]
similarity = 100
encountered = 100
possible_encounters = 2
isShiny = False

hour = datetime.now(timezone('US/Central')).hour
minute = datetime.now(timezone('US/Central')).minute
second = datetime.now(timezone('US/Central')).second
start_time = (hour*60**2) + (minute*60) + second

print("Make sure the window is focused on")
time.sleep(3)


bubble_image = 'img/bubble.png'
img = Image.open(bubble_image)
bubble_hash = imagehash.whash(img)
img.close()

tooSlow_image = 'img/tooSlow.png'
img = Image.open(tooSlow_image)
tooSlow_hash = imagehash.whash(img)
img.close()

bottomScreen_image = 'img/bottomScreen.png'
img = Image.open(bottomScreen_image)
bottomScreen_hash = imagehash.whash(img)
img.close()

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
encounter_names = ["Wailmer", "Staryu", "Corsola"]


try:
    os.remove("img/screenshot.png")
except:
    pass

while isShiny == False:
    encountered = 100
    similarity = 100
    delay = 0
    pydirectinput.press('x')
    #finding the !! bubble
    #the loop ends when the !! bubble appears on screen
    while similarity > 10:
        time.sleep(0.005)
        screenshot = ImageGrab.grab(bbox=(1406, 247, 1468, 308))
        screenshot_hash = imagehash.whash(screenshot)
        similarity = bubble_hash - screenshot_hash
        screenshot.close()
    pydirectinput.press('a')
    time.sleep(3)

    #seeing if you missed the reel in
    #checks to see if the "No! You reeled it in too slow!"
    screenshot = ImageGrab.grab(bbox=(1029,416,1851,528))
    screenshot_hash = imagehash.whash(screenshot)
    similarity = tooSlow_hash - screenshot_hash
    #print(similarity)

    screenshot.close()

    # if similarity > 15 then you didnt miss the reel in
    if similarity > 15:
        #finding the encounter
        #the loop ends once the pokemons name appears on screen
        try:
            encounter.close()
        except:
            pass
        while encountered == 100:
            time.sleep(0.01)
            delay = delay + 1
            encounter = ImageGrab.grab(bbox=(1139,467,1231,501))
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

            #resets["total_seconds_since_last_shiny"] = 0
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