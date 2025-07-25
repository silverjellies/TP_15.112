from cmu_graphics import *
from PIL import Image
import random
import math
import numpy as np
from matplotlib import _cm

def onAppStart(app):
    app.height = 600
    app.width = 800
    app.horizontalRes = 150
    app.halfVertRes = 120
    app.scalingFact = app.horizontalRes/50
    app.cx = 50
    app.cy = 250
    app.rot = 120
    app.stepsPerSecond = 100
    app.map = Image.open("SNES_Rainbow_Road.jpg")
    app.map = app.map.resize((app.width,app.height))
    app.mapArr = app.map.convert("RGB")
    app.mapFilt = Image.new(mode="RGB",size=(app.width, app.height)).convert('RGB')

def redrawAll(app):
    image = CMUImage(app.mapFilt)
    drawImage(image, 0, 0)

def onStep(app):
    for i in range(app.horizontalRes):
        rotate = app.rot + np.deg2rad(i/app.scalingFact - 30)
        sine, cos, cos2 = np.sin(rotate), np.cos(rotate), np.cos((i/app.scalingFact - 30)/180*math.pi)
        for j in range(app.halfVertRes):
            n = (app.halfVertRes/(app.halfVertRes-j))/cos2
            x,y = app.cx + cos*n, app.cy + sine*n
            X,Y = int(x/30%1*800), int (y/30%1*600)
            app.mapFilt.putpixel((i,app.halfVertRes*5-j-1),(app.mapArr.getpixel((X,Y))))
            app.image = CMUImage(app.mapFilt)

def onKeyPress(app, key):
    if key == 'left':
        app.rot -= 0.1
    elif key == 'right':
        app.rot += 0.1
    elif key == 'up':
        app.cx += math.cos(app.rot)*0.1
        app.cy += math.sin(app.rot)*0.1
    elif key == 'down':
        app.cx -= math.cos(app.rot)*0.1
        app.cy -= math.sin(app.rot)*0.1

def main():
    runApp()
main()