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
        gluLookAt(x,y,z,x+math.cos(rot[2]),y+math.sin(rot[2]),z,0,0,1)