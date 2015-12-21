#Study Guide  
This guide was created to summarize the concepts and topics studied in Operating Systems

##File Descriptors  
File descriptors are values in a File Descriptor Table that point to various inputs and outputs. By default they are as follows:  
0 = stdin  
1 = stdout  
2 = stderr  

##C Commands  
- pipe(int p [2])
  - passed an array of integers
  - returns 0 on success and -1 on error
  - occupies the next available file descriptors, by default 3 and 4. this means p[0] = 3, and p[1] 4 in the example above
  - in the shell, pipe is used to bring input from one command into another EX: ls | grep "doc" returns all documents in a directory
- fork()
  - passed no arguments
  - returns twice, once in each thread
  - fork returns a negative value on error, a 0 indicating a child thread, and a positive value, namely the ID of the child, in the parent thread
  - when fork is called, everything below the statement is duplicated and happens independent of the other thread
  - when a child process terminates, it returns information regarding termination. this remains with the kernal and in the system as a zombie process until wait is called by the parent
  - when a parent process with children terminates, the children are orphaned. they will be reassigned a parent with a PID of 1
  - Fork will fail if the imposed limit of processes is exceeded, if the total number of processes under a single user is exceeded, or if there is insufficient space to swap to a new process
  - By limiting the number of processes a user can have, or the number of processes running, and operating system can prevent a fork bomb
- wait(NULL)
  - waits for the child process to terminate in a forked process
  - typically passed no arguments, but can be passed a pointer to get the exit code of process
  - returns the process ID of the process that it was waiting on
- open()
  - opens a file for use in a program
  - Returns the file descriptor by which to access the file, returns the lowest free descriptor
  - If return is negative, an error occuered
- close()
  - closes an open file descriptor
  - passed an integer
  - returns 0 on success and -1 on failure 
- write()
  - write n bytes from a buffer to a file, associated bt the handle (or a pipe file descriptor)
  - passed three parameters, the file descriptor, the buffer or string, and the number of bytes to write
  - returns the number of bytes written to the file, or -1 indicating an error
- read()
  - reads n bytes from a file descriptor and places those read characters into a buffer
  - passed three parameters, the file descriptor, the buffer, and the number of bytes to read
  - returns the number of bytes read, or -1 indicating an error
- dup()
  - duplicates a file descriptor
  - takes one argument, the old file descriptor, and creates a copy of it at the lowest available file descriptor
  - on success, returns the new descriptor, and -1 on error
- dup2() 
  - duplicates a file descriptor
  - takes two arguments, first the old file descriptor, and then the new file descriptor, which is closed and set to the old file descriptor, creating a second copy
  - on success, returns the new descriptor, and -1 on error
- fflush()
  - flushes the output buffer of a stream
  - takes one argument, the output stream, like stdout or stderr
  - returns 0 on success, and -1 on error

##Scheduling
Wait Time  
- The amount of time spend in the ready queue
Turnaround Time  
- Wait Time + CPU Burst  
CPU Bound
- If something is CPU bound, that means the largest impact could be made by increasing CPU speed. That is where things are taking the longest  
IO Bound
- If something is IO bound, that mains the largest imapct could be made by increasing the IO speed. That is where things are taking the longest.

##Exponential Averaging
tau[i + 1] = alpha * t[i] + (1 - alpha) * tau[i]  
tau = estimated burst time  
t = actual burst time  

##Multi Threading
- pthread_create()  
  - creates a new thread
  - passed four parameters, a thread ID, an attribute (typically null), a function to execute, and any arguments
  - returns 0 for success, and various other codes on error  
- pthread_join()
  - make calling thread wait until specified thread terminates
  - passed two arguments, the thread and the value (typically null)
  - returns 0 on success, or other value on error  

####BEWARE STATICALLY ALLOCATED VARIABLES

##Memory
1 Kilobyte = 1024 Bytes  
1 Megabyte = 1048576 Bytes  
1 Gigabyte = 1073741824 Bytes  

Internal Fragmentation - when there is empty space within a block (non-dynamic or fixed allocation)  
External Fragmentation - when blocks are free in memory, but too small to be used (dynamic allocation) 

####Contiguous Memory
Subject to external fragmentation  
Allocation Algorithms
- First Fit
- Best Fit
- Next Fit  

####Noncontiguous Memory
Subject to internal fragmentation  
Allocation Algorithms
- FIFO or first in, first out
- OPT or optimal
- LRU or least recently used
- LFU or least frequently used

Working Set - the values adjacent to an indicated point, with a delta determining how far away (to the left), no repetition

Page Tables
- Total space = 2^{num bits}
- Page Number = num bits - page offset = first X bits
- Page Offset = num bits - page number = last N - X bits
- Number of Pages = 2^{page number}
- Page Size = 2^(page offset)
- Frame Size = 2^(page offset)
- Pages Required = ceil(process size / page offset)
- External Fragmentation = 0
- Internal Fragmentation = (page offset * pages required) - process size
- paged memory reference = 2 * memory reference/requested memory access
- TLB, or Translation Lookaside Buffer works on the princple of locality to reduce access time for processes on the same page
- TLB hit = memory reference + TLB access
- TLB miss = memory reference + paged memory reference + TLB access
- EMAT = %tlb_hit * time + %tlb_miss * time
