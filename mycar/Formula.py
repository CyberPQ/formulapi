#!/usr/bin/python
# -*- coding: utf-8 -*-
import cv2
import numpy
import math
import logging
import socket

from ImageProcessor import ImageProcessor

class CarControl(object):
    def __init__(self, carnumber):
        self.client_socket = None
        self.latestimage = None
        self.carnumber = carnumber
        self.speed = 0
        self.logger = logging.getLogger('formulapi')
        self.imgprocess = ImageProcessor()

    def ConnectToSimulator(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(("localhost", 8000))
    
    def GetImage():
        if not client_socket:
            raise AssertionError('Must connect to simulator !!!')
        starttime = datetime.datetime.now()
        client_socket.send('capture %d' % self.carnumber)
        size = client_socket.recv(1024)
        size = int(size)
        client_socket.send('go')
        image = ''
        while len(image) != size:
            image += client_socket.recv(size)
        self.logger.debug('receive image : size', len(image))
        self.logger.debug("getimage duration:", datetime.datetime.now()-starttime)
        x = np.fromstring(image, dtype='uint8')
        self.lattestimage = cv2.imdecode(x, cv2.IMREAD_UNCHANGED)
        return self.latestimage

    def SetMotorSpeed(left, right):
        client_socket.send('motor %d %f %f' % (self.carnumber, left, right))

    def Start(self):
        self.ConnectToSimulator()
        #launch thread
        #TODO

    def Run(self):
        """
        get image
        process image
        control motor
        """
        raise NotImplementedError()
    
    def Stop(self):
        client_socket.close()
        
    def Speed(speed):
        self.speed = speed

    def TrackCurve():
        return self.imgprocess.trackcurve
    
    def CurrentTrackPosition():
        return self.imgprocess.trackoffset

    def TrackFound():
        if self.imgprocess.trackoffset is None:
            return False
        else:
            return True
    
    def CurrentAngle():
        return self.imgprocess.angle

    def GetLatestImage():
        return self.lastestimage