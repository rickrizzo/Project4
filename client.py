import socket
import sys

#Variables
host = 'localhost'
port = 8765

#Create Socket
try:
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
	print "Failed to create socket"
	sys.exit()
print "Socket Created"

#Connect to Host
try:
	remote_ip = socket.gethostbyname(host)
except socket.gaierror:
	print("Host could not be resolved")
	sys.exit()
s.connect((remote_ip, port))
print "Connected to", host, "on IP", remote_ip

#Send Data
while True:
	try:
		command = raw_input("Enter a command: ")
		#Upload Files
		#if(command.split(' ')[0] == "STORE" and len(command.split(' ')) == 3):

		s.send(command + "\n")
	except socket.error:
		print "Send failed"
		sys.exit()

	#Recieve Data
	reply = s.recv(4096)
	print "Reply: ", reply

#Close Connection
s.close()