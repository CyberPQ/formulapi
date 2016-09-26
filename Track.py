from OpenGL.GL import *
from OpenGL.GLU import *

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
