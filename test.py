#Sarah Zhu
from cmu_graphics import *
from PIL import Image
import random
import math
import numpy as np
from matplotlib import _cm

class Time:
    def __init__(self):
        self.steps = 0
        self.seconds = 0
    
    def setTime(self, steps):
        self.steps = steps
        self.seconds = int(steps//7.3)

    def getSeconds(self):
        seconds = self.seconds%60
        if seconds>=10:
            return f'{seconds}'
        else:
            return f'0{seconds}'
    
    def getMilli(self):
        steps = ((self.steps)*10)//10
        if steps>=10:
            return f'{steps}'
        else:
            return f'0{steps}'

    def getMinutes(self):
        minutes = (self.seconds//60)%60
        if minutes>=10:
            return f'{minutes}'
        else:
            return f'0{minutes}'

def onAppStart(app):
    app.height = 600
    app.width = 800
    app.horizontalRes = 150
    app.halfVertRes = 120
    app.image = []
    app.laps = [(1,'red'),(2,'blue'),(3,'green')]
    app.lap = 0
    app.scalingFact = app.horizontalRes/60
    app.cx = 2.3
    app.cy = 12.2
    app.rot = 4.7
    app.stepsPerSecond = 100
    app.time = Time()
    app.totalSteps = 0
    app.checkpointStatus = [False,False,False,False,False]
    app.checkpointRGB = [(131,130,60),(10,14,20),(255,0,128),(0,64,65),(3,2,4)]
    app.coinColor = (255,255,128)
    app.skyColor = (0,255,255)
    app.coinCooldown = 70
    app.coinCount = 0
    #got the sprites from https://github.com/s4rd0n1k/pygame_mariokart/blob/master/sprites/mario.png
    spriteRight = loadSpritePilImages('mario.png',12, 1)
    spriteLeft = loadSpritePilImages('mario.png',12, -1)
    app.spriteLeftTurn = [CMUImage(pilImage) for pilImage in spriteLeft]
    app.spriteRightTurn = [CMUImage(pilImage) for pilImage in spriteRight]
    app.turningLeft = 0
    app.turningRight = 0
    app.rightFrame = 0
    app.leftFrame = 0
    app.leftHoldFirst = False
    app.rightHoldFirst = False
    #got rainbow road from https://mariokart.fandom.com/wiki/Tracks?file=SNES_Rainbow_Road.png
    #I edited it to look like the map you see now
    app.map = Image.open("edited_rainbow_road.png")
    app.map = app.map.resize((app.width,app.height))
    app.mapArr = app.map.convert("RGB")
    app.mapFilt = Image.new(mode="RGB",size=(app.width, app.height)).convert('RGB')
    app.result = Image.new(mode="RGB",size=(150,140)).convert('RGB')
    app.marioHitbox = []
    app.isDrifting = False
    app.win = False
    backtrack = Sound('https://soundcloud.com/safrmusic/super-mario-kart-rainbow-road-re-imagined')
    backtrack.play(loop=True)
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
    if app.win:
        drawRect(0,0,800,600,fill='black',opacity=20)
        drawLabel('Completed 3 laps!',400,200,fill='green',size=30,bold=True)
        drawLabel(f"Total Time: {app.time.getMinutes()}' {app.time.getSeconds()}" + f'"', 400, 550, size=60, bold=True, fill='white', font='orbitron')
    else:
        drawImage(app.image, app.width//2, app.height//2,align='center')
        if app.turningLeft == 0 and app.turningRight == 0:
            drawImage(app.spriteRightTurn[0],400, 450, align='center')
        elif app.turningLeft>0:
            drawImage(app.spriteLeftTurn[app.leftFrame],400, 450, align='center')
        else:
            drawImage(app.spriteRightTurn[app.rightFrame],400, 450, align='center')
        drawLine(340,0,340,600)
        drawLine(0,470,800,470)
        drawLine(0,510,800,510)
        drawCircle(400,490,4,fill='red')
        drawLabel(f"{app.time.getMinutes()}' {app.time.getSeconds()}" + f'"', 680,50,size = 40, fill = 'white', font = 'orbitron')
        label,color = app.laps[app.lap]
        drawRect(530,10,50,65, fill='gray')
        drawLabel(label, 550,40,size = 60, bold = True, fill = color)
        drawLabel('lap',580,80,fill = 'white', align = 'left-bottom')
        drawLabel(f'x{app.coinCount} coins',40,20,fill='white')
        passed = 0
        for checkpoint in app.checkpointStatus:
            if checkpoint:
                passed += 1
        drawLabel(f'{passed}/5 checkpoints passed',350,30,size = 24, fill='white',bold = True)
    #drawImage(CMUImage(app.mapFilt),0,0)


def onStep(app):
    if app.win:
        pass
    else:
        app.totalSteps += 1
        app.time.setTime(app.totalSteps)
        updateCanvas(app)
        app.coinCooldown += 1
        print(app.coinCount)
        print(app.resultCopy.getpixel((470,470)))
        print(app.checkpointStatus)
    
#main floorcasting algorithm
#learned from: https://www.youtube.com/watch?v=2Yj5mmKWukw, adjusted to fit my code
def updateCanvas(app):
    for i in range(int(app.horizontalRes)):
        rotate = app.rot + np.deg2rad(i/app.scalingFact - 30)
        sine, cos, cos2 = np.sin(rotate), np.cos(rotate), np.cos((i/app.scalingFact - 30)/180*math.pi)
        for j in range(app.halfVertRes):
            n = (app.halfVertRes/(app.halfVertRes-j))/cos2
            x,y = app.cx + cos*n, app.cy + sine*n
            X,Y = int(x*25), int (y*25)
            if 0 <= X < app.width and 0 <= Y < app.height:
                app.mapFilt.putpixel((i, app.halfVertRes*5 - j - 1), app.mapArr.getpixel((X, Y)))
            else:
                app.mapFilt.putpixel((i, app.halfVertRes*5 - j - 1), (0, 255, 255))
    #splicing a smaller image and resizing it
    for i in range(150):
        for j in range(140):
            app.result.putpixel((i,j),(app.mapFilt.getpixel((i,460+j))))      
    app.resultCopy = app.result.resize((800,600))
    app.marioHitbox = [] 
    #getting mario's hitbox   
    for i in range(130):
        newRow = []
        for j in range(40):
            newRow.append((app.resultCopy.getpixel((340+i,470+j))))    
        app.marioHitbox.append(newRow)
    passedCheckPoint(app)
    if app.coinCount<10 and checkCollision(app,app.coinColor) and app.coinCooldown>70:
        app.coinCount += 1
        app.coinCooldown = 0
    app.image = CMUImage(app.resultCopy)

def passedCheckPoint(app):
    for i in range(len(app.checkpointRGB)):
        color = app.checkpointRGB[i]
        if checkCollision(app,color) and (i==0 or app.checkpointStatus[i-1] == True):
            app.checkpointStatus[i] = True
            break
    allCheckPassed = True
    for checkpoint in app.checkpointStatus:
        if not checkpoint:
            allCheckPassed = False
    if allCheckPassed:
        app.lap+= 1
        app.checkpointStatus = [False,False,False,False,False]
        if app.lap>0:
            app.win = True
            app.lap = 0

def checkCollision(app, color):
    for row in app.marioHitbox:
        if color in row:
            return True
    return False 

def isClose(app,color1,color2):
    a,b,c = color1
    x,y,z = color2
    return abs(a-x)<5 and abs(b-y)<5 and abs(c-z)<5

#controls
def onKeyHold(app, keys):
    if ('space' in keys):
        app.isDrifting = True
    if ('left' in keys) and not(app.rightHoldFirst):
        if 'right' not in keys:
            app.leftHoldFirst = True
        ogRot = app.rot
        app.rot -= 0.05
        if app.isDrifting:
            app.rot-=0.03
            app.leftFrame = 3
        elif app.turningLeft<2:
            app.leftFrame += 1
        app.turningLeft += 1
        #updateCanvas(app)
        if checkCollision(app,app.skyColor):
            app.rot = ogRot
    elif 'right' in keys and not(app.leftHoldFirst):
        app.rightHoldFirst = True
        ogRot = app.rot
        app.rot += 0.05
        if app.isDrifting:
            app.rot += 0.03
            app.rightFrame = 3
        elif app.turningRight<2:
            app.rightFrame += 1
        app.turningRight += 1
        #updateCanvas(app)
        if checkCollision(app,app.skyColor):
                app.rot = ogRot
    if 'up' in keys:
        ogx = app.cx
        ogy = app.cy
        app.cx += math.cos(app.rot)*(0.1+0.025*app.coinCount)
        app.cy += math.sin(app.rot)*(0.1+0.025*app.coinCount)
        #updateCanvas(app)
        if checkCollision(app,app.skyColor):
                app.cx = ogx
                app.cy = ogy
    if 'down' in keys:
        ogx = app.cx
        ogy = app.cy
        app.cx -= math.cos(app.rot)*0.1
        app.cy -= math.sin(app.rot)*0.1
        #updateCanvas(app)
        #if checkCollision(app,app.skyColor):
        #        app.cx = ogx
        #        app.cy = ogy
    #print('-------------------')
    #print(app.marioHitbox)
def onKeyRelease(app,key):
    if ('left' == key):
        app.leftFrame = 0
        app.turningLeft = 0
        app.leftHoldFirst = False
    elif 'right' == key:
        app.rightHoldFirst = False
        app.turningRight = 0
        app.rightFrame = 0
    elif ('space' == key):
        app.isDrifting = False
        if app.turningLeft>0 or app.turningRight>0:
            app.frame = 1

def main():
    runApp()
main()