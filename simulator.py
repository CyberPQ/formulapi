import wx
import sys

# This working example of the use of OpenGL in the wxPython context
# was assembled in August 2012 from the GLCanvas.py file found in
# the wxPython docs-demo package, plus components of that package's
# run-time environment.

# Note that dragging the mouse rotates the view of the 3D cube or cone.

try:
    from wx import glcanvas
    haveGLCanvas = True
except ImportError:
    haveGLCanvas = False

try:
    # The Python OpenGL package can be found at
    # http://PyOpenGL.sourceforge.net/
    from OpenGL.GL import *
    from OpenGL.GLUT import *
    haveOpenGL = True
except ImportError:
    haveOpenGL = False

import numpy
import math
import time
import sys
import threading
import SocketServer
import time

from carlist import listcar
from CarView import CarView
from TrackView import TrackView
import httpserver
#----------------------------------------------------------------------

mycar = listcar[0]

class MainPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)

        self.oldtime = time.time()
        self.viewbox = wx.WrapSizer()
        #self.viewbox.Add((20, 30))
        #car views
        global listcar
        for i, car in enumerate(listcar):
            c = CarView(self, listcar, i)
            c.SetMinSize((600, 400))
            #c.Refresh()
            self.viewbox.Add(c, 0, wx.ALL, 1)

        #track view
        c = TrackView(self, listcar)
        c.SetMinSize((600, 400))
        self.viewbox.Add(c, 0, wx.ALL, 1)

        self.SetAutoLayout(True)
        self.SetSizer(self.viewbox)

        #refresh and animation timer
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)
        self.timer.Start(1/60.)

    def OnTimer(self, event):
        current = time.time()
        dt = current - self.oldtime
        self.oldtime = current
        global listcar
        for car in listcar:        
            car.move(dt)
        self.Refresh()

#----------------------------------------------------------------------
class Simulator(wx.App):
    def __init__(self):
        wx.App.__init__(self, redirect=False)

    def OnInit(self):
        frame = wx.Frame(None, -1, "Simulator: ", pos=(0,0),
                        style=wx.DEFAULT_FRAME_STYLE, name="run a sample")
        #frame.CreateStatusBar()

        menuBar = wx.MenuBar()
        menu = wx.Menu()
        item = menu.Append(wx.ID_EXIT, "E&xit\tCtrl-Q", "Exit demo")
        self.Bind(wx.EVT_MENU, self.OnExitApp, item)
        menuBar.Append(menu, "&File")
        
        frame.SetMenuBar(menuBar)
        frame.Show(True)
        frame.Bind(wx.EVT_CLOSE, self.OnCloseFrame)
        
        frame.Bind(wx.EVT_CHAR_HOOK, self.OnKey)
        self.mainwin = MainPanel(frame)

        # set the frame to a good size for showing the two buttons
        frame.SetSize((600*2,400*2))
        self.mainwin.SetFocus()
        self.window = self.mainwin
        frect = frame.GetRect()

        self.SetTopWindow(frame)
        self.frame = frame
        return True
        
    def OnExitApp(self, evt):
        self.frame.Close(True)

    def OnCloseFrame(self, evt):
        if hasattr(self, "window") and hasattr(self.window, "ShutdownDemo"):
            self.window.ShutdownDemo()
        evt.Skip()

    def OnKey(self, evt):
        key = evt.GetKeyCode()
        if key == wx.WXK_UP:
            mycar.add_speed(.4, .4)
        elif key == wx.WXK_DOWN:
            mycar.add_speed(-.4, -.4)
        elif key == wx.WXK_SPACE:
            mycar.set_speed(.0, .0)
        elif key == ord('T'):
            print datetime.datetime.now()
        elif key == ord('A'):
            global mycar
            mycar = listcar[0]
        elif key == ord('B'):
            global mycar
            mycar = listcar[1]
        elif key == wx.WXK_LEFT:
            mycar.add_speed(-.1,.1)
        elif key == wx.WXK_RIGHT:
            mycar.add_speed(.1,-.1)
        else:
            evt.Skip()

if __name__ == '__main__':
    HOST, PORT = "localhost", 8000
    #server = BaseHTTPServer.HTTPServer((HOST, PORT), httpserver.RequestHandler)
    server = SocketServer.TCPServer((HOST, PORT), httpserver.MyTCPHandler)
    # Start a thread with the server -- that thread will then start one
    # more thread for each request
    server_thread = threading.Thread(target=server.serve_forever)
    # Exit the server thread when the main thread terminates
    server_thread.daemon = True
    server_thread.start()

    app = Simulator()
    app.MainLoop()

    #close http server
    server.shutdown()
    server.server_close()
    quit()


