import requests
import datetime
from PIL import Image
from constants import url
import json
import random

def decision(probability):
    return random.random() < probability

def getImage():
    now = datetime.datetime.now()
    dt_str = now.strftime("%Y-%m-%dT%H:%M:%Sz")
    newurl = url.format(WIDTH=3840, HEIGHT=2160, DATE=dt_str)
    r = requests.get(newurl)
    img_data = r.json()["batchrsp"]["items"][0]
    # ["ad"]["image_fullscreen_001_landscape"]["u"]
    img_url = json.loads(img_data["item"])["ad"]["image_fullscreen_001_landscape"]["u"]
    r = requests.get(img_url)
    with open("uhd.jpg", "wb") as f:
        f.write(r.content)

def mod_image_repeat_rows(imgname, chance_of_row_repeat=0, max_row_repeats=0, min_row_repeats=0, save=True):
    img = Image.open(imgname)
    pixels = img.load()
    width, height = img.size

    repeat = False
    num_repeats = 0
    times_to_repeat = 0
    row_to_repeat = []
    for y in range(height):
        if not repeat and decision(chance_of_row_repeat):
            repeat = True
            times_to_repeat = random.randint(min_row_repeats, max_row_repeats)
            print("Repeat true: " + str(times_to_repeat))
        for x in range(width):
            r, g, b = img.getpixel((x, y))

            if repeat and len(row_to_repeat) != width:
                pixels[x, y] = (r, g, b)
                row_to_repeat.append((r, g, b))
            elif repeat:
                pixels[x, y] = row_to_repeat[x]
            else:
                pixels[x, y] = (r, g, b)
        
        if repeat:
            num_repeats += 1
            if num_repeats >= times_to_repeat:
                repeat = False
                times_to_repeat = 0
                num_repeats = 0
                row_to_repeat = []
    if save:
        img.save("test1.jpg")

getImage()
mod_image_repeat_rows("uhd.jpg", 0.008, 30, 10)