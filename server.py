import socket
import sys
from thread import *
from sys import stdout
import math

#Server Information
HOST = ''
PORT = 9999

n_blocks = 128
blocksize = 4096
simmem = []
#dict to track names currently used
fnames = {}
#print on one line without spaces
Print = sys.stdout.write

#the below initializes the simulated memory
for i in range(n_blocks):
	simmem.append('.')

eqln = []
for i in range(32):
	eqln.append('=')

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

#prints memory nice and pretty
def printmem():
	for i in eqln:
		Print(i)
	for i in range(len(simmem)):
		if not i % 32:
			Print("\n")
		Print(simmem[i])
	Print("\n")
	for i in eqln:
		Print(i)
	Print("\n")
	return

#stores data, currently only simulates this
def store(cmdln):
	if len(cmdln) != 3:
		conn.send("ERROR: invalid STORE usage\n STORE syntax: STORE <filename> <bytes>\\n<file-contents>\n")
		return
	i = num_written = prevpos = openb = 0
	clusters = 1
	curchar = 65
	fname = cmdln[1]
	fsize = float(cmdln[2])
	blocks = int(math.ceil(fsize / blocksize))
	#counts how many open blocks there are
	for row in simmem:
		for column in row:
			if column == '.':
				openb+=1
	#increments curchar to one that is available as a file label	
	while chr(curchar) in fnames.values():
		curchar+=1

	if blocks > openb:
		conn.send("ERROR: not enough storage\n")
		return
	
	if fnames.has_key(fname):
		conn.send("ERROR: FILE EXISTS\n")
		return
	else:
		#enters the file into simulated memory
		fnames.update({str(fname):chr(curchar)})
		while num_written < blocks:
			#determines if memory can be written to this location
			if simmem[i] == '.':
				simmem[i] = chr(curchar)
				print chr(curchar)
				num_written+=1
				prevpos = i
			#determines if another cluster has been used
			if (prevpos) != (i):
				clusters+=1
			i+=1
		Print("[thread " + "1" + "] Stored file '" + chr(curchar) + "' (" + str(int(fsize)) + " bytes; " + str(blocks) + " blocks; " + str(clusters))
		if clusters == 1:
			Print(" cluster)\n")
		else:
			Print(" clusters)\n")
		Print("[thread " + "1" + "] Simulated Clustered Disk Space Allocation:\n")
		printmem()
		conn.send("ACK\n")
		Print("[thread " + "1" + "] Sent: ACK\n")
	

#Handle Connections
def clientthread(conn):
	
	print "Block size is " + str(n_blocks)
	print "Number of blocks is " + str(blocksize)
	print "Listening on port " + str(PORT)
	
	#Connections
	while True:

		#Recieve
		data = conn.recv(1024)
		print "[thread ", "1", "] Rcvd: ", data
		if not data:
			break
		cmdln = data.split()
		if cmdln[0] == "STORE":
			store(cmdln)
		elif cmdln[0] == "READ":
			read(cmdln)
		elif cmdln[0] == "DELETE":
			delete(cmdln)
		elif cmdln[0] == "DIR":
			Dir()
		else:
			conn.send("ERROR: Unrecognized command: " + str(cmdln[0]) + '\n')
		reply = "Okay..." + str(data)

		#Reply
		conn.send(reply)

	#Close
	conn.close()

#Create Threads
while 1:
	conn, addr = s.accept()
	print "Received incoming connection from", addr[0], ":", str(addr[1])
	start_new_thread(clientthread, (conn,))

#Close Socket
s.close()