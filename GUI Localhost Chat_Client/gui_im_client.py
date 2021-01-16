# Varun Shourie, CIS345, Tuesday/Thursday, 12:00PM-1:15PM, A8

from tkinter import *
from tkinter import font
from tkinter import messagebox
from socket import *
from threading import Thread


def validate_keypress(event):
    """Restricts the key presses the user can make when entering the ip address for the application."""
    valid_keys = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '.', '\b', '']

    if event.char not in valid_keys:
        return "break"


def connect():
    """Connects to the server located on the user provided IP address, port 49000, resizing the window to include the
    newly placed chat widgets like the listbox, entry, and send button. Furthermore, a thread is started to handle
    receiving all messages for the chat client."""
    global sock, ip_address, screen_name, toggle_connection_button, window, chat_frame, PORT
    ip_addr = ip_address.get()
    scrn_name = screen_name.get()

    # IP address name should be at minimum '0.0.0.0' (7 chars) and the screen name should not be blank.
    if len(ip_addr) > 6 and scrn_name != '':
        try:
            addr = (ip_addr, PORT)
            sock = socket(AF_INET, SOCK_STREAM)
            sock.connect(addr)
            sock.send(scrn_name.encode())
        except:
            sock.close()
            sock = None
        else:
            x = Thread(target=receive_message, daemon=True)
            x.start()

        window.geometry('450x455')
        toggle_connection_button.config(bg='gold', text='Disconnect', command=disconnect)
        chat_frame.grid(row=3, column=0, columnspan=2, sticky=N+S+W+E, padx=10)
    else:
        messagebox.showinfo(title='Error', message='Please enter both an IP address with four numbers between 0 to 255 '
                                                   + 'separated by a period (.) and at least one character for your '
                                                   + 'desired screen name.')


def disconnect():
    """Whenever the user presses the disconnect button while in an active chat session, the client sends an exit
    sequence to the server to signal it is closing; the window is resized to exclude the chat section, and the
    disconnect button is toggled to "connect" to signal the GUI is not connected to the localhost server."""
    global sock, ip_address, screen_name, toggle_connection_button, window, chat_frame, EXIT

    try:
        if sock:
            sock.send(EXIT.encode())
    except:
        pass
    finally:
        if sock:
            sock.close()
        sock = None

    toggle_connection_button.config(bg='SystemButtonFace', text='Connect', command=connect)
    chat_frame.grid_forget()
    window.geometry('450x100')
    ip_address.set('')
    screen_name.set('')


def receive_message():
    """Handles receiving all messages for one chat client by inserting them into the listbox as they are received
    from other clients through the server. If there is no message from the server, the chat client will disconnect
    from the server."""
    global sock, screen_name, msg_listbox, BUFSIZE

    while True:
        try:
            received_msg = sock.recv(BUFSIZE)
        except OSError:
            received_msg = None
            break
        if not received_msg:
            disconnect()
            break
        msg_listbox.insert(END, received_msg.decode())


def send_message():
    """If the user's message is not blank, the function sends the user's message from the chat client to the server,
    which will distribute it to other clients. If the user types the exit sequence, the chat client will cease."""
    global sock, message, EXIT
    msg = message.get()
    if msg == EXIT:
        disconnect()
    elif msg != '':
        try:
            if sock:
                sock.send(msg.encode())
        except OSError:
            disconnect()
    message.set('')


def window_closing():
    """Disconnects the socket if not done already before closing the window."""
    global sock
    if sock:
        disconnect()
    window.quit()


PORT = 49000
EXIT = '[Q]'
BUFSIZE = 1024

# Variables used to display, send, and receive chat data throughout the entire application.
sock = socket(AF_INET, SOCK_STREAM)
window = Tk()
window.geometry('450x100')
window.title('CIS IM Client')
app_font = font.Font(family='Arial', size=12)
ip_address = StringVar()
screen_name = StringVar()
message = StringVar()

# Widgets used to intake server IP address and the user's screen name.
ip_label = Label(window, text='Server IP:', font=app_font)
ip_label.grid(row=0, column=0, sticky=W, padx=10)
screen_name_label = Label(window, text='Screen Name:', font=app_font)
screen_name_label.grid(row=1, column=0, sticky=W, padx=10)
ip_textbox = Entry(window, textvariable=ip_address, font=app_font, width=33)
ip_textbox.grid(row=0, column=1, sticky=E, padx=10)
ip_textbox.bind('<Key>', validate_keypress)
screen_textbox = Entry(window, textvariable=screen_name, font=app_font, width=33)
screen_textbox.grid(row=1, column=1, sticky=E, padx=10)

# Toggles between connection/disconnection from the chat server.
toggle_connection_button = Button(window, text='Connect', font=app_font, width=46, command=connect)
toggle_connection_button.grid(row=2, column=0, columnspan=2, pady=5)

# Section of the chat client which contains all messages from the user and other users present in the chat.
chat_frame = Frame(window, width=435, background='maroon')
msg_frame = Frame(chat_frame, width=408, height=300, background='maroon')
msg_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
msg_frame.pack_propagate(0)
scrollbar = Scrollbar(msg_frame)
msg_listbox = Listbox(msg_frame, yscrollcommand=scrollbar.set, font=app_font, width=43)
msg_listbox.pack(fill=BOTH, side=LEFT)
scrollbar.config(command=msg_listbox.yview)
scrollbar.pack(fill=Y, side=RIGHT)

# Widgets used to compose and send messages to other users on the chat hosted by the server.
msg_textbox = Entry(chat_frame, textvariable=message, width=37, font=app_font)
msg_textbox.grid(row=1, column=0, sticky=W, padx=10, pady=10)
send_button = Button(chat_frame, text='Send', font=app_font, command=send_message, bg='gold')
send_button.grid(row=1, column=1, sticky=E, padx=10)

window.protocol('WM_DELETE_WINDOW', window_closing)
window.mainloop()
