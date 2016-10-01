import numpy
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image

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
        color = (1.0, 0.0, 0.0, 1.0)
        glTexParameterfv(GL_TEXTURE_2D, GL_TEXTURE_BORDER_COLOR, color)
        
        glTexImage2D( GL_TEXTURE_2D, 0, GL_RGBA,
                    img.size[0], img.size[1],
                    0, GL_RGBA, GL_UNSIGNED_BYTE, imgdata )
        glDisable(GL_TEXTURE_2D)

    def __del__(self):
        glDeleteTextures(self.texid)
