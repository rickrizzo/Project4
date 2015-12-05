import socket
import sys
import os
import shutil
from thread import *

#Server Information
HOST = ''
PORT = 8765

n_blocks = 128
blocksize = 4096

#Create Socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print "Socket created"

#Bind Socket
try:
	s.bind((HOST, PORT))
except socket.error as msg:
	print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message: ' + msg[1]
	sys.exit()
print "Socket bind complete"

#Listen
s.listen(10)
print "Socket listening"

#Create Directory

if os.path.exists('.storage'):
	shutil.rmtree('.storage')
else:
	os.makedirs('.storage')

#Handle Connections
def clientthread(conn):
	
	#Connections
	while True:

		#Recieve
		print "Block size is " + str(n_blocks)
		print "Number of blocks is " + str(blocksize)
		print "Listening on port " + str(PORT)
		data = conn.recv(1024)

		if not data:
			break

		#Recieve Data
		print "[thread ] Rcvd: ", data.split(' ')

		#Variables
		command = data.split(' ')
		reply = "Invalid command " + data;

		####Handle Commands###
		#Store File
		if command[0] == "STORE":
			if len(command) == 3:
				reply = "STORE FILE"

		#Read File
		if command[0] == "READ":
			if len(command) == 4:
				reply = "READ FILE"

		#Delete File
		if command[0] == "DELETE":
			if len(command) == 2:
				reply = "DELETE FILE"

		#Print Directory
		if command[0] == "DIR\n":
			if len(command) == 1:
				reply = "PRINT DIR"

		#Reply
		conn.send(reply)

	#Close
	conn.close()

#Create Threads
while 1:
	conn, addr = s.accept()
	print "Connected with ", addr[0], ":", str(addr[1])
	start_new_thread(clientthread, (conn,))

#Close Socket
s.close()