# import the necessary packages
import numpy as np
import cv2
import time
import datetime
import socket,os


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("localhost", 8000))
k = ' '
size = 1024

while(1):
    print "debut reception fichier:", datetime.datetime.now()
    client_socket.send('capture 0')
    size = client_socket.recv(1024)
    size = int(size)
    print "The file size is - ",size," bytes"
    client_socket.send('go')
    image = ''
    while len(image) != size:
        image += client_socket.recv(size)
    print 'longueur recue:', len(image)
    print "fin reception fichier:", datetime.datetime.now()
    x = np.fromstring(image, dtype='uint8')
    image = cv2.imdecode(x, cv2.IMREAD_UNCHANGED)
    cv2.imshow('test 0', image)
    cv2.waitKey(100)
    client_socket.send('motor 0 0.1 0.1')
