from threading import RLock
import math
import datetime
import numpy
from OpenGL.GL import *
from OpenGL.GLU import *

import importobj
from Track import Track

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
    hauteurcamera = 0.0415 #41.5mm

    def __init__(self,num):
        #lock to protect variable
        self.lock = RLock()
        #motor speed
        self.leftspeed = .0
        self.rightspeed = .0
        self.pos = [0,0,self.hauteurcamera]
        self.rot = [0,0,0]
        self.cameraimg = CameraImage()
        self.carobj = {}
        self.num = num
        self.laps ={'count':0, 'best':None, 'worst':None, 'last':None, 'lasttime':None}
        self.startime = datetime.datetime.now() #TODO mettre la bonne valeur


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
    
    def countlap(self, oldpos):
        """The problem reduces to this question: Do two lines from A to B and from C to D intersect?
        Then you can ask it four times (between the line and each of the four sides of the rectangle).

        Here's the vector math for doing it. I'm assuming the line from A to B is the line in question and the line from C to D is one of the rectangle lines.
        My notation is that Ax is the "x-coordinate of A" and Cy is the "y-coordinate of C." And "*" means dot-product, so e.g. A*B = Ax*Bx + Ay*By.

            E = B-A = ( Bx-Ax, By-Ay )
            F = D-C = ( Dx-Cx, Dy-Cy ) 
            P = ( -Ey, Ex )
            h = ( (A-C) * P ) / ( F * P )

        This h number is the key. If h is between 0 and 1, the lines intersect, otherwise they don't. If F*P is zero,
        of course you cannot make the calculation, but in this case the lines are parallel and therefore only intersect in the obvious cases.

        The exact point of intersection is C + F*h.
        """
        a = numpy.array(Track.START_LINE[0])
        b = numpy.array(Track.START_LINE[1])
        c = numpy.array((oldpos[0], oldpos[1]))
        d = numpy.array((self.pos[0], self.pos[1]))
        e = b-a
        f = d-c
        p = numpy.array((-e[1], e[0]))
        fdotp = numpy.dot(f,p)
        if fdotp != 0:
            h = numpy.dot(a-c, p) / fdotp
            i = c + h*f
            if h <= 1 and h >= 0 and b[0]<=i[0]<=a[0] and b[1]<=i[1]<=a[1] :
                #intersection, TODO: fix date with intersection point
                current_time = datetime.datetime.now()
                self.laps['count'] += 1
                #computation last time
                if self.laps['lasttime'] is None:
                    laptime = current_time - self.startime
                else:
                    laptime = current_time - self.laps['lasttime']
                self.laps['last'] = laptime
                self.laps['lasttime'] = current_time
                #compute best time
                if self.laps['best'] is None:
                    self.laps['best'] = laptime
                else:
                    if laptime < self.laps['best']:
                        self.laps['best'] = laptime
                #compute worst time
                if self.laps['worst'] is None:
                    self.laps['worst'] = laptime
                else:
                    if laptime > self.laps['worst']:
                        self.laps['worst'] = laptime
    
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
        oldpos = list(self.pos)
        self.pos[0] += dx
        self.pos[1] += dy
        self.countlap(oldpos)
        

    def draw(self, viewname):
        #print 'car', self.num, '-',self.pos, self.rot,self
        if not self.carobj.get(viewname, None):
            obj = importobj.OBJ('resources/car.obj')
            self.carobj[viewname] = obj
        glPushMatrix()
        angle = self.rot[2]
        glTranslatef(self.pos[0], self.pos[1], self.pos[2])
        glRotatef(math.degrees(angle),0,0,1)
        glRotatef(90.,0,0,1)
        glCallList(self.carobj[viewname].gl_list)
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
        
