import wx
import sys

from OpenGL.GL import *
from OpenGL.GLU import *
from wx import glcanvas
from SceneView import SceneView
from OpenGL.GLU import *

class TrackView(SceneView):
    def __init__(self, parent, car):
        self.name = 'trackview'
        SceneView.__init__(self, parent, car)

    def initpov(self):
        size = self.GetClientSize()
        print self.name, 'init pov', size
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0.0, size.width, size.height, 0.0, 0., 10.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        self.ispovinit = True
    
    def setpointofview(self):
        #5 au dessus du centre
        #gluLookAt(0,4,0,0,0,0,1,0,0)
        pass