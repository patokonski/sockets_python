import socket
import datetime
import time
import pickle

def build_msg(msg, header_size):
    return bytes(f"{len(msg):<{header_size}}", "utf-8") + msg


# ------------------------------ CONSTS
HEADERSIZE = 10
SLEEP_TIME = 2

# ------------------------------ VARS
msg_new_client = "Welcome to server lad!"

# ------------------------------ SERVER SOCKET CONFIG
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 1234))
s.listen(5)

while True:
    # accept connection
    client_socket, adress = s.accept()
    print(f"New connection to the server: {adress}")

    # pickle data (dict for example) and send it to client
    dicc = {1: "start", 2:[3, "1", ([2, "5"],[5, "2"])], 3: "end"}
    msg = pickle.dumps(dicc)
    msg = build_msg(msg, HEADERSIZE)
    print(msg)
    client_socket.send(msg)

