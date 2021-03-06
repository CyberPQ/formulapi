import wx
import sys

from OpenGL.GL import *
from OpenGL.GLU import *
from wx import glcanvas
from wx.glcanvas import WX_GL_DEPTH_SIZE
from wx.glcanvas import WX_GL_DOUBLEBUFFER
from wx.glcanvas import WX_GL_SAMPLE_BUFFERS
from wx.glcanvas import WX_GL_RGBA

from Track import Track


class SceneGLCanvas(glcanvas.GLCanvas):
    def __init__(self, parent, name, carlist, **kwargs):
        attribs=[WX_GL_RGBA,WX_GL_DOUBLEBUFFER,WX_GL_SAMPLE_BUFFERS, GL_TRUE,WX_GL_DEPTH_SIZE,16,0,0]
        glcanvas.GLCanvas.__init__(self, parent, -1, attribList=attribs, **kwargs)
        self.init = False
        self.ispovinit = False
        self.name = name
        self.carlist = carlist
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
        glShadeModel(GL_SMOOTH)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_MULTISAMPLE)
        self.track = Track()
        self.initpov()

    def initpov(self):
        size = self.GetClientSize()
        print self.name, 'init pov', size
        size.height = size.height or 1
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(70,float(size.width)/float(size.height),0.001,100)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        self.ispovinit = True

    def OnEraseBackground(self, event):
        pass # Do nothing, to avoid flashing on MSW.

    def OnSize(self, event):
        self.SetCurrent(self.context)
        size = self.GetClientSize()
        glViewport(0,0,size.width, size.height)
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
        self.CaptureView()

    def OnDraw(self):
        # clear color and depth buffers
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        #set point of view
        self.setpointofview()
        #draw Cars
        #print self.name,'draw car'
        for car in self.carlist:
            car.draw(self.name)
        #draw track
        self.track.draw(self.name)
        
        self.SwapBuffers()
    
    def setpointofview(self):
        raise NotImplementedError()

    def CaptureView(self):
        pass