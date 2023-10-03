import numpy as np
import matplotlib.pyplot as plt
import json
import io

from PIL import Image

from typing import Union
from fastapi import FastAPI, Response
app = FastAPI()

if not hasattr(Image, 'Resampling'):
  Image.Resampling = Image

## GLOBALS ##
PIXELS = 128

TILE_TRANSFORM = (
    (0, 'blocked'),  
    (1, 'grass'), 
    (2, 'soiledDry'),
    (3, 'seededDry'),
    (4, 'growingDry'),
    (5, 'readyDry'),
    (6, 'soiledWathered'),
    (7, 'seededWathered'),
    (8, 'growingWathered'),
    (9, 'readyWathered')
)

tiles = {}
for _, tile_name in TILE_TRANSFORM:
    tiles[tile_name] = Image.open(f'img/{tile_name}.png').convert('RGBA')
    tiles[tile_name].load()


## Server ##
@app.get("/farms/")
def read_root():
    return {"API": "Farm"}

@app.get("/farms/{id}",  
    responses = {
        200: {
            "content": {"image/png": {}}
        }
    },
    response_class=Response
)
def farm(id: str):

    ## Get image ##
    data = requestConstructionAPI(id)

    ## Parse it into bytes ##
    imageBytes = getFarm(data)

    ## Send it ##
    return Response(content=imageBytes, media_type="image/png")


def requestConstructionAPI(id=None):

    if id == None:
        data = open("response.json")
        return json.load(data)
    else:
        data = open("response.json")
        data = json.load(data)
        for key, item in data.items():
            if item["granja"]["userId"] == id:
                return item["granja"]

### Farm dict to ImageArray ###
def getFarm(farm):

    ## Get data ##
    HEIGHT = farm["expansion_actual"][0]
    WIDTH = farm["expansion_actual"][1]
    
    MAX_HEIGHT = farm["expansion_maxima"][0]
    MAX_WIDTH = farm["expansion_maxima"][1]

    buildings = farm["construcciones"]

    ## Make data structure of farm ##
    dataset = np.zeros((MAX_HEIGHT, MAX_WIDTH))
    dataset[MAX_HEIGHT-HEIGHT:, 0:WIDTH] = 1
    for position, build in buildings.items():
        coordinates = position.split(",")
        x = int(coordinates[0].strip())
        y = int(coordinates[1].strip())

        temp = 0
        if(build["readyToPlant"] == 1):
            temp = 2

        if(build["hasPlant"] == 1 and build["grownDays"] in [0, 1]):
            temp = 3

        if(build["hasPlant"] == 1 and build["grownDays"] > 1):
            temp = 4

        if(build["hasPlant"] == 1 and build["daysTillDone"] == 0):
            temp = 5

        if(build["isWatered"] == 1):
            temp += 4

        dataset[MAX_HEIGHT-y-1][x] = temp

    ## Reshape ##
    room = np.reshape(dataset, (MAX_HEIGHT, MAX_WIDTH))

    ## Generate Image ##
    assert room.shape == (MAX_HEIGHT, MAX_WIDTH)
    
    canvas = Image.new('RGBA', (PIXELS*MAX_WIDTH, PIXELS*MAX_HEIGHT))
    
    for i in range(MAX_WIDTH):
        for j in range(MAX_HEIGHT):
            canvas.paste(tiles['blocked'], (i*PIXELS, j*PIXELS))

    for tile_number, tile_name in TILE_TRANSFORM:
        J, I = np.nonzero(room == tile_number)
        for x in range(I.size):
            canvas.alpha_composite(tiles[tile_name], (I[x]*PIXELS, J[x]*PIXELS))
            
    image = canvas.resize((2*PIXELS*MAX_WIDTH, 2*PIXELS*MAX_HEIGHT), resample=Image.Resampling.BOX)

    ## Turn image into bytes ##
    imgByteArr = io.BytesIO()
    image.save(imgByteArr, format="PNG")
    #image.save("output.png")
    imgByteArr = imgByteArr.getvalue()
    
    return imgByteArr