import wx
import sys
import math

from OpenGL.GL import *
from OpenGL.GLU import *
from wx import glcanvas
from SceneView import SceneView
from OpenGL.GLU import *

class CarView(SceneView):
    def __init__(self, parent, car):
        self.name = 'carview'
        SceneView.__init__(self, parent, car)

    def setpointofview(self):
        rot = self.car.rot
        x,y,z = self.car.pos
        #camera point of view
        gluLookAt(x,y,z,x-math.sin(rot[1]),y,z-math.cos(rot[1]),0,1,0)