from PIL import ImageGrab
import os
import json

try:
    os.path.abspath('./img/bubble.png')
except:
    pass

with open(os.path.abspath('./settings.json'), 'r') as file:
    settings = json.loads(file.read())

screenshot = ImageGrab.grab(bbox=settings["bounding_boxes"]["exclamation"])
screenshot.save(os.path.abspath('./img/bubble.png'))