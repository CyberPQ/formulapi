import wx
import sys

from OpenGL.GL import *
from OpenGL.GLU import *
from wx import glcanvas
from SceneGLCanvas import SceneGLCanvas
from OpenGL.GLU import *
from Track import Track


class TrackView(wx.Panel):
    def __init__(self, parent, carlist, **kwargs):
        wx.Panel.__init__(self, parent, -1, **kwargs)
        name = 'trackview'
        self.glcanvas = TrackGLCanvas(self, name, carlist, size=(400, 200))
        self.title = wx.TextCtrl(self, value=name, style=wx.TE_READONLY)
        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(self.title)
        box.Add(self.glcanvas)
        self.SetSizer(box)
        box.Fit(self)



class TrackGLCanvas(SceneGLCanvas):
    def __init__(self, parent, name, carlist, **kwargs):
        SceneGLCanvas.__init__(self, parent, name, carlist, **kwargs)
    
    def setpointofview(self):
        #5 au dessus du centre
        gluLookAt(-3,1.5,5,-3,1.5,0,0,1,0)
