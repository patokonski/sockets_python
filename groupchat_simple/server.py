import socket
import select
from datetime import datetime
import sys

# CONSTS
HEADER_SIZE = 10
IP = "127.0.0.1"
PORT = 1234

def receive_message(csock):
    """Handling data received from client socket."""
    try:
        header = csock.recv(HEADER_SIZE)
        if not len(header):
            print(f"{datetime.now()}: Nothing to read. Connection closed by client.")
            return False
        header_length = int(header.decode('utf-8'))
        msg = csock.recv(header_length)
        return {'header': header, 'data': msg}
    except Exception as e:
        print(f"{datetime.now()}: Brutal client disconnection detected. Error: {str(e)}")
        return False


# CONFIGURING SERVER SOCKET
try:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((IP, PORT))
    server_socket.listen()
except Exception as e:
    print(f"Failed to initialize server socket. Error: {str(e)}")
    sys.exit()


# VARS
sockets_list = [server_socket]
clients = {}

# MAIN LOOP
while True:
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)
    for r_socket in read_sockets:
        # handle new connection to the server
        if r_socket == server_socket:
            client_socket, client_address = server_socket.accept()
            user = receive_message(client_socket)
            if not user:
                print(f"{datetime.now()}: Client {client_address[0]}{client_address[1]} disconnected from the server.")
                continue
            sockets_list.append(client_socket)
            clients[client_socket] = user
            print(f"{datetime.now()}: New client connected to the server from {client_address[0]}{client_address[1]}. Username: {user['data'].decode('utf8')}")
        # handle new message from the client
        else:
            message = receive_message(r_socket)
            if not message:
                print(f"{datetime.now()}: Client {clients[r_socket]['data'].decode('utf-8')} disconnected from the server.")
                sockets_list.remove(r_socket)
                del clients[r_socket]
                continue
            user = clients[r_socket]
            print(f"{datetime.now()}: New message from client: {clients[r_socket]['data'].decode('utf-8')}\nMessage: {message['data'].decode('utf-8')}")
            for client in clients:
                if client != r_socket:
                    client.send(user['header'] + user['data'] + message['header'] + message['data'])
    for exc_client in exception_sockets:
        pass
