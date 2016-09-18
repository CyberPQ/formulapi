#!/bin/env python

import Wireframe as wf
import pygame
import numpy as np
from math import pi as PI

key_to_function = {
    pygame.K_LEFT:   (lambda x: x.rotate(1)),
    pygame.K_RIGHT:  (lambda x: x.rotate(-1)),
    pygame.K_DOWN:   (lambda x: x.move(-1)),
    pygame.K_UP:     (lambda x: x.move(1)),
    pygame.K_EQUALS: (lambda x: x.scaleAll(1.25)),
    pygame.K_MINUS:  (lambda x: x.scaleAll( 0.8)),
    pygame.K_q:      (lambda x: x.rotateAll('X',  0.1)),
    pygame.K_w:      (lambda x: x.rotateAll('X', -0.1)),
    pygame.K_a:      (lambda x: x.rotateAll('Y',  0.1)),
    pygame.K_s:      (lambda x: x.rotateAll('Y', -0.1)),
    pygame.K_z:      (lambda x: x.rotateAll('Z',  0.1)),
    pygame.K_x:      (lambda x: x.rotateAll('Z', -0.1))}


def rotateZMatrix(radians):
    """ Return matrix for rotating about the z-axis by 'radians' radians """
    
    c = np.cos(radians)
    s = np.sin(radians)
    return np.array([[c,-s, 0],
                     [s, c, 0],
                     [0, 0, 1]])

def deplacementmatrix(d, orientation):
    theta = orientation[0]
    md = np.array([[d*np.cos(theta), 0, 0],
                   [0, d*np.sin(theta),0],
                   [0,0,0]])
    return md

class ProjectionViewer:
    """ Displays 3D objects on a Pygame screen """

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Wireframe Display')
        self.background = (10,10,50)

        self.wireframes = {}
        self.displayNodes = True
        self.displayEdges = True
        self.nodeColour = (255,255,255)
        self.edgeColour = (200,200,200)
        self.nodeRadius = 4

        self.clock = pygame.time.Clock()
        self.frametime = 0
        self.font = pygame.font.SysFont(pygame.font.get_default_font(), 20)

        #position (x,y,z) dans le plan de la carte z = altitude
        self.eyepoint = np.array([0, 0, 0])
        self.camera = np.array([0, 0, 0])
        # rotation angle en radian
        self.orientation = np.array([PI/2, 0, 0])
        # speed modifiers
        self.movespeed = 0 # the constant value is in meter / second
        self.rotspeed = 0 # the constant value is in radians / second

    def addWireframe(self, name, wireframe):
        """ Add a named wireframe object. """

        self.wireframes[name] = wireframe

    def computespeed(self):
        # speed modifiers
        self.movespeed = self.frametime * 1.0 # the constant value is in squares / second
        self.rotspeed = self.frametime * 1.0 # the constant value is in radians / second
    
    def run(self):
        """ Create a pygame screen until it is closed. """

        running = True
        while running:
            self.clock.tick(60)
            self.frametime = float(self.clock.get_time()) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key in key_to_function:
                        key_to_function[event.key](self)
            
            self.computespeed()
            self.display()  
            pygame.display.flip()
        
    def display(self):
        """ Draw the wireframes on the screen. """

        self.screen.fill(self.background)
        
        self.displayinfo()

        for wireframe in self.wireframes.values():
            if self.displayEdges:
                for n1, n2 in wireframe.edges:
                    pygame.draw.aaline(self.screen, self.edgeColour, wireframe.nodes[n1][:2], wireframe.nodes[n2][:2], 1)

            if self.displayNodes:
                for node in wireframe.nodes:
                    pygame.draw.circle(self.screen, self.nodeColour, (int(node[0]), int(node[1])), self.nodeRadius, 0)

    def displayinfo(self):
        infos = [str(self.clock.get_fps()),
                 'eyepoint:%r, orientation:%r' %(self.eyepoint, self.orientation),
                 'movespeed:%f, rotspeed:%f' %(self.movespeed, self.rotspeed)]
        h = 0
        for info in infos:
            text = self.font.render(info, False, (255, 255, 0))
            self.screen.blit(text, (text.get_rect()[0], h), text.get_rect())
            h += text.get_rect()[3] - text.get_rect()[1]

    
    def translateAll(self, axis, d):
        """ Translate all wireframes along a given axis by d units. """

        for wireframe in self.wireframes.itervalues():
            wireframe.translate(axis, d)

    def scaleAll(self, scale):
        """ Scale all wireframes by a given scale, centred on the centre of the screen. """

        centre_x = self.width/2
        centre_y = self.height/2

        for wireframe in self.wireframes.itervalues():
            wireframe.scale((centre_x, centre_y), scale)

    def rotateAll(self, axis, theta):
        """ Rotate all wireframe about their centre, along a given axis by a given angle. """

        rotateFunction = 'rotate' + axis

        for wireframe in self.wireframes.itervalues():
            centre = wireframe.findCentre()
            getattr(wireframe, rotateFunction)(centre, theta)

    def move(self, dir):
        theta = self.orientation[0]
        d = 1
        md = np.array([dir*d*np.cos(theta), dir*d*np.sin(theta),0])
        self.eyepoint = md + self.eyepoint

    def rotate(self, dir):
        self.orientation = np.dot(rotateZMatrix(dir*self.rotspeed), self.orientation)
        


if __name__ == '__main__':
    pygame.init()
    pv = ProjectionViewer(800, 600)

    cube = wf.Wireframe()
    cube_nodes = [(x,y,z) for x in (50,250) for y in (50,250) for z in (50,250)]
    cube.addNodes(np.array(cube_nodes))
    cube.addEdges([(n,n+4) for n in range(0,4)]+[(n,n+1) for n in range(0,8,2)]+[(n,n+2) for n in (0,1,4,5)])
    
    pv.addWireframe('cube', cube)
    pv.run()