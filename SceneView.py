import wx
import sys

from OpenGL.GL import *
from OpenGL.GLU import *
from wx import glcanvas
from Track import Track

class SceneView(glcanvas.GLCanvas):
    def __init__(self, parent, car):
        glcanvas.GLCanvas.__init__(self, parent, -1)
        self.init = False
        self.ispovinit = False
        self.car = car
        self.context = glcanvas.GLContext(self)
        self.size = self.GetClientSize()
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        
        print self.name, 'fin init'

    def InitGL(self):
        size = self.GetClientSize()
        print self.name, 'initGL', size
        
        glClearColor(0.5,0.7,1, 1.0)
        self.track = Track()
        self.initpov()

    def initpov(self):
        size = self.GetClientSize()
        print self.name, 'init pov', size
        glShadeModel(GL_SMOOTH)
        glEnable(GL_DEPTH_TEST)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(70,(size.width/size.height),0.001,100)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        self.ispovinit = True

    def OnEraseBackground(self, event):
        pass # Do nothing, to avoid flashing on MSW.

    def OnSize(self, event):
        self.ispovinit = False
        event.Skip()
        
    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        self.SetCurrent(self.context)
        if not self.init:
            self.InitGL()
            self.init = True
        if not self.ispovinit:
            self.initpov()
        self.OnDraw()

    def OnDraw(self):
        #print self.name, 'draw'
        # clear color and depth buffers
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glPushMatrix()
        #set point of view
        self.setpointofview()
        #draw Car
        self.car.draw()
        #draw track
        self.track.draw()
        glPopMatrix()
        
        self.SwapBuffers()
    
    def setpointofview(self):
        raise NotImplementedError()