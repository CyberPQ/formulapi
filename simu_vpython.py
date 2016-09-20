from __future__ import division
from visual import *
import random

if __name__ == '__main__':

    # Set up window and sceen.
    scene = display()
    scene.fullscreen = 0
    scene.autocenter = 0
    scene.autoscale = 0
    scene.userzoom = 0
    scene.userspin = 1
    scene.ambient = 0
    outer = 10
    outer*= 2
    scene.range = (outer,outer,outer)

    sunpos = [0,0,0]
    color = [ 3, 1.5, .75]
    sunradius = 2
    sun = sphere( pos=sunpos, radius=sunradius, color=color)

    speed = 0.

    while True: 
        rate(50)              
        
        if speed != 0:
            scene.center = scene.center+scene.forward*float(speed)
        
        if scene.kb.keys:
            key = scene.kb.getkey()
            angle = 0
            #move in / out
            if key == 'up':
                speed += .2
            if key == 'down':
                speed -= .2

            #strafe left / right
            if key == 'a' or key == 'd':
                move = vector(-0.5,0,0)
                if key == 'd':
                    move = vector(0.5,0,0)
                scene.center = scene.center+move
            #look left / right
            if key == 'left' or key == 'right':
                ray = 0
                angle = 0.6
                if key == 'right':
                    angle = -0.6
                newforward = rotate(scene.forward, axis=scene.up, angle=angle/10.)
                scene.center = scene.mouse.camera+newforward*mag(scene.center-scene.mouse.camera)
                scene.forward = newforward
                scene.center = scene.center+scene.forward*ray/2.
            #move up / down
            if key == 'f' or key == 'v':
                move = vector(0,-0.5,0)
                if s == 'v':
                    move = vector(0,0.5,0)
                scene.center = scene.center+move