import socket
import time

# create socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind socket to local ip and 1234 port
s.bind((socket.gethostname(), 1234))

# queue
s.listen(5)

# determine headersize
HEADERSIZE = 10

while True:
    # on connection accept and get data
    client_socket, adress = s.accept()

    # print msg for debug purposes
    print("New connection from: {}",format(adress))

    # send message to the client
    msg = "Hello new client!"
    msg = f'{len(msg):<{HEADERSIZE}}' + msg

    client_socket.send(bytes(msg, "utf-8"))

    while True:
        time.sleep(3)
        msg = f"Time is: {time.time()}"
        msg = f'{len(msg):<{HEADERSIZE}}' + msg
        client_socket.send(bytes(msg, "utf-8"))