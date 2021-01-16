# Varun Shourie, CIS345, Tuesday/Thursday, 12:00PM-1:15PM

from socket import *

HOST = '127.0.0.1'
PORT = 49000
ADDR = (HOST, PORT)
BUFSIZE = 1024

# Create a socket obj, connect to server, and send client's screen name.
sock = socket(AF_INET, SOCK_STREAM)
client_screen_name = input('Enter screen name: ')
sock.connect(ADDR)
sock.send(client_screen_name.encode())

# Receive server's screen name.
server_screen_name = sock.recv(BUFSIZE).decode()
print(f'{server_screen_name} has joined the chat...\nType[Q] to quit the application...')

# Receive messages from server first and send the client's response to server as long as exit sequence is not provided.
while True:
    server_msg = sock.recv(BUFSIZE).decode()
    print(f'{server_screen_name}>> {server_msg}')

    client_msg = input(f'{client_screen_name}>> ')
    if client_msg == '[Q]':
        sock.send('Leaving chat...'.encode())
        sock.close()
        break
    sock.send(client_msg.encode())
