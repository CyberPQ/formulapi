from threading import RLock
import math
from OpenGL.GL import *
from OpenGL.GLU import *

import importobj

class CameraImage(object):
    def __init__(self):
        self.data = ''
        self.width = 0
        self.height = 0
        self.mode = 'RGB'
        self.capture = False

class Car(object):
    #159mm
    ENTRAXE = 0.159
    #chassis + demi-roue
    LONGUEUR = 0.105 + 0.088
    LARGEUR = 0.18
    #41.5mm
    hauteurcamera = 0.0415

    def __init__(self,num):
        #lock to protect variable
        self.lock = RLock()
        #motor speed
        self.leftspeed = .0
        self.rightspeed = .0
        self.pos = [0,0,0]
        self.rot = [0,0,0]
        self.cameraimg = CameraImage()
        self.carobj = None
        self.num = num


    def set_speed(self, left, right):
        with self.lock:
            self.leftspeed = left
            self.rightspeed = right

    def add_speed(self, left, right):
        with self.lock:
            self.leftspeed += left
            self.rightspeed += right

    def get_deltarotation(self, dt):
        with self.lock:
            deltaleft = self.leftspeed * dt
            deltaright = self.rightspeed * dt
            d = (deltaleft + deltaright) / 2.
            if deltaright == deltaleft:
                return 0., d
            rayon = (self.ENTRAXE * d) / (deltaright - deltaleft)
            deltarotation = (deltaright - deltaleft)/(self.ENTRAXE)
            #deltarotation = d / rayon
        return deltarotation, d

    def get_absspeed(self):
        with self.lock:
            speed = (self.leftspeed + self.rightspeed) / 2.
            #print 'speed',self.leftspeed, self.rightspeed
        return speed
    
    def move(self, dt):
        drot_radian, d = self.get_deltarotation(dt)
        #ajustement rotation
        self.rot[2] += drot_radian
        if self.rot[2] > 2* math.pi:
            self.rot[2] -= 2 * math.pi
        if self.rot[2] < -2 * math.pi:
            self.rot[2] += 2 * math.pi
        #calcul nouvelle coordonnee
        yaw = self.rot[2]
        dx = d*math.cos(yaw)
        dy = d*math.sin(yaw)
        self.pos[0] += dx
        self.pos[1] += dy

    def draw(self):
        #print 'car', self.num, '-',self.pos, self.rot,self
        if not self.carobj:
            self.carobj = importobj.OBJ('resources/car.obj')
        glPushMatrix()
        angle = self.rot[2]
        glTranslatef(self.pos[0], self.pos[1], 0.1)
        #glRotatef(math.degrees(self.rot[2]),0,0,1)
        #glRotatef(90.,0,0,1)
        glCallList(self.carobj.gl_list)
        glPopMatrix()
    
    def olddraw(self):
        x = self.pos[0]
        y = self.pos[1]
        z = self.pos[2]
        angle = self.rot[2]

        ax = x - self.LARGEUR/2.*math.cos(angle+math.pi/2.) - self.LONGUEUR/2.*math.cos(angle)
        ay = y - self.LARGEUR/2.*math.sin(angle+math.pi/2.) - self.LONGUEUR/2.*math.sin(angle)
        bx = x - self.LARGEUR/2.*math.cos(angle-math.pi/2.) - self.LONGUEUR/2.*math.cos(angle)
        by = y - self.LARGEUR/2.*math.sin(angle-math.pi/2.) - self.LONGUEUR/2.*math.sin(angle)
        cx = bx + self.LONGUEUR*math.cos(angle)
        cy = by + self.LONGUEUR*math.sin(angle)
        dx = ax + self.LONGUEUR*math.cos(angle)
        dy = ay + self.LONGUEUR*math.sin(angle)
        points = [(ax,ay,z),(bx,by,z),(cx,cy,z),(dx,dy,z)]
        glBegin(GL_QUADS)
        #blanc
        glColor3fv((1,1,1))
        for vertex in points:
            glVertex3fv(vertex)
        glEnd()
