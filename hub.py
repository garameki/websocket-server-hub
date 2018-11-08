#!/usr/bin/env python3:
# _*_ coding: utf-8 _*_

import logging
from websocket_server import WebsocketServer
import re	#regexp


class MyClient:

	allClients = []	#class variable : all client instans is allocated into 

	def __init__(self,client_websocket_server,server_websocket_server):
		self.pClient = client_websocket_server
		self.pServer = server_websocket_server
		self.pRoll = None
		MyClient.allClients.append(self)

	def speak_to_myself(self,message):
		self.pServer.send_message(self.pClient,message)

	def say_to_roll(self,roll,message):
		allclients = MyClient.allClients
		for ii in range(0,len(allclients)):
			if allclients[ii].pRoll == roll:
				self.pServer.send_message(allclients[ii].pClient,message)

	def say_to_all(self,message):
		self.pServer.send_message_to_all(message)

	def get_roll(self):
		return self.pRoll

	def set_roll(self,roll):
		self.pRoll = roll

	def set_roll_exclusively(self,roll):
		if self.pRoll == roll:
			self.pServer.send_message(self.pClient,"success : you have already been "+roll)
			return True
		elif MyClient.exist_roll(roll):
			self.pServer.send_message(self.pClient,"falure : "+roll+" already exists")
			return False
		else:
			self.set_roll(roll)
			self.pServer.send_message(self.pClient,"success : you became "+roll)
			return True

	@classmethod
	def get_rolls_of_all(cself):
		rolls = []
		for ii in range(0,len(MyClient.allClients)):
			rolls.append(MyClient.allClients[ii].pRoll)
		print('rolls =',rolls)
		return rolls

	@classmethod
	def exist_roll(cself,roll):
		allRolls = MyClient.get_rolls_of_all()
		if roll in allRolls:
			return True
		else:
			return False

	@classmethod
	def remove(cself,client_websocket_server):
		for ii in range(0,len(MyClient.allClients)):
			if MyClient.allClients[ii].pClient == client_websocket_server:
				del MyClient.allClients[ii]

	@classmethod
	def convertFrom(cself,client_websocket_server):
		ii=0
		for ii in range(0,len(MyClient.allClients)):
			if MyClient.allClients[ii].pClient == client_websocket_server:
				break
		return MyClient.allClients[ii]





class HubServer:

	ANONYMOUS = 'anonymous'
	rollnameMAX31856 = 'MAX31856'
	rollnameCONTROLLER = 'CONTROLLER'


	def __init__(self,PORT,HOST,LOGGING):
		server = WebsocketServer(PORT,HOST,LOGGING)
		server.set_fn_new_client(self.new_client)
		server.set_fn_client_left(self.client_left)
		server.set_fn_message_received(self.message_received)
		server.run_forever()

	# Called for every client connecting (after handshake)
	def new_client(self,client_websocket_server, server):
		print("New client connected and was given id %d" % client_websocket_server['id'])
		print(client_websocket_server)
		server.send_message_to_all('new client joined')
		MyClient(client_websocket_server,server)

	# Called for every client disconnecting
	def client_left(self,client, server):
		print("Client(%d) disconnected" % client['id'])
		MyClient.remove(client)


	# Called when a client sends a message
	def message_received(self,client_websocket_server, server, message):
		print('messge from ',client_websocket_server)
		print("Client({}) said: {}".format(client_websocket_server['id'], message))
		client = MyClient.convertFrom(client_websocket_server)

		if message.strip() == "co6":
			client.set_roll_exclusively(HubServer.rollnameCONTROLLER)
		elif message.strip() == "ma6":
			client.set_roll_exclusively(HubServer.rollnameMAX31856)

		roll = client.get_roll()
		if roll == HubServer.rollnameCONTROLLER:
			if re.search('toM',message):#pass phrase
				client.say_to_roll(HubServer.rollnameMAX31856,message)
		elif roll == HubServer.rollnameMAX31856:
			if re.search('toC',message):#pass phrase
				client.say_to_roll(HubServer.rollnameCONTROLLER,message)

if __name__ == '__main__':
	HubServer(8801,'raspberrypi.garameki.com',logging.INFO)

