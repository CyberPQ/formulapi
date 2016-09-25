from OpenGL.GL import *
from OpenGL.GLU import *

from Texture import Texture
from Robot import Robot

class Track(object):
    #10.3m par 6.6
    L1 = 10.3
    L2 = 6.6
    H = -Robot.hauteurcamera
    terrain = ((-L1/2.,L2/2.,H),(-L1/2.,-L2/2.,H),(L1/2.,-L2/2.,H),(L1/2.,L2/2.,H))
    terraintex = ((0.0, 0.0),(1.0, 0.0),(1.0, 1.0),(0.0, 1.0))

    def __init__(self):
        self.texture = Texture('piste2.png')

    def draw(self):
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