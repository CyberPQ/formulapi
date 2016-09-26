import wx
import sys
import math

from OpenGL.GL import *
from OpenGL.GLU import *
from wx import glcanvas
from SceneView import SceneView


class CarView(SceneView):
    def __init__(self, parent, carlist, carnumber):
        name = 'carview '+str(carnumber)
        SceneView.__init__(self, parent, name, carlist)
        self.carnumber = carnumber
        self.car = self.carlist[self.carnumber]

    def setpointofview(self):
        rot = self.car.rot
        x,y,z = self.car.pos
        #camera point of view
        gluLookAt(x,y,z,x+math.cos(rot[2]),y+math.sin(rot[2]),z,0,0,1)

    def CaptureView(self):
        size = self.GetClientSize()
        glPixelStorei(GL_PACK_ALIGNMENT, 1)
        data = glReadPixels(0, 0, size.width, size.height, GL_RGB, GL_UNSIGNED_BYTE, outputType=None)
        self.car.cameraimg.mode = 'RGB'
        self.car.cameraimg.width = size.width
        self.car.cameraimg.height = size.height
        self.car.cameraimg.data = data