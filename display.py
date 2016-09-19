import numpy
import math
import time

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

"""
source:
https://github.com/AidanHaddonWright/OpenGL_tutorials/blob/master/Lessons/02-%20Creating_a_first_person_perspective/main.py

install pyopengl from http://www.lfd.uci.edu/~gohlke/pythonlibs/#pyopengl

install these .whl files for 64 bits:
    pip install PyOpenGL-3.1.1-cp27-cp27m-win_amd64.whl
    pip install PyOpenGL_accelerate-3.1.1-cp27-cp27m-win_amd64.whl

install these .whl files for 32 bits:
    pip install PyOpenGL-3.1.1-cp27-cp27m-win32.whl 
    pip install PyOpenGL_accelerate-3.1.1-cp27-cp27m-win32.whl


"""


terrain = ((-50,-1,50),(-50,-1,-50),(50,-1,-50),(50,-1,50))

vertices = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
    )

faces = (
    (0,1,2,3),
    (3,2,7,6),
    (6,7,5,4),
    (4,5,1,0),
    (1,5,7,2),
    (4,0,3,6)
    )

colours = ((1,1,0),(1,0,0),(1,0,1),(0,1,1),(0,1,0),(0,0,1))

def glut_print( x,  y,  font,  text, r,  g , b , a):

    blending = False 
    if glIsEnabled(GL_BLEND) :
        blending = True

    #glEnable(GL_BLEND)
    glColor3f(1,1,1)
    glRasterPos2f(x,y)
    for ch in text :
        glutBitmapCharacter( font , ctypes.c_int( ord(ch) ) )


    if not blending :
        glDisable(GL_BLEND) 


class Camera(object):

    def __init__(self):
        self.pos = [0,0,0]
        self.rot = [0,0,0]

    def update(self):
        yaw = math.radians(-self.rot[1])

        dx,dz = math.sin(yaw),math.cos(yaw)
        
        pressed = pygame.key.get_pressed()
        if pressed[K_UP]:
            self.pos[0] += dx
            self.pos[2] -= dz

        if pressed[K_DOWN]:
            self.pos[0] -= dx
            self.pos[2] += dz

        if pressed[K_LEFT]:
            self.rot[1] += 10

        if pressed[K_RIGHT]:
            self.rot[1] -= 10

class Main(object):
    WIDTH = 600
    HEIGHT = 400

    def lock_mouse(self):
        if self.lock == True:
            pygame.mouse.set_visible(False)
            pygame.event.set_grab(1)
        else:
            pygame.mouse.set_visible(True)
            pygame.event.set_grab(0)

    def view3d(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        gluPerspective(70,(self.WIDTH/self.HEIGHT),0.1,100)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def view2d(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0.0, 1.0, 0.0, 1.0)
        glMatrixMode(GL_MODELVIEW)

        glut_print( 10 , 10 , GLUT_BITMAP_9_BY_15 , "Hallo World" , 1.0 , 1.0 , 1.0 , 1.0 )


    def startup(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        pygame.display.set_mode((self.WIDTH,self.HEIGHT), DOUBLEBUF|OPENGL)
        pygame.display.set_caption('OpenGL window')
        glutInit()
        glClearColor(0.5,0.7,1, 1.0)

        glEnable(GL_DEPTH_TEST)
    
    def __init__(self):
        self.running = True
        self.lock = True
        
        self.startup()

        self.camera = Camera()

    def run(self):
        while self.running:
            self.clock.tick(60)
            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
            self.view2d()

            self.view3d()
            
            #self.lock_mouse()
            
            self.checkForInput()

            glPushMatrix()
            rot = self.camera.rot
            glRotatef(-rot[0],1,0,0)
            glRotatef(-rot[1],0,1,0)
            x,y,z = self.camera.pos
            glTranslatef(-x,-y,-z)

            glBegin(GL_QUADS)
            i = 0
            for face in faces:
                glColor3fv(colours[i])
                for vertex in face:
                    glVertex3fv(vertices[vertex])
                i += 1
            glEnd()

            glBegin(GL_QUADS)
            for vertex in terrain:
                glColor3fv((0,0.25,0))
                glVertex3fv(vertex)
        
            glEnd()
            

            glPopMatrix()
            pygame.display.flip()
            pygame.time.wait(15)
            
    def checkForInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == K_ESCAPE:
                self.lock = False
        #update camera position with pressed keys
        self.camera.update()

if __name__ == '__main__':
    view = Main()
    view.run()
    quit()