import socket
import select

# TODO: need to be tested after client implementation

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
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

    for socketn in read_sockets:
        if socketn == server_socket:
            client_socket, client_address = server_socket.accept()
            user = receive_message(client_socket)

            if user is False:
                continue

            sockets_list.append(client_socket)
            clients[client_socket] = user

            print(f"New connection accepted. IP: {client_address}, username: {user['data'].decode('utf-8')}")

        else:
            message = receive_message(socketn)
            if message is False:
                print(f"Closed connection from {clients[socketn]['data'].decode('utf-8')}")
                sockets_list.remove(socketn)
                del clients[socketn]
                continue

            user = clients[socketn]
            print(f"Received message from {user['data'].decode('utf-8')}: {message['data'].decode('utf-8')}")

            for csocket in clients:
                if csocket != socketn:
                    csocket.send(user['header'] + user['data'] + message['header'] + message['data'])

    for socketn in exception_sockets:
        sockets_list.remove(socketn)
        del clients[socketn]

