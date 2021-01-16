# Varun Shourie, CIS345, Tuesday/Thursday, 12:00PM-1:15PM

from socket import *

# Define constants for information on the server.
HOST = 'localhost'
PORT = 65000
ADDR = (HOST, PORT)
BUFSIZE = 1024

# Create a socket for the server, send it the name of the user, and receive the time from the server.
server = socket(AF_INET, SOCK_STREAM)
server.connect(ADDR)
server.send('Varun'.encode())
current_time = server.recv(BUFSIZE)
server.close()

print(current_time.decode())
