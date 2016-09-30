from OpenGL.GL import *
from OpenGL.GLU import *
import math
from math import pi, cos, sin

from Texture import Texture
from Car import Car

class Track(object):
    """La piste fait 10.3m (ligne droite) par 6.6m
    la texture representant la piste fait 1024*1024, il faut donc que la surface
    texturee soit un carre. dans l image de texture 10.3m=752px. Il faut donc que la
    surface fasse 10.3 * 1024/752
    """
    L1 = 10.3 * 1024/752.
    L2 = L1
    H = -Car.hauteurcamera
    terrain = ((-L1/2.,-L2/2.,H),(L1/2.,-L2/2.,H),(L1/2.,L2/2.,H),(-L1/2.,L2/2.,H))
    terrain = ((-10,-10,H),(10,-10,H),(10,10,H),(-10,10,H))
    terraintex = ((0.0, 0.0),(1.0, 0.0),(1.0, 1.0),(0.0, 1.0))

    RED   = (1,0,0)
    BLUE  = (0,0,1)
    GREEN = (0,1,0)
    LANE_WIDTH = 0.3
    NB_LANE = 6
    LANE_COLOR = [GREEN, BLUE, GREEN, RED, BLUE, RED]

    def __init__(self):
        self.texture = Texture('piste2.png')
        self.quadric = {}
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
    
    def draw(self, viewname):
        if not self.quadric.get(viewname,None):
            self.quadric[viewname] = []
            #create one quadric by turn by view
            for elt in self.trackelt:
                if elt['type'] == 'turn':
                    quad = gluNewQuadric()
                    gluQuadricDrawStyle(quad, GLU_FILL)
                    self.quadric[viewname].append(quad)
                else:
                    self.quadric[viewname].append(None)

        for lane in range(self.NB_LANE):
            current_angle = -pi
            offsetlane = self.LANE_WIDTH*lane
            x,y = 0,-offsetlane
            for i, elt in enumerate(self.trackelt):
                #print 'x,y,angle',x,y,math.degrees(current_angle)
                glPushMatrix()
                glColor3fv(self.LANE_COLOR[lane])
                if elt['type'] == 'turn':
                    if elt['sweep'] > 0:
                        angle = math.degrees(-current_angle)
                        sweep = math.degrees(elt['sweep'])
                        inside_r = elt['L'] / elt['sweep'] + offsetlane
                        outside_r = inside_r + self.LANE_WIDTH
                        dx = inside_r*cos(current_angle+pi/2.)
                        dy = inside_r*sin(current_angle+pi/2.)
                        glTranslatef(x-dx,y-dy,-Car.hauteurcamera)
                        gluPartialDisk(self.quadric[viewname][i],inside_r,outside_r,32,32,angle,sweep)
                        # on calcule le changement de coordonnee pour un point a qui tourne de sweep a partir de current angle
                        # les coordonnees ont pour origine le centre du cercle de rotation
                        sweep = elt['sweep']
                        xa = dx
                        ya = dy
                        xb = xa*cos(sweep) + ya*sin(sweep)
                        yb = -xa*sin(sweep) + ya*cos(sweep)
                        # on ajoute le deplacement par rapport au coordonnee initiale en corrigeant par rapport au centre du cercle de rotation
                        x = x + (xb-xa)
                        y = y + (yb-ya)
                        current_angle -= elt['sweep']
                    else:
                        sweep = abs(math.degrees(elt['sweep']))
                        angle = math.degrees(-current_angle + pi/2.)
                        outside_r = elt['L'] / abs(elt['sweep']) - offsetlane
                        inside_r = outside_r - self.LANE_WIDTH
                        dx = outside_r*cos(current_angle-pi/2.)
                        dy = outside_r*sin(current_angle-pi/2.)
                        glTranslatef(x-dx,y-dy,-Car.hauteurcamera)
                        gluPartialDisk(self.quadric[viewname][i],inside_r,outside_r,32,32,angle,sweep)
                        # on calcule le changement de coordonnee pour un point a qui tourne de sweep a partir de current angle
                        # les coordonnees ont pour origine le centre du cercle de rotation
                        sweep = elt['sweep']
                        xa = dx
                        ya = dy
                        xb = xa*cos(sweep) + ya*sin(sweep)
                        yb = -xa*sin(sweep) + ya*cos(sweep)
                        # on ajoute le deplacement par rapport au coordonnee initiale en corrigeant par rapport au centre du cercle de rotation
                        x = x + (xb-xa)
                        y = y + (yb-ya)
                        current_angle -= elt['sweep']
                else:
                    angle = math.degrees(current_angle)
                    glTranslatef(x,y,-Car.hauteurcamera)
                    glRotatef(angle,0,0,1)
                    glScalef(elt['L'], self.LANE_WIDTH, 0)
                    self.drawrect()
                    x += elt['L']*cos(current_angle)
                    y += elt['L']*sin(current_angle)
                glPopMatrix()