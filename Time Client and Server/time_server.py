# Varun Shourie, CIS345, Tuesday/Thursday, 12:00PM-1:15PM

from socket import *
import time

# Define constants for information on the server.
HOST = 'localhost'
PORT = 65000
ADDR = (HOST, PORT)
BUFSIZE = 1024
count = 0

# Create a socket, bind it to the host name/port number, and listen for up to 5 queued connections.
server = socket(AF_INET, SOCK_STREAM)
server.bind(ADDR)
server.listen(5)

print(f'The server has started and is listening on {ADDR}.')

# Accept the client's socket and IP address/port, print their info, and send encoded time.
while True:
    client, address = server.accept()
    count += 1
    name = client.recv(BUFSIZE)
    print(f'Connection {count} from {name.decode()} - {address}')

    msg = f'Current time: {time.ctime()}\nGoodbye!'
    client.send(msg.encode())
    client.close()

