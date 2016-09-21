import numpy
import math
import time
import sys
import threading
import BaseHTTPServer
import httpserver
import imagebuffer

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

H = -1
terrain = ((-50,H,50),(-50,H,-50),(50,H,-50),(50,H,50))
terraintex = ((0.0, 0.0),(1.0, 0.0),(1.0, 1.0),(0.0, 1.0))

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

def drawText(x, y, text):                                                
    position = (x, y, 0)                                                       
    font = pygame.font.Font(None, 64)                                          
    textSurface = font.render(text, True, (255,255,255,255),                   
                              (0,0,0,255))                                     
    textData = pygame.image.tostring(textSurface, "RGBA", True)                
    glRasterPos3d(*position)                                                
    glDrawPixels(textSurface.get_width(), textSurface.get_height(),         
                    GL_RGBA, GL_UNSIGNED_BYTE, textData)


class Texture(object):
# simple texture class
# designed for 32 bit png images (with alpha channel)
    def __init__(self,fileName):
        self.texid=0
        self.LoadTexture(fileName)
    def LoadTexture(self,fileName):
        textureSurface = pygame.image.load(fileName)
        textureData = pygame.image.tostring(textureSurface, "RGBA", 0)

        self.texid=glGenTextures(1)

        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texid)
        glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR)
        
        glTexImage2D( GL_TEXTURE_2D, 0, GL_RGBA,
                    textureSurface.get_width(), textureSurface.get_height(),
                    0, GL_RGBA, GL_UNSIGNED_BYTE, textureData )
        glDisable(GL_TEXTURE_2D)

    def __del__(self):
        glDeleteTextures(self.texid)


class Camera(object):

    def __init__(self):
        self.pos = [0,0,0]
        self.rot = [0,0,0]
        
        

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
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

    def startup(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.WIDTH,self.HEIGHT), DOUBLEBUF|OPENGL)
        pygame.display.set_caption('OpenGL window')
        #glutInit()
        glClearColor(0.5,0.7,1, 1.0)

        glEnable(GL_DEPTH_TEST) 

        self.piste = Texture('piste2.png')
    
    def draw(self):
        """glBegin(GL_QUADS)
        i = 0
        for face in faces:
            glColor3fv(colours[i])
            for vertex in face:
                glVertex3fv(vertices[vertex])
            i += 1
        glEnd()"""

        #sol
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D,self.piste.texid)
        glBegin(GL_QUADS)
        glColor3fv((1,1,1))
        for i, vertex in enumerate(terrain):
            glTexCoord2f(*terraintex[i])
            glVertex3fv(vertex)
    
        glEnd()
        glDisable(GL_TEXTURE_2D)

    def __init__(self):
        self.running = True
        self.lock = True
        self.speed = 0
        self.capture = False
        self.startup()
        self.camera = Camera()

    def update_camera(self):
        rot = self.camera.rot
        glRotatef(-rot[0],1,0,0)
        glRotatef(-rot[1],0,1,0)
        x,y,z = self.camera.pos
        glTranslatef(-x,-y,-z)
    
    def run(self):
        while self.running:
            self.clock.tick(60)

            self.checkForInput()
            self.move()
            #debut nouvelle frame 
            self.view3d()
            glPushMatrix()
            self.update_camera()
            #drawText(5,5,'testfklsfklskflskflsdfksdlfkdslfklsm')
            self.draw()
            glPopMatrix()
            pygame.display.flip()
            if self.capture:
                imagebuffer.mode = 'RGBA'
                imagebuffer.width = self.WIDTH
                imagebuffer.height = self.HEIGHT
                imagebuffer.data = pygame.image.tostring(self.screen, imagebuffer.mode, False)

    def move(self):
        yaw = math.radians(-self.camera.rot[1])

        if self.speed != 0:
            dx,dz = self.speed*math.sin(yaw), self.speed*math.cos(yaw)
            self.camera.pos[0] += dx
            self.camera.pos[2] -= dz


    def checkForInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    self.lock = False
                if event.key == K_UP:
                    self.speed += .1
                if event.key == K_DOWN:
                    self.speed -= .1
                if event.key == K_SPACE:
                    self.speed = 0
                if event.key == K_p:
                    self.capture = not self.capture
                    print 'capture:', self.capture
        #process pressed keys
        pressed = pygame.key.get_pressed()

        if pressed[K_LEFT]:
            self.camera.rot[1] += 1

        if pressed[K_RIGHT]:
            self.camera.rot[1] -= 1

if __name__ == '__main__':
    HOST, PORT = "localhost", 8000
    server = BaseHTTPServer.HTTPServer((HOST, PORT), httpserver.RequestHandler)
    # Start a thread with the server -- that thread will then start one
    # more thread for each request
    server_thread = threading.Thread(target=server.serve_forever)
    # Exit the server thread when the main thread terminates
    server_thread.daemon = True
    server_thread.start()

    view = Main()
    view.run()

    #close http server
    server.shutdown()
    server.server_close()
    quit()