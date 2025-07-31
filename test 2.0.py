from cmu_graphics import *
import math

def onAppStart(app):
    app.obs = [20,20,-50]
    app.width = 600
    app.height = 800
    app.setMaxShapeCount(100000)
    app.theta = 55*math.pi/180
    app.tot = math.tan(app.theta)
    onStep(app)

def redrawAll(app):
    for i in range(50):
        for j in range(50):
            xp,yp= convert(app, app.coords[i][j],app.obs)
            drawCircle(xp,yp,1,fill='green')


def convert(app, coordinates, obs):
    xr = coordinates[0]-obs[0]
    yr = coordinates[1]-obs[1]
    zr = coordinates[2]-obs[2]

    dyz = (yr**2 + zr**2)**0.5
    dxz = (xr**2 + zr**2)**0.5

    xp = 2000
    yp = 2000

    if dyz>0:
        xp = app.height*(xr*(app.tot)/(2*dyz)+0.5)
    if dxz>0:
        yp = app.width*(yr*(app.tot)/(2*dxz)+0.5)
    return xp,yp

def onStep(app):
    app.tot = math.tan(app.theta)
    app.coords = []
    for i in range(50):
        add = []
        for j in range(50):
            add.append([i,0,j])
        app.coords.append(add)

def onKeyHold(app, keys):
    if 'left' in keys:
        app.obs[0] -= 0.2
    if 'right' in keys:
        app.obs[0] += 0.2
    if 'up' in keys:
        app.obs[1] -= 0.2
    if 'down' in keys:
        app.obs[1] += 0.2
    if 'w' in keys:
        app.obs[2] += 0.2
    if 's' in keys:
        app.obs[2] -= 0.2

def main():
    runApp(app)
    
main()