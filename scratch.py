#!/usr/bin/env python

import socket
import re
import array
import errno

class Error(Exception):
	"""Base class for exceptions in this module."""
	pass
class ScratchConnectionError(Error): pass	
class ScratchNotConnected(ScratchConnectionError): pass
class ScratchConnectionRefused(ScratchConnectionError): pass
class ScratchConnectionEstablished(ScratchConnectionError): pass

class Scratch:
	def __init__(self, host='localhost'):
		self.host= host
		self.port = 42001
		self.connect(poll=True)
		self.connected = 1

	def connect(self, poll=False):
		"""
		Creates a connection to the Scratch environment. If poll is True, blocks until
		Scratch is running, and listening for connections on port 42001, else connect()
		raises appropiate exceptions.
		"""
		while True:
			try:
				# create the socket here not in __init__() to avoid errno 22 invalid argument
				self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				self.connection.connect((self.host, self.port))
			except socket.error as (err, message):
				if err == errno.EISCONN:
					raise ScratchConnectionEstablished('Already connected to Scratch')
				elif poll == True:
					continue
				elif err == errno.ECONNREFUSED:
					raise ScratchConnectionRefused('Connection refused, try enabling remote sensor connections')
				else:
					print(err, message)
					raise ScratchConnectionError(message)
			break
		self.connected = 1

	def disconnect(self):
		self.connection.close()
		self.connected = 0

	def send(self, message):
		#credit to chalkmarrow from scratch.mit.edu
		n = len(message)
		a = array.array('c')
		a.append(chr((n >> 24) & 0xFF))
		a.append(chr((n >> 16) & 0xFF))
		a.append(chr((n >>  8) & 0xFF))
		a.append(chr(n & 0xFF))
		if self.connected:
			try:
				self.connection.send(a.tostring() + message)
			except socket.error as (err, message):
				raise ScratchConnectionError(message)
		else:
			raise ScratchConnectionError('Not connected to Scratch')

	def sensorupdate(self, data):
		"""Takes a dictionary and writes a message using the keys as sensors, and the values as the update values"""
		if not isinstance(data, dict):
			raise TypeError('Expected a dict')
		message = 'sensor-update'
		for key in data.keys():
			message = message+' "'+key+'" '+data[key]
		self.send(message)

	def broadcast(self, data):
		"""Takes a list of message strings and writes a broadcast message to scratch"""
		if not isinstance(data, list):
			raise TypeError('Expected a list')
		message = 'broadcast'
		for mess in data:
			message = message+' "'+mess+'"'
		self.send(message)

	def parse_message(self, message):
		#TODO: parse sensorupdates with quotes in sensor names and values
		#	   make more readable
		if message:
			sensorupdate_re = 'sensor-update[ ](((?:\").[^\"]*(?:\"))[ ](?:\"|)(.[^\"]*)(?:\"|)[ ])+'
			broadcast_re = 'broadcast[ ]\".[^"]*\"'
			sensors = {}
			broadcast = []

			sensorupdates = re.search(sensorupdate_re, message)
			if sensorupdates:
				# formats string to '<sensor> <value> <sensor1> <value1> ...'
				sensorupdates = sensorupdates.group().replace('sensor-update', '').strip().split()
				# for sensors that are multiple words, make sure that entire sensor name
				# shows up as one sensor value in the list
				i = 0
				sensorlist = []
				while i < len(sensorupdates):
					if sensorupdates[i][0] == '\"':
						if sensorupdates[i][-1] != '\"':
							j = i
							multisense = ''
							#now loop through each word in list and find the word 
							#that ends with " which is the end of the variable name
							while j < len(sensorupdates):
								multisense = multisense+' '+sensorupdates[j]
								if sensorupdates[j][-1] == '\"':
									break
								i+=1
								j+=1
							sensorlist.append(multisense.strip(' \"'))
						else:
							sensorlist.append(sensorupdates[i].strip(' \"'))
					else:
						sensorlist.append(sensorupdates[i])
					i+=1			
				i = 0
				# place sensor name and values in a dictionary
				while len(sensors) < len(sensorlist)/2:
					sensors[sensorlist[i]] = sensorlist[i+1]
					i+=2

			broadcasts = re.findall(broadcast_re, message)
			if broadcasts:
				# strip each broadcast message of quotes ("") and "broadcast"
				broadcast = [mess.replace('broadcast','').strip('\" ') for mess in broadcasts]
		
			return dict([('sensor-update', sensors), ('broadcast', broadcast)])
		else: 
			return None

	def receive(self, noparse=0):
		""" Receives data from Scratch
		Arguments:
			noparse: 0 to pass message through a parser and return the message as a data structure
				 	 1 to not parse message, but format as a string
				  	 2 to not parse message and not format as a string (returns raw message)
		"""
		try:
			mess = self.connection.recv(1024)
		except socket.error as (errno, message):
			raise ScratchConnectionError(errno, message)
		if not mess:
			return None
		if noparse == 0:
			return self.parse_message(repr(mess))
		if noparse == 1:
			return repr(mess)
		elif noparse == 2:
			return mess
		else:
			return self.parse_message(repr(mess))

if __name__ == "__main__":
	#runs and prints out raw messages received from Scratch
	try:
		s = Scratch()
	except ScratchConnectionError, e:
		print(e)
		exit(1)
	while 1:
		try:
			message = s.receive(2)
		except ScratchConnectionError, e:
			print(e)
			exit(1)	
		print(message)
