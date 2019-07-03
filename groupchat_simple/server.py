import socket
import select

# CONSTS
HEADER_SIZE = 10
LISTEN_QUEUE = 5
IP = socket.gethostname()
PORT = 1234


# SOCKET
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((IP, PORT))
server_socket.listen(LISTEN_QUEUE)

# VARS
sockets_list = [server_socket]
clients = {}


def receive_message(client_socket):
    try:
        msg_header = client_socket.recv(HEADER_SIZE)

        if not len(msg_header):
            return False

        msg_length = int(msg_header.decode("utf-8"))
        msg = client_socket.recv(msg_length)

        return {"header": msg_header, "data": msg}

    except:
        return False


while True:
    pass

