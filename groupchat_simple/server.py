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




