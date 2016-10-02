from OpenGL.GL import *
from OpenGL.GLU import *
import numpy
import math
from math import pi, cos, sin, pow

from Texture import Texture


class Track(object):
    """La piste fait 10.3m (ligne droite) par 6.6m
    la texture representant la piste fait 1024*1024, il faut donc que la surface
    texturee soit un carre. dans l image de texture 10.3m=752px. Il faut donc que la
    surface fasse 10.3 * 1024/752
    """
    L1 = 10.3 * 1024/752.
    L2 = L1
    H = 0
    terrain = ((-L1/2.,-L2/2.,H),(L1/2.,-L2/2.,H),(L1/2.,L2/2.,H),(-L1/2.,L2/2.,H))
    terrain = ((-10,-10,H),(10,-10,H),(10,10,H),(-10,10,H))
    terraintex = ((0.0, 0.0),(1.0, 0.0),(1.0, 1.0),(0.0, 1.0))

    RED   = (157/255.,68/255.,72/255.)
    GREEN = (73/255.,131/255.,81/255.)
    BLUE  = (66/255.,87/255.,117/255.)
    LANE_WIDTH = 0.3
    NB_LANE = 6
    LANE_COLOR = [GREEN, BLUE, GREEN, RED, BLUE, RED]
    START_LINE = [(0,0.5), (0,-NB_LANE*LANE_WIDTH -0.5)]

    def __init__(self):
        self.texture = Texture('resources/piste2.png')
        self.tracklist= {}
        self.trackelt=[
            {'type':'straight', 'L':5.4},
            {'type':'turn', 'L':0.7, 'sweep':math.radians(135)},
            {'type':'straight', 'L':2},
            {'type':'turn', 'L':0.5, 'sweep':math.radians(78.65)},
            {'type':'turn', 'L':4.5, 'sweep':-math.radians(90)},
            {'type':'turn', 'L':0.8, 'sweep':math.radians(146.35)},
            {'type':'straight', 'L':1.7},
            {'type':'turn', 'L':1.4, 'sweep':math.radians(90)}
        ]

    @staticmethod
    def bezier(t, p0, p1, p2, p3):
        # Cubic bezier Curve
        point = (pow((1-t), 3.0) * P0) + (3 * pow((1-t),2) * t * P1) + (3 * (1-t) * t * t * P2) + (pow(t, 3) * P3)
        return point
    
    def olddraw(self):
        #sol
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D,self.texture.texid)
        glBegin(GL_QUADS)
        glColor3fv((1,1,1))
        for i, vertex in enumerate(self.terrain):
            glTexCoord2f(*self.terraintex[i])
            glVertex3fv(vertex)

        glEnd()
        glDisable(GL_TEXTURE_2D)
    
    def drawrect(self):
        glBegin(GL_QUADS)
        glVertex3f(0, 0, 0)
        glVertex3f(1, 0, 0)
        glVertex3f(1, 1, 0)
        glVertex3f(0, 1, 0)
        glEnd()

    def drawwall(self):
        glBegin(GL_QUADS)
        glVertex3f(0, 0, 0)
        glVertex3f(0, 0, 1)
        glVertex3f(1, 0, 1)
        glVertex3f(1, 0, 0)
        glEnd()

    def drawcurvedwall(self, radius, start, sweep, split=16):
        """ draw a curved surface a,b,c,d centre @ 0,0,0 """
        pas = sweep / float(split)
        old_b = 0
        glBegin(GL_QUADS)
        for i in range(split):
            b = (radius*sin(start + pas*(i+1)),radius*cos(start + pas*(i+1)),0)
            if i == 0:
                a = (radius*sin(start + pas*i),radius*cos(start + pas*i),0)
            else:
                a = old_b
            c = numpy.array(b,'f') + numpy.array((0,0,1),'f')
            d = numpy.array(a, 'f') + numpy.array((0,0,1), 'f')
            old_b = b
            for v in (a,b,c,d):
                glVertex3fv(v)
        glEnd()


    
    def draw(self, viewname):
        if not self.tracklist.get(viewname, None):
            self.tracklist[viewname] = self.create_tracklist()
        glCallList(self.tracklist[viewname])

    def create_tracklist(self):
        gllist = glGenLists(1)
        glNewList(gllist, GL_COMPILE)
        for lane in range(self.NB_LANE):
            current_angle = -pi
            offsetlane = self.LANE_WIDTH*lane
            x,y = 0,-offsetlane
            for i, elt in enumerate(self.trackelt):
                if elt['type'] == 'turn':
                    quad = gluNewQuadric()
                    gluQuadricDrawStyle(quad, GLU_FILL)
                    if elt['sweep'] > 0:
                        angle = math.degrees(-current_angle)
                        sweep = math.degrees(elt['sweep'])
                        inside_r = elt['L'] / elt['sweep'] + offsetlane
                        outside_r = inside_r + self.LANE_WIDTH
                        dx = inside_r*cos(current_angle+pi/2.)
                        dy = inside_r*sin(current_angle+pi/2.)
                        glPushMatrix()
                        try:
                            glColor3fv(self.LANE_COLOR[lane])
                            glTranslatef(x-dx,y-dy,0)
                            gluPartialDisk(quad,inside_r,outside_r,32,32,angle,sweep)
                        finally:
                            glPopMatrix()
                        # draw wall
                        if lane == 0 or lane == self.NB_LANE-1:
                            glPushMatrix()
                            try:
                                glColor3fv((0,0,0))
                                if lane == 0:  
                                    glTranslatef(x-dx,y-dy,0)
                                    r = inside_r
                                else:
                                    glTranslatef(x-dx,y-dy,0)
                                    r = outside_r
                                glScalef(1, 1, 0.2)
                                self.drawcurvedwall(r, -current_angle, elt['sweep'])
                            finally:
                                glPopMatrix()
                    else:
                        sweep = abs(math.degrees(elt['sweep']))
                        angle = math.degrees(-current_angle + pi/2.)
                        outside_r = elt['L'] / abs(elt['sweep']) - offsetlane
                        inside_r = outside_r - self.LANE_WIDTH
                        dx = outside_r*cos(current_angle-pi/2.)
                        dy = outside_r*sin(current_angle-pi/2.)
                        glPushMatrix()
                        try:
                            glColor3fv(self.LANE_COLOR[lane])
                            glTranslatef(x-dx,y-dy,0)
                            gluPartialDisk(quad,inside_r,outside_r,32,32,angle,sweep)
                        finally:
                            glPopMatrix()
                        # draw wall
                        if lane == 0 or lane == self.NB_LANE-1:
                            glPushMatrix()
                            try:
                                glColor3fv((0,0,0))
                                dxx = dx - self.LANE_WIDTH*cos(current_angle-pi/2.)
                                dyy = dy - self.LANE_WIDTH*sin(current_angle-pi/2.)
                                if lane == 0:  
                                    glTranslatef(x-dx,y-dy,0)
                                    r = inside_r + self.LANE_WIDTH
                                else:
                                    glTranslatef(x-dx,y-dy,0)
                                    r = outside_r - self.LANE_WIDTH
                                glScalef(1, 1, 0.2)
                                self.drawcurvedwall(r, -current_angle + pi/2., abs(elt['sweep']))
                            finally:
                                glPopMatrix()

                    #update coords
                    # on calcule le changement de coordonnee pour un point a qui tourne de sweep a partir de current angle
                    # les coordonnees ont pour origine le centre du cercle de rotation
                    sweep = elt['sweep']
                    xa = dx
                    ya = dy
                    xb = xa*cos(sweep) + ya*sin(sweep)
                    yb = -xa*sin(sweep) + ya*cos(sweep)
                    x += (xb-xa)
                    y += (yb-ya)
                    current_angle -= sweep
                else:
                    angle = math.degrees(current_angle)
                    # draw wall
                    if lane == 0 or lane == self.NB_LANE-1:
                        glPushMatrix()
                        try:
                            glColor3fv((0,0,0))
                            if lane == 0:  
                                glTranslatef(x,y,0)
                            else:
                                glTranslatef(x+self.LANE_WIDTH*cos(current_angle+pi/2.),
                                             y+self.LANE_WIDTH*sin(current_angle+pi/2.),
                                             0)
                            glRotatef(angle,0,0,1)
                            glScalef(elt['L'], 1, 0.2)
                            self.drawwall()
                        finally:
                            glPopMatrix()
                    
                    # draw rectangle
                    glPushMatrix()
                    try:
                        glColor3fv(self.LANE_COLOR[lane])
                        glTranslatef(x,y,0)
                        glRotatef(angle,0,0,1)
                        glScalef(elt['L'], self.LANE_WIDTH, 1)
                        self.drawrect()
                    finally:    
                        glPopMatrix()
                    # update coords
                    x += elt['L']*cos(current_angle)
                    y += elt['L']*sin(current_angle)
        glEndList()
        return gllist