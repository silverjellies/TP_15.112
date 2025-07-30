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
    app.cx = 70
    app.cy = 280
    app.rot = 120
    app.stepsPerSecond = 100
    spriteRight = loadSpritePilImages('mario.png',12, 1)
    spriteLeft = loadSpritePilImages('mario.png',12, -1)
    app.spriteLeftTurn = [CMUImage(pilImage) for pilImage in spriteLeft]
    app.spriteRightTurn = [CMUImage(pilImage) for pilImage in spriteRight]
    app.turningLeft = 0
    app.turningRight = 0
    app.frame = 0
    app.map = Image.open("rainbow_road.png")
    app.map = app.map.resize((app.width,app.height))
    app.mapArr = app.map.convert("RGB")
    app.mapFilt = Image.new(mode="RGB",size=(app.width, app.height)).convert('RGB')
    app.result = Image.new(mode="RGB",size=(150,140)).convert('RGB')
    
    onStep(app)

def loadSpritePilImages(path, numSprites, flip):
    spritestrip = Image.open(path)
    spritePilImages = [ ]
    for i in range(numSprites):
        leftMargin = 0
        spacing = 32
        imageWidth = 30
        topMargin = 0
        imageHeight = 30
        spriteImage = spritestrip.crop((leftMargin+spacing*i, topMargin, 
                                        leftMargin+imageWidth+spacing*i, topMargin+imageHeight))
        spriteImage = spriteImage.resize((130,130))
        if flip == -1:
            spriteImage = spriteImage.transpose(Image.FLIP_LEFT_RIGHT)
        spritePilImages.append(spriteImage)
    
    return spritePilImages

def redrawAll(app):
    
    drawImage(app.image, app.width//2, app.height//2,align='center')
    if app.turningLeft == 0 and app.turningRight == 0:
        drawImage(app.spriteRightTurn[0],400, 450, align='center')
    elif app.turningLeft>0:
        drawImage(app.spriteLeftTurn[app.frame],400, 450, align='center')
    else:
        drawImage(app.spriteRightTurn[app.frame],400, 450, align='center')


def onStep(app):
    for i in range(int(app.horizontalRes)):
        rotate = app.rot + np.deg2rad(i/app.scalingFact - 30)
        sine, cos, cos2 = np.sin(rotate), np.cos(rotate), np.cos((i/app.scalingFact - 30)/180*math.pi)
        for j in range(app.halfVertRes):
            n = (app.halfVertRes/(app.halfVertRes-j))/cos2
            x,y = app.cx + cos*n, app.cy + sine*n
            X,Y = int(x/27%1*800), int (y/27%1*600)
            app.mapFilt.putpixel((i,app.halfVertRes*5-j-1),(app.mapArr.getpixel((X,Y))))
    #app.image = CMUImage(app.mapFilt)

    for i in range(150):
        for j in range(140):
            app.result.putpixel((i,j),(app.mapFilt.getpixel((i,460+j))))
            
    app.resultCopy = app.result.resize((800,600))         
    app.image = CMUImage(app.resultCopy)

def onKeyHold(app, keys):
    if ('left' in keys):
        app.rot -= 0.1
        if app.turningLeft<2:
            app.frame += 1
        app.turningLeft += 1
        if app.turningLeft>10:
            app.frame = 3
    elif 'right' in keys:
        app.rot += 0.1
        if app.turningRight<2:
            app.frame += 1
        app.turningRight += 1
        if app.turningRight>10:
            app.frame = 3
    elif 'up' in keys:
        app.cx += math.cos(app.rot)*0.1
        app.cy += math.sin(app.rot)*0.1
        print(app.mapArr.getpixel((app.cx,app.cy)))
        if (app.mapArr.getpixel((app.cx,app.cy))==(0,255,255)):
            app.cx -= math.cos(app.rot)*0.1
            app.cy -= math.sin(app.rot)*0.1
            
    elif 'down' in keys:
        app.cx -= math.cos(app.rot)*0.1
        app.cy -= math.sin(app.rot)*0.1

def onKeyRelease(app,key):
    if ('left' == key):
        app.frame = 0
        app.turningLeft = 0
    elif 'right' == key:
        app.turningRight = 0
        app.frame = 0

def main():
    runApp()
main()