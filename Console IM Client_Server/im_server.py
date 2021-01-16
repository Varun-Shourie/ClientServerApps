# Varun Shourie, CIS345, Tuesday/Thursday, 12:00PM-1:15PM

from socket import *

# Constants used throughout the application
COMPUTER_NAME = gethostname()
HOST = '127.0.0.1'
PORT = 49000
ADDR = (HOST, PORT)
BUFSIZE = 1024
EXIT = '[Q]'

# Create a socket, bind it to IP address/port, and gather user's screen name.
sock = socket(AF_INET, SOCK_STREAM)
sock.bind(ADDR)
print(f'{COMPUTER_NAME}: Bind on and IP: {HOST}\n{sock}')
server_screen_name = input('Enter your screen name: ')

# Listen and accept connections from clients, send them the server's screen name.
sock.listen(1)
print('Waiting for connections.')
conn, addr = sock.accept()
print(f'Client connected -- connection from host IP addr {addr[0]}: port number {addr[1]}')
client_screen_name = conn.recv(BUFSIZE).decode()
print(f'{client_screen_name} has entered the chat...\nPress {EXIT} to leave the chat.')
conn.send(server_screen_name.encode())

# Keep on sending messages from the server and receiving messages from client until EXIT phrase is provided.
while True:
    server_msg = input(f'{server_screen_name}>> ')
    if server_msg == EXIT:
        conn.send('Server shutting down...'.encode())
        conn.close()
        break
    conn.send(f'{server_msg}'.encode())

    client_msg = conn.recv(BUFSIZE).decode()
    print(f'{client_screen_name}>> {client_msg}')
