import socket
import sys

#Variables
host = ''
port = 9999
message = "GET / HTTP/1.1\r\n\r\n"

#Create Socket
try:
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
	print("Failed to create socket")
	sys.exit()
print("Socket Created")

#Connect to Host
try:
	remote_ip = socket.gethostbyname(host)
except socket.gaierror:
	print("Host could not be resolved")
	sys.exit()
s.connect((remote_ip, port))
print("Connected to ", host, " on IP ", remote_ip)

#Send Data
try:
	s.sendall(message)
except socket.error:
	print("Send failed")
	sys.exit()
print("Message successfully recieved")

#Recieve Data
reply = s.recv(4096)
print("Reply: ", reply)