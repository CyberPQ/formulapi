import numpy
import math
import time
import sys
import threading
import SocketServer
import httpserver
import imagebuffer
import datetime
from Robot import robot

from PIL import Image
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

#41.5mm
hauteurcamera = 0.0415
H = -hauteurcamera
#10.3m par 6.6
L1 = 10.3
L2 = 6.6
terrain = ((-L1/2.,H,L2/2.),(-L1/2.,H,-L2/2.),(L1/2.,H,-L2/2.),(L1/2.,H,L2/2.))
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

    def LoadTexture(self,filename):
        img = Image.open(filename)
        imgdata = numpy.array(list(img.getdata()), numpy.uint8)

        self.texid=glGenTextures(1)

        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texid)
        glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR)
        
        glTexImage2D( GL_TEXTURE_2D, 0, GL_RGBA,
                    img.size[0], img.size[1],
                    0, GL_RGBA, GL_UNSIGNED_BYTE, imgdata )
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

    def startup(self):
        glutInit()
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
        glutInitWindowSize(self.WIDTH, self.HEIGHT)
        glutCreateWindow("Formulapi Simulator")
        glClearColor(0.5,0.7,1, 1.0)

        glShadeModel(GL_SMOOTH)
        glEnable(GL_DEPTH_TEST)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(70,(self.WIDTH/self.HEIGHT),0.001,100)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        #fps timer
        self.setfps(60)
        glutKeyboardFunc(self.checkForInput)
        glutSpecialFunc(self.checkForInput)
        glutDisplayFunc(self.display)

    def setfps(self, fps):
        self.fps = fps
        glutTimerFunc(1000/fps, self.fpstimer, fps)

    def fpstimer(self, value):
        glutPostRedisplay()
        self.setfps(value)
    
    def draw(self):
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
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
        self.oldframetime = 0
        self.speed = 0
        self.capture = False
        self.startup()
        self.camera = Camera()
        self.piste = Texture('piste2.png')

    def update_camera(self):
        rot = self.camera.rot
        #print 'rotation:', rot[1]
        glRotatef(-rot[0],1,0,0)
        glRotatef(-rot[1],0,1,0)
        x,y,z = self.camera.pos
        glTranslatef(-x,-y,-z)
    
    def display(self):
        currenttime = glutGet(GLUT_ELAPSED_TIME) / 1000.0
        deltat = currenttime - self.oldframetime
        self.oldframetime = currenttime

        #self.checkForInput()
        self.move(deltat)
        glPushMatrix()
        self.update_camera()
        self.draw()
        glPopMatrix()
        glutSwapBuffers()
        if self.capture:
            width, height = self.WIDTH, self.HEIGHT
            glPixelStorei(GL_PACK_ALIGNMENT, 1)
            data = glReadPixels(0, 0, width, height, GL_RGB, GL_UNSIGNED_BYTE, outputType=None)
            imagebuffer.mode = 'RGB'
            imagebuffer.width = width
            imagebuffer.height = height
            imagebuffer.data = data

    def run(self):
        # infinite loop
        glutMainLoop()

    def move(self, dt):
        drot_radian, d = robot.get_deltarotation(dt)
        #ajustement rotation
        self.camera.rot[1] += math.degrees(drot_radian)
        if self.camera.rot[1] > 360.:
            self.camera.rot[1] -= 360.
        if self.camera.rot[1] < -360.:
            self.camera.rot[1] += 360.
        #calcul nouvelle coordonnee
        yaw = -math.radians(self.camera.rot[1])
        dx = d*math.sin(yaw)
        dz = d*math.cos(yaw)
        self.camera.pos[0] += dx
        self.camera.pos[2] -= dz


    def checkForInput(self, key, x, y):
        if key == GLUT_KEY_UP:
            robot.add_speed(.4, .4)
        if key == GLUT_KEY_DOWN:
            robot.add_speed(-.4, -.4)
        if key == ' ':
            robot.set_speed(.0, .0)
        if key == 't':
            print datetime.datetime.now()
        if key == 'p':
            self.capture = not self.capture
            print 'capture:', self.capture
        if key == GLUT_KEY_LEFT:
            robot.add_speed(-.1,.1)
        if key == GLUT_KEY_RIGHT:
            robot.add_speed(.1,-.1)


        

if __name__ == '__main__':
    HOST, PORT = "localhost", 8000
    #server = BaseHTTPServer.HTTPServer((HOST, PORT), httpserver.RequestHandler)
    server = SocketServer.TCPServer((HOST, PORT), httpserver.MyTCPHandler)
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