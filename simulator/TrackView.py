import wx
import sys

from OpenGL.GL import *
from OpenGL.GLU import *
from wx import glcanvas
from SceneView import SceneView
from OpenGL.GLU import *
from Track import Track

class TrackView(SceneView):
    def __init__(self, parent, carlist):
        SceneView.__init__(self, parent, 'trackview', carlist)

    def _initpov(self):
        size = self.GetClientSize()
        print self.name, 'init pov', size
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-15, 15, -15, 15, -2, 1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        self.ispovinit = True
    
    def setpointofview(self):
        #5 au dessus du centre
        gluLookAt(-1,2,5,-1,2,0,0,1,0)
