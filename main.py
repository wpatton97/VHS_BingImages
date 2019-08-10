import requests
import datetime
from PIL import Image
import colorsys
from constants import url
import json
import numpy as np
import imageio
import random
from math import floor


def generate_offsets(array_size, max_offset):
    periodicity = random.randint(1, 10)
    periodicity = random.random() * periodicity
    print(periodicity)
    offsets = []
    for i in range(array_size):
        # print(floor(max_offset*np.sin(periodicity*(i*np.pi/180))))
        offsets.append(floor(max_offset*np.sin(periodicity*(i*np.pi/180))))
    return offsets


def HSVColor(img):
    if isinstance(img,Image.Image):
        r,g,b = img.split()
        Hdat = []
        Sdat = []
        Vdat = [] 
        for rd,gn,bl in zip(r.getdata(),g.getdata(),b.getdata()) :
            h,s,v = colorsys.rgb_to_hsv(rd/255.,gn/255.,bl/255.)
            Hdat.append(int(h*255.))
            Sdat.append(int(s*255.))
            Vdat.append(int(v*255.))
        r.putdata(Hdat)
        g.putdata(Sdat)
        b.putdata(Vdat)
        return Image.merge('RGB',(r,g,b))
    else:
        return None

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
    offsets = []
    for y in range(height):
        if not repeat and decision(chance_of_row_repeat):
            repeat = True
            times_to_repeat = random.randint(min_row_repeats, max_row_repeats)
            offsets = generate_offsets(times_to_repeat, random.randint(10, 50))
            print("Repeat true: " + str(times_to_repeat))
        for x in range(width):
            r, g, b = img.getpixel((x, y))

            if repeat and len(row_to_repeat) != width:
                pixels[x, y] = (r, g, b)
                row_to_repeat.append((r, g, b))
            elif repeat:
                try:
                    pixels[x, y] = row_to_repeat[x + offsets[num_repeats]]
                except Exception as e:
                    pixels[x, y] = row_to_repeat[x - offsets[num_repeats]]
            else:
                pixels[x, y] = (r, g, b)
        
        if repeat:
            num_repeats += 1
            if num_repeats >= times_to_repeat:
                repeat = False
                times_to_repeat = 0
                num_repeats = 0
                row_to_repeat = []
                offsets = []
    if save:
        img.save("test1.jpg")


def add_img_noise(imgpath, intensity=1):
    img = imageio.imread(imgpath, pilmode='RGB')
    noise1 = img + intensity * img.std() * np.random.random(img.shape)
    imageio.imwrite("test2.jpg", noise1)

def offset_hue(image):
    if isinstance(image, str):
        image = Image.open(image)
        image = HSVColor(image)
        print(image.mode)
    pass
    
getImage()
mod_image_repeat_rows("uhd.jpg", 0.012, 50, 10)
add_img_noise("test1.jpg")

#generate_offsets(30, 50)

#offset_hue("uhd.jpg")