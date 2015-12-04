import socket
import sys

HOST, PORT = "localhost", 9999
data = " ".join(sys.argv[1:])

#Create Socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
	#Connect to Server
	sock.connect((HOST, PORT))
	sock.sendall(data + "\n")

	#Recieve from Server
	received = sock.recv(1024)

finally:
	sock.close()

print("Sent:     {}").format(data)
print ("Recieved: {}").format(received)