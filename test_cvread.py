# import the necessary packages
import numpy as np
import urllib
import cv2
import time
import datetime
import socket,os

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("localhost", 8000))
k = ' '
size = 1024

while(1):
    k = '1'
    print "debut reception fichier:", datetime.datetime.now()
    client_socket.send(k)
    size = client_socket.recv(1024)
    size = int(size)
    print "The file size is - ",size," bytes"
    size = size*2
    client_socket.send('go')
    strng = client_socket.recv(size)
    print "fin reception fichier:", datetime.datetime.now()
