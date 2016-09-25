from threading import RLock
import math
from OpenGL.GL import *
from OpenGL.GLU import *


class Robot(object):
    #159mm
    ENTRAXE = 0.159
    #chassis + demi-roue
    LONGUEUR = 0.105 + 0.088
    LARGEUR = 0.18
    #41.5mm
    hauteurcamera = 0.0415

    def __init__(self):
        #lock to protect variable
        self.lock = RLock()
        #motor speed
        self.leftspeed = .0
        self.rightspeed = .0
        self.pos = [0,0,0]
        self.rot = [0,0,0]


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
        self.rot[1] += drot_radian
        if self.rot[1] > 2* math.pi:
            self.rot[1] -= 2 * math.pi
        if self.rot[1] < -2 * math.pi:
            self.rot[1] += 2 * math.pi
        #calcul nouvelle coordonnee
        yaw = -self.rot[1]
        dx = d*math.sin(yaw)
        dz = d*math.cos(yaw)
        self.pos[0] += dx
        self.pos[2] -= dz

    def draw(self):
        x = self.pos[0]
        y = self.pos[1]
        z = self.pos[2]
        angle = self.rot[1]

        ax = x - self.LARGEUR/2.*math.sin(angle+math.pi/2.) - self.LONGUEUR/2.*math.sin(angle)
        az = z - self.LARGEUR/2.*math.cos(angle+math.pi/2.) - self.LONGUEUR/2.*math.cos(angle)
        bx = x - self.LARGEUR/2.*math.sin(angle-math.pi/2.) - self.LONGUEUR/2.*math.sin(angle)
        bz = z - self.LARGEUR/2.*math.cos(angle-math.pi/2.) - self.LONGUEUR/2.*math.cos(angle)
        cx = bx + self.LONGUEUR*math.sin(angle)
        cz = bz + self.LONGUEUR*math.cos(angle)
        dx = ax + self.LONGUEUR*math.sin(angle)
        dz = az + self.LONGUEUR*math.cos(angle)
        points = [(ax,y,az),(bx,y,bz),(cx,y,cz),(dx,y,dz)]
        glBegin(GL_QUADS)
        #noir
        glColor3fv((0,0,0))
        for vertex in points:
            glVertex3fv(vertex)
        glEnd()

robot = Robot()