import wx
import sys
import math

from OpenGL.GL import *
from OpenGL.GLU import *
from wx import glcanvas
from SceneGLCanvas import SceneGLCanvas

class CarView(wx.Panel):
    def __init__(self, parent, carlist, carnumber, **kwargs):
        wx.Panel.__init__(self, parent, -1, **kwargs)
        name = 'carview '+str(carnumber)
        self.name = name
        self.car = carlist[carnumber]
        self.glcanvas = CarGLCanvas(self, name, carlist, carnumber, size=(400, 200))
        self.title = wx.TextCtrl(self, value='\n\n', style=wx.TE_READONLY|wx.TE_MULTILINE|wx.TE_NO_VSCROLL)
        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(self.title,0 , wx.EXPAND)
        box.Add(self.glcanvas)
        self.SetSizer(box)
        box.Fit(self)

        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def OnPaint(self, event=None):
        dc = wx.PaintDC(self)
        title = '%s - motor left:%.02f, right:%.02f' % (self.name, self.car.leftspeed, self.car.rightspeed)
        title += '\n'
        title += 'lap count: %d, last: %s\nbest: %s, worst: %s' % (self.car.laps['count'],
                                                                                  self.car.laps['last'] or '-',
                                                                                  self.car.laps['best'] or '-',
                                                                                  self.car.laps['worst'] or '-')
        self.title.SetValue(title)


class CarGLCanvas(SceneGLCanvas):
    def __init__(self, parent, name, carlist, carnumber, **kwargs):
        SceneGLCanvas.__init__(self, parent, name, carlist, **kwargs)
        self.carnumber = carnumber
        self.car = self.carlist[self.carnumber]
        print self.name, 'car is', self.car

    def setpointofview(self):
        #print 'setpointofview', self.name, '-',self.car.pos, self.car.rot
        rot = self.car.rot
        x,y,z = self.car.pos
        #camera point of view
        gluLookAt(x+0.12*math.cos(rot[2]),y+0.12*math.sin(rot[2]),z,x+math.cos(rot[2]),y+math.sin(rot[2]),z,0,0,1)

    def CaptureView(self):
        if self.car.cameraimg.capture:   
            size = self.GetClientSize()
            glPixelStorei(GL_PACK_ALIGNMENT, 1)
            data = glReadPixels(0, 0, size.width, size.height, GL_RGB, GL_UNSIGNED_BYTE, outputType=None)
            self.car.cameraimg.mode = 'RGB'
            self.car.cameraimg.width = size.width
            self.car.cameraimg.height = size.height
            self.car.cameraimg.data = data
            self.car.cameraimg.capture = False