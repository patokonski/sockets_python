import socket
import sys
from datetime import datetime
import errno

# CONSTS
HEADER_SIZE = 10
IP = "127.0.0.1"
PORT = 1234

# CLIENT SOCKET CONFIG
try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((IP, PORT))
    client_socket.setblocking(False)
except Exception as e:
    print(f"{datetime.now()}: Failed to create client socket. Error: {str(e)}")
    sys.exit()


# SEND INIT MESSAGE WITH USERNAME
username = input("Enter your username: ")
user = username.encode('utf-8')
message = f"{len(user):<{HEADER_SIZE}}".encode('utf-8')
client_socket.send(message + user)

# MAIN LOOP
while True:
    # get message from user and sand it if any
    message = input(f"{datetime.now()}: {username} > ")
    if message:
        message = message.encode('utf-8')
        message_h = f"{len(message):<{HEADER_SIZE}}".encode('utf-8')
        client_socket.send(message_h + message)
    # get all the waiting data and display it
    try:
        while True:
            header_length = client_socket.recv(HEADER_SIZE)
            if not len(header_length):
                print(f"{datetime.now()}: Connection closed by the server.")
                sys.exit()
            usr = client_socket.recv(int(header_length.decode('utf-8'))).decode('utf-8')
            message_length = client_socket.recv(HEADER_SIZE)
            message = client_socket.recv(int(message_length.decode('utf-8'))).decode('utf-8')
            print(f"{datetime.now()}: {usr} > {message}")
    # handling specific errors to ensure all data has been read
    except IOError as e:
        if e.errno != errno.EWOULDBLOCK and e.errno != errno.EAGAIN:
            print(f"{datetime.now()}: Reading error: {str(e)}")
            sys.exit()
        continue
    except Exception as e:
        print(f"{datetime.now()}: Reading error: {str(e)}")
        sys.exit()
