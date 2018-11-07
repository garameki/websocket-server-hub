#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

import threading

import logging

from websocket_server import WebsocketServer
from time import sleep
from datetime import datetime

import socket

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(('raspberrypi.garameki.com',8801))
s.send('ma6'.encode('UTF-8'))
print(s.recv(1024))
s.send('ma6'.encode('UTF-8'))
print(s.recv(1024))
s.send('ma6'.encode('UTF-8'))
print(s.recv(1024))
print(s.recv(1024))
print(s.recv(1024))
print(s.recv(1024))
print(s.recv(1024))
print(s.recv(1024))
print(s.recv(1024))
print(s.recv(1024))
print(s.recv(1024))
print(s.recv(1024))
print(s.recv(1024))
s.close()
