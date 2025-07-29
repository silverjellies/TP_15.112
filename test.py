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
    app.image = []
    app.scalingFact = app.horizontalRes/50
    app.cx = 50
    app.cy = 250
    app.rot = 120
    app.stepsPerSecond = 100
    app.map = Image.open("SNES_Rainbow_Road.jpg")
    app.map = app.map.resize((app.width,app.height))
    app.mapArr = app.map.convert("RGB")
    app.mapFilt = Image.new(mode="RGB",size=(app.width, app.height)).convert('RGB')
    app.result = Image.new(mode="RGB",size=(150,140)).convert('RGB')
    onStep(app)

def redrawAll(app):
    
    drawImage(app.image, app.width//2, app.height//2,align='center')

def onStep(app):
    for i in range(int(app.horizontalRes)):
        rotate = app.rot + np.deg2rad(i/app.scalingFact - 30)
        sine, cos, cos2 = np.sin(rotate), np.cos(rotate), np.cos((i/app.scalingFact - 30)/180*math.pi)
        for j in range(app.halfVertRes):
            n = (app.halfVertRes/(app.halfVertRes-j))/cos2
            x,y = app.cx + cos*n, app.cy + sine*n
            X,Y = int(x/25%1*800), int (y/25%1*600)
            app.mapFilt.putpixel((i,app.halfVertRes*5-j-1),(app.mapArr.getpixel((X,Y))))
    #app.image = CMUImage(app.mapFilt)

    for i in range(150):
        for j in range(140):
            app.result.putpixel((i,j),(app.mapFilt.getpixel((i,460+j))))
            
    app.resultCopy = app.result.resize((800,600))         
    app.image = CMUImage(app.resultCopy)
'''
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
    onStep(app)
'''
def onKeyHold(app, keys):
    if ('left' in keys):
        app.rot -= 0.1
    elif 'right' in keys:
        app.rot += 0.1
    elif 'up' in keys:
        app.cx += math.cos(app.rot)*0.1
        app.cy += math.sin(app.rot)*0.1
    elif 'down' in keys:
        app.cx -= math.cos(app.rot)*0.1
        app.cy -= math.sin(app.rot)*0.1

def main():
    runApp()
main()