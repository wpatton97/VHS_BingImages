import requests
import datetime
from PIL import Image
from constants import url
import json

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

def mod_image(imgname):
    img = Image.open(imgname)
    pixels = img.load()
    width, height = img.size
    for y in range(height):
        for x in range(width):
            r, g, b = img.getpixel((x, y))
            pixels[x, y] = (b, b, b)
    img.save("test1.jpg")

getImage()
mod_image("uhd.jpg")