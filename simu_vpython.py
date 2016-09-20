from __future__ import division
from visual import *
import random
import Image # Must install PIL

speed = 0.
speedrotation = 0.


def key_callback(evt):
    global speed
    global speedrotation
    if evt.event == 'keydown':
        #move in / out
        if evt.key == 'up':
            speed += .2
        if evt.key == 'down':
            speed -= .2
        if evt.key == 'space':
            speed = 0
        if evt.key == 'left':
            speedrotation = pi/16.
        if evt.key == 'right':
            speedrotation = -pi/16.

    if evt.event == 'keyup':
        if evt.key == 'left':
            speedrotation = 0
        if evt.key == 'right':
            speedrotation = 0
        



if __name__ == '__main__':

    # Set up window and sceen.
    scene = display()
    scene.fullscreen = 0
    scene.autocenter = 0
    scene.autoscale = 0
    scene.userzoom = 0
    scene.userspin = 1
    scene.ambient = 0
    scene.bind('keydown', key_callback)
    scene.bind('keyup', key_callback)
    outer = 10
    outer*= 2
    #scene.range = (outer,outer,outer)

    #sphere
    sunpos = [0,0,0]
    color = [ 3, 1.5, .75]
    sunradius = 2
    #sun = sphere( pos=sunpos, radius=sunradius, color=color)

    #circuit = sol
    img = Image.open("piste2.png")
    #img = img.resize((128,128), Image.ANTIALIAS)
    print "image size:", img.size
    #materials.saveTGA("circuit",img)
    tex = materials.texture(data=img, mapping="top")
    box(pos=(0,-2,0), length=100, width=100, height=.5, material=tex)

    #box(pos=(-1,-1,-2), length=200, height=2, width=200, material=materials.wood)


    while True:
        rate(50)              
        
        if speed != 0:
            #move camera
            scene.center = scene.center+scene.forward*float(speed)

        if speedrotation != 0:
            ray = 0
            newforward = rotate(scene.forward, axis=scene.up, angle=speedrotation)
            scene.center = scene.mouse.camera+newforward*mag(scene.center-scene.mouse.camera)
            scene.forward = newforward
            scene.center = scene.center+scene.forward*ray/2.

                
