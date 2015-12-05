import socket
import sys
from thread import *

#Server Information
HOST = ''
PORT = 9999

#Create Socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print "Socket created"

#Bind Socket
try:
	s.bind((HOST, PORT))
except socket.error as msg:
	print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
	sys.exit()
print "Socket bind complete"

#Listen
s.listen(10)
print "Socket listening"

#Handle Connections
def clientthread(conn):
	
	#Connections
	while True:

		#Recieve
		data = conn.recv(1024)
		if not data:
			break
		print "[thread ", current_thread(), "] Recieved: ", data
		reply = "Okay..." + str(data)

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