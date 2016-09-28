"""Simple HTTP Server.

This module builds on BaseHTTPServer by implementing the standard GET
and HEAD requests in a fairly straightforward manner.
http://www.acmesystems.it/python_httpd

"""

import os
import posixpath
import BaseHTTPServer
import urllib
from urlparse import urlparse, parse_qs
import cgi
import sys
import shutil
import mimetypes
from PIL import Image
import datetime
import time

from carlist import listcar

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO


import SocketServer

class MyTCPHandler(SocketServer.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        while True:
            self.data = self.request.recv(1024).strip()
            command = self.data.split()
            if command[0] == 'capture':
                carnum = int(command[1])
                car = listcar[carnum]
                print datetime.datetime.now(),'start capture', carnum
                car.cameraimg.capture = True
                while car.cameraimg.capture:
                    time.sleep(0.01)
                # Send the html message
                img = Image.fromstring(car.cameraimg.mode, (car.cameraimg.width,car.cameraimg.height), car.cameraimg.data.tostring())
                img = img.transpose( Image.FLIP_TOP_BOTTOM)
                pseudofile = StringIO()
                print datetime.datetime.now(),'start png'
                img.save(pseudofile,'PNG')
                pseudofile.seek(0, os.SEEK_END)
                size = pseudofile.tell()
                #size = len(imagebuffer.data)
                # send image size
                self.request.sendall(str(size))
                # wait for image transfert
                self.data = self.request.recv(1024).strip()
                #send image
                self.request.sendall(pseudofile.getvalue())#imagebuffer.data)
                print datetime.datetime.now(),'fin capture'
            
            elif command[0] == 'motor':
                carnum = int(command[1])
                car = listcar[carnum]
                car.set_speed(float(command[2]), float(command[3]))


