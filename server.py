import socket
import sys
import os
import shutil
import math
import threading
from sys import stdout

#ToDo
#Rob - Read
#Harrison - Delete, Memory, 

#Server Information
HOST = ''
PORT = 8765

#Storage Information
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
	print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message: ' + msg[1]
	sys.exit()
print "Socket bind complete"

#Listen
s.listen(10)
print "Socket listening"

#Create Directory
if os.path.exists('.storage'):
	shutil.rmtree('.storage')
os.makedirs('.storage')

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
		conn.send("ERROR: INVLAID STORE USEAGE\nEX: STORE <filename> <bytes>\\n<file-contents>\n")

	i = num_written = openb = 0
	clusters = 0
	curchar = 65
	flag = False
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
		conn.send("ERROR: NOT ENOUGH STORAGE\n")
		return
	
	if fnames.has_key(fname):
		conn.send("ERROR: FILE EXISTS\n")
		return
	else:
		#receives and writes file to disk
		clientFile = conn.recv(int(cmdln[2]))
		f = open('.storage/' + cmdln[1], 'w+')
		f.write(clientFile)
		f.close()
		
		#enters the file into simulated memory
		fnames.update({str(fname):chr(curchar)})
		while num_written < blocks:
			#determines if memory can be written to this location
			if simmem[i] == '.':
				simmem[i] = chr(curchar)
				num_written+=1
			i+=1
		#determines if another cluster has been used
		for i in simmem:
			if i == chr(curchar) and not flag:
				clusters+=1
				flag = True
			elif i != chr(curchar):
				flag = False

		Print("[thread " + str(threading.current_thread().ident) + "] Stored file '" + chr(curchar) + "' (" + str(int(fsize)) + " bytes; " + str(blocks) + " blocks; " + str(clusters))
		if clusters == 1:
			Print(" cluster)\n")
		else:
			Print(" clusters)\n")
		Print("[thread " + str(threading.current_thread().ident) + "] Simulated Clustered Disk Space Allocation:\n")
		printmem()
		Print("[thread " + str(threading.current_thread().ident) + "] Sent: ACK\n")
	
#deletes data
def delete(cmdln):
	if not cmdln[1] in fnames.keys():
		conn.send("ERROR: NO SUCH FILE\n")
		return
	
	for i in range(len(simmem)):
		if simmem[i] == fnames[cmdln[1]]:
			simmem[i] = '.'
	
	PRINT("Deleted " + cmdln[1] + " file '" + fnames[cmdln[1]] + "' (deallocated X blocks)")
	del fnames[cmdln[1]]
	Print("[thread " + str(threading.current_thread().ident) + "] Simulated Clustered Disk Space Allocation:\n")
	printmem()
	Print("[thread " + str(threading.current_thread().ident) + "] Sent: ACK\n")
	
def Dir():
	names = fnames.keys()
	if len(names):
		names.sort()
		msg = ""
		for i in names:
			msg+=str(i)+"\n"
		return str(len(names)) + "\n" + msg
	else:
		return "0\n";
	
#Handle Connections
def clientthread(conn):
	
	#Connections
	while True:
		#Recieve
		data = conn.recv(1024)

		#If Client Quit
		if(len(data) == 0):
			print "Client closed its socket...terminating"
			break

		#Recive Data
		if not data:
			break
		Print( "[thread " + str(threading.current_thread().ident) + "] Rcvd: " + data.rstrip('\n') + "\n")

		#Variables
		command = data.rstrip('\n').split(' ')
		reply = "Invalid command " + data;

		#Store File
		if command[0] == "STORE":
			if len(command) == 3:
				store(command)
				reply = "ACK\n"
			else:
				conn.send("WRONG")
				reply = "ERROR: INVALID STORE USAGE\nEX: STORE <filename> <bytes>\\n<file-contents>\n"

		#Read File
		if command[0] == "READ":
			if len(command) == 4:
				if fnames.has_key(command[1]):
					if (int(command[2]) + int(command[3])) <= os.path.getsize('.storage/' + command[1]):
						fRead = open('.storage/' + command[1])
						fRead.read(int(command[2]))
						contents = fRead.read(int(command[3]))
						reply = "ACK " + command[3] + "\n" + contents;
						fRead.close()
					else:
						reply = "ERROR: INVALID BYTE RANGE\n"
				else:
					reply = "ERROR: NO SUCH FILE\n"
			else:
				reply = "ERROR: INVALID READ USAGE\nEX: READ <filename> <byte-offset> <length>"

		#Delete File
		if command[0] == "DELETE":
			if len(command) == 2:
				delete(command)
				reply = "ACK\n"
			else:
				reply = "ERROR: invalid DELETE usage\n DELETE syntax: DELETE <filename>\n"
				
		#Print Directory
		if command[0] == "DIR":
			if len(command) == 1:
				reply = Dir()
			else:
				reply = "ERROR: invalid DIR usage\n DIR syntax: DIR\n"

		#Reply
		conn.send(reply)

	#Close
	conn.close()

#Create Threads
while 1:
	conn, addr = s.accept()
	print "Block size is " + str(n_blocks)
	print "Number of blocks is " + str(blocksize)
	print "Received incoming connection from ", addr[0], ":", str(addr[1])
	threading.Thread(target= clientthread, args= (conn, )).start()

#Close Socket
s.close()