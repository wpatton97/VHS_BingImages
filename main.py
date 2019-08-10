import requests
import datetime
# from PIL.Image import core
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

getImage()