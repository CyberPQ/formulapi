#!/bin/env python

import Wireframe as wf
import pygame
import numpy as np
import math
from math import pi as PI

key_to_function = {
    pygame.K_LEFT:   (lambda x: x.rotate(-1)),
    pygame.K_RIGHT:  (lambda x: x.rotate(1)),
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


def rotateYMatrix(radians):
    """ Return matrix for rotating about the z-axis by 'radians' radians """
    
    c = np.cos(radians)
    s = np.sin(radians)
    return np.array([[ c, 0, s],
                     [ 0, 1, 0],
                     [-s, 0, c]])

def cameratransform(vector, orientation):
    cx = np.cos(orientation[0])
    cy = np.cos(orientation[1])
    cz = np.cos(orientation[2])
    sx = np.sin(orientation[0])
    sy = np.sin(orientation[1])
    sz = np.sin(orientation[2])
    m1 = np.array([[1 ,0 ,0],
                   [0, cx, sx],
                   [0, -sx, cx]])
    m2 = np.array([[cy ,0 ,-sy],
                   [0, 1, 0],
                   [sy, 0, cy]])
    m3 = np.array([[cz ,sz ,0],
                   [-sz, cz, 0],
                   [0, 0, 1]])
    r = np.dot(m1, m2)
    r = np.dot(r, m3)
    r = np.dot(r, vector)
    return r

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
        self.objects = {'essai':[(0,3,5), (5,3,5), (5,5,5), (0,5,5)]}

        self.clock = pygame.time.Clock()
        self.frametime = 0
        self.font = pygame.font.SysFont(pygame.font.get_default_font(), 20)

        #position (x,y,z) dans le plan de la carte y = altitude (left handed system)
        """
        y  z
        | /
        |/______x

        le plan xz est le sol
        """
        self.eyepoint = np.array([0, 2, 0])
        self.camera = np.array([0, 2, 0])
        # rotation angle en radian
        self.orientation = np.array([0, 0, 0])
        # speed modifiers
        self.movespeed = 0 # the constant value is in meter / second
        self.rotspeed = 0 # the constant value is in radians / second
        #focal, pour un angle de vision a 135 degre, la distance entre eye et camera est
        # d = screen width / 2*tan(135)
        self.distancefocale = self.width / abs(2 * math.tan(PI*135/180))

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
        """ Draw on the screen. """

        self.screen.fill(self.background)
        self.displayinfo()
        self.displayobjects()

    def displayobjects(self):
        for obj in self.objects:
            newpoints = []
            for point in self.objects[obj]:
                ax = point[0]
                ay = point[1]
                az = point[2]
                camera = self.eyepoint
                print 'point:',point
                print 'camera:',camera
                print 'point - camera:',point - camera
                d = cameratransform(point - camera, self.orientation)
                print 'd:',d
                ez = self.distancefocale
                b1 = d[0] * ez / d[2]
                b2 = d[1] * ez / d[2]
                print 'result:',(b1,b2)
                newpoints.append((b1, b2))
            screennewpoints = self.toscreencoord(newpoints)
            print screennewpoints
            pygame.draw.polygon(self.screen, (255,0,0), self.toscreencoord(newpoints) )
            #pour verification
            theorie = [(10/5, 0),(15/5, 0),(15/5,3./5),(10/5,3./5)]
            attendu = self.toscreencoord(theorie, 100)
            pygame.draw.polygon(self.screen, (0,255,0), attendu)

    def toscreencoord(self, points, scale=1):
        result = []
        for point in points:
            a = (float(point[0])* float(scale) + self.width/2) 
            b = (self.height - float(point[1])* float(scale)) 
            result.append((a,b))
        return result
    
    def displayinfo(self):
        infos = [str(self.clock.get_fps()),
                 'eyepoint:%r, orientation:%r' %(self.eyepoint, self.orientation),
                 'movespeed:%f, rotspeed:%f' %(self.movespeed, self.rotspeed)]
        h = 0
        for info in infos:
            text = self.font.render(info, False, (255, 255, 0))
            self.screen.blit(text, (text.get_rect()[0], h), text.get_rect())
            h += text.get_rect()[3] - text.get_rect()[1]
   

    def move(self, dir):
        theta = self.orientation[0]
        d = 1
        md = np.array([dir*d*np.cos(theta), 0, dir*d*np.sin(theta)])
        self.eyepoint = md + self.eyepoint

    def rotate(self, dir):
        angle = PI/16
        self.orientation = self.orientation + dir*np.array([0,angle,0])
        


if __name__ == '__main__':
    pygame.init()
    pv = ProjectionViewer(800, 600)

    cube = wf.Wireframe()
    cube_nodes = [(x,y,z) for x in (50,250) for y in (50,250) for z in (50,250)]
    cube.addNodes(np.array(cube_nodes))
    cube.addEdges([(n,n+4) for n in range(0,4)]+[(n,n+1) for n in range(0,8,2)]+[(n,n+2) for n in (0,1,4,5)])
    
    pv.addWireframe('cube', cube)
    pv.run()