import os
from PIL import ImageGrab, Image
import pyautogui
import imagehash
import time
import pydirectinput
import cv2
import numpy as np
from util import get_limits
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
similarity = 100
encountered = 100
possible_encounters = 3
isShiny = False

lower_color, upper_color = get_limits([124,208,228]) #Barboach
lower_color2, upper_color2 = get_limits([82,117,239]) #Magikarp
lower_color3, upper_color3 = get_limits([87,130,241]) #Goldeen

hour = datetime.now(timezone('US/Central')).hour
minute = datetime.now(timezone('US/Central')).minute
second = datetime.now(timezone('US/Central')).second
start_time = (hour*60**2) + (minute*60) + second

print("Make sure the window is focused on")
time.sleep(3)


bubble_image = 'bubble.png'
img = Image.open(bubble_image)
bubble_hash = imagehash.whash(img)
img.close()

tooSlow_image = 'tooSlow.png'
img = Image.open(tooSlow_image)
tooSlow_hash = imagehash.whash(img)
img.close()

try:
    encounter1_image = 'encounter1.png'
    img = Image.open(encounter1_image)
    encounter1_hash = imagehash.whash(img)
    img.close()
except:
    encounter1_hash = 100

try:
    encounter2_image = 'encounter2.png'
    img = Image.open(encounter2_image)
    encounter2_hash = imagehash.whash(img)
    img.close()
except:
    encounter2_hash = 100

try:
    encounter3_image = 'encounter3.png'
    img = Image.open(encounter3_image)
    encounter3_hash = imagehash.whash(img)
    img.close()
except:
    encounter3_hash = 100

encounter_hashes = [encounter1_hash, encounter2_hash, encounter3_hash]
encounter_names = ["Barboach", "Magikarp", "Goldeen"]
avoid_color = [False, True, True]
custom_bbox = [True, False, False]
custom_bbox_values = [[1386,314,1568,352], [], []]

while isShiny == False:
    try:
        os.remove("screenshot.png")
    except:
        pass
    try:
        os.remove("screenshot2.png")
    except:
        pass
    try:
        os.remove("screenshot3.png")
    except:
        pass
    encountered = 100
    similarity = 100
    pydirectinput.press('x')
    #finding the !! bubble
    #the loop ends when the !! bubble appears on screen
    while similarity > 10:
        time.sleep(0.005)
        screenshot = ImageGrab.grab(bbox=(1409,231,1472,294))
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

    screenshot.close()

    # if similarity > 10 then you didnt miss the reel in
    if similarity > 10:
        #finding the encounter
        #the loop ends once the pokemon appears on screen
        try:
            encounter.close()
        except:
            pass
        while encountered == 100:
            time.sleep(0.01)
            encounter = ImageGrab.grab(bbox=(1139,467,1231,501))
            #encounter = ImageGrab.grab(bbox=(1025,53,1855,551))
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
        resets["chain"] = resets["chain"] + 1
        resets["total_seconds"] = json_time + elapsed_time
        write_json("resets.json", resets)

        encounter.save("screenshot2.png")
        encounter.close()
        encounter = ImageGrab.grab(bbox=(1025,53,1855,551))
        encounter.save("screenshot.png")
        encounter.close()

        if custom_bbox[encountered] == True:
            encounter = ImageGrab.grab(bbox=custom_bbox_values[encountered])
            encounter.save("screenshot3.png")
            encounter.close()
            image = cv2.imread('screenshot3.png')
        else:
            image = cv2.imread('screenshot.png')

        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        masks = [cv2.inRange(hsv_image, lower_color, upper_color), cv2.inRange(hsv_image, lower_color2, upper_color2), cv2.inRange(hsv_image, lower_color3, upper_color3)]

        if (avoid_color[encountered] == True and cv2.countNonZero(masks[encountered]) < 200) or (avoid_color[encountered] == False and cv2.countNonZero(masks[encountered]) > 75):
            isShiny = True
            print("Color detected in the image")
            pyautogui.hotkey('ctrl', 'c')
            print("Save state created")
            resets = read_json("resets.json")
            webhook = DiscordWebhook(url="", username="Sparkles")
            with open("screenshot.png", "rb") as f:
                webhook.add_file(file=f.read(), filename="screenshot.png")
            embed = DiscordEmbed(title=f"Shiny {encounter_names[encountered]} Found", description=f"{resets['resets']} Resets over {resets['total_seconds']} Seconds, with a chain of {resets['chain']}\nGame: Alpha Sapphire", color="FCDE3A")
            embed.set_author(name="Shiny Found", icon_url="https://em-content.zobj.net/source/apple/391/sparkles_2728.png",)
            embed.set_image(url="attachment://screenshot.png")
            embed.set_timestamp()
            webhook.add_embed(embed)
            response = webhook.execute()
            cv2.imshow('Original Image', image)
            highlighted_image = cv2.bitwise_and(image, image, mask=masks[encountered])
            cv2.imshow(f'Highlighted Image (Color{encountered} Detected)', highlighted_image)

            cv2.waitKey(0)
            cv2.destroyAllWindows()

        #for i in range(possible_encounters):
        #    if cv2.countNonZero(masks[i]) > 20:
        #        isShiny = True
        #        print("Color detected in the image.")
        #        cv2.imshow('Original Image', image)
        #        for j in range(possible_encounters):
        #            highlighted_image = cv2.bitwise_and(image, image, mask=masks[j])
        #            cv2.imshow(f'Highlighted Image (Color{j} Detected)', highlighted_image)

        #        cv2.waitKey(0)
        #        cv2.destroyAllWindows()

        if isShiny == False:
            print("Color not detected in the image")
            time.sleep(7)
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

"""
while isShiny == False:
    try:
        os.remove("screenshot.png")
    except:
        pass
    similarity = 100
    pydirectinput.press('x')
    while similarity > 10:
        time.sleep(0.005)
        # !! bubble
        screenshot = ImageGrab.grab(bbox=(1412,234,1475,296))
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

    if similarity > 20:
        time.sleep(3)
        encounter = ImageGrab.grab(bbox=(1025,53,1855,551))
        screenshot_hash = imagehash.whash(encounter)
        encounter.save("screenshot.png")
        encounter.close()

        image = cv2.imread('screenshot.png')

        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        lower_color, upper_color = get_limits([164,132,240])
        lower_color2, upper_color2 = get_limits([180,128,161])

        mask = cv2.inRange(hsv_image, lower_color, upper_color)
        mask2 = cv2.inRange(hsv_image, lower_color2, upper_color2)

        if cv2.countNonZero(mask) > 20 or cv2.countNonZero(mask2) > 20:
            isShiny = True
            print("Color detected in the image.")
            highlighted_image = cv2.bitwise_and(image, image, mask=mask)
            highlighted_image2 = cv2.bitwise_and(image, image, mask=mask2)

            cv2.imshow('Original Image', image)
            cv2.imshow('Highlighted Image (Color Detected)', highlighted_image)
            cv2.imshow('Highlighted Image (Color2 Detected)', highlighted_image2)

            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else:
            isShiny = False
            print("Color not detected in the image.")
            if possibleShiny_hash - screenshot_hash < 15:
                isShiny = True
                print("Images are similar, possible shiny")
                os.remove("screenshot.png")
                time.sleep(3)
                encounter = ImageGrab.grab(bbox=(1025,53,1855,551))
                encounter.save("screenshot.png")
                encounter.close()

                image = cv2.imread('screenshot.png')

                hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
                mask = cv2.inRange(hsv_image, lower_color, upper_color)
                mask2 = cv2.inRange(hsv_image, lower_color2, upper_color2)

                if cv2.countNonZero(mask) > 20 or cv2.countNonZero(mask2) > 20:
                    isShiny = True
                    print("Color detected in the image.")
                    highlighted_image = cv2.bitwise_and(image, image, mask=mask)
                    highlighted_image2 = cv2.bitwise_and(image, image, mask=mask2)

                    cv2.imshow('Original Image', image)
                    cv2.imshow('Highlighted Image (Color Detected)', highlighted_image)
                    cv2.imshow('Highlighted Image (Color2 Detected)', highlighted_image2)

                    cv2.waitKey(0)
                    cv2.destroyAllWindows()

            else:
                time.sleep(6)
                pydirectinput.press('down')
                #time.sleep(0.2)
                pydirectinput.press('right')
                #time.sleep(0.2)
                pydirectinput.press('a')
                time.sleep(6)

        hour = datetime.now(timezone('US/Central')).hour
        minute = datetime.now(timezone('US/Central')).minute
        second = datetime.now(timezone('US/Central')).second
        current_time = (hour*60**2) + (minute*60) + second
        elapsed_time = current_time - start_time
        resets = read_json("resets.json")
        resets["resets"] = resets["resets"] + 1
        resets["total_seconds"] = json_time + elapsed_time
        write_json("resets.json", resets)
    else:
        pydirectinput.press('a')
        time.sleep(1)

"""
"""
highlighted_image = cv2.bitwise_and(image, image, mask=mask)

output_image = np.zeros_like(image)
output_image[mask > 0] = [255, 255, 255]

cv2.imshow('Original Image', image)
cv2.imshow('Highlighted Image (Color Detected)', highlighted_image)
cv2.imshow('Mask Output', output_image)

cv2.waitKey(0)
cv2.destroyAllWindows()
"""