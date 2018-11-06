#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

import threading

import logging

from websocket_server import WebsocketServer
from time import sleep
from datetime import datetime


#クライアントからのメッセージはサニタイズしてからしないと、send_message_allで多くのクライアントに迷惑を掛けてしまうことになります



def threaded_function():
	global server
	global clients
	global flagStopThread

	while not flagStopThread:
		for i in range(0,len(clients)):
			server.send_message(clients[i],datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
		sleep(1)

# Called for every client connecting (after handshake)
def new_client(client, server):
	global clients

	print("New client connected and was given id %d" % client['id'])
	server.send_message_to_all("Hey all, a new client has joined us")
	clients.append(client)

# Called for every client disconnecting
def client_left(client, server):
	print("Client(%d) disconnected" % client['id'])
	clients.remove(client)


# Called when a client sends a message
def message_received(client, server, message):
	if len(message) > 200:
		message = message[:200]+'..'
	print("Client(%d) said: %s" % (client['id'], message))

PORT=8801






HOST='raspberrypi.garameki.com'
LOGGING = logging.INFO
server = WebsocketServer(PORT,HOST,LOGGING)







server.set_fn_new_client(new_client)
server.set_fn_client_left(client_left)
server.set_fn_message_received(message_received)

clients = []

if __name__ == "__main__":
	
	flagStopThread = False
	thread = threading.Thread(target = threaded_function)
	thread.start()
	server.run_forever()
	flagStopThread = True	#Ctrl+Cで、serverが止まるとこの行に来る
	thread.join()		#スレッドを止める
