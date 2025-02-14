from PIL import ImageGrab, Image
import os
try:
    os.remove("img/bubble.png")
except:
    pass
screenshot = ImageGrab.grab(bbox=(1406, 247, 1468, 308))
screenshot.save("img/bubble.png")