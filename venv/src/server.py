import socket
import datetime
import time


def build_msg(msg, header_size):
    return f"{len(msg):<{header_size}}"+msg


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
    msg = build_msg(msg_new_client, HEADERSIZE)
    client_socket.send(bytes(msg, "utf-8"))

    while True:
        time.sleep(SLEEP_TIME)
        msg = build_msg(str(datetime.datetime.now()), HEADERSIZE)
        print(f"{datetime.datetime.now()}: Sending message to client: {adress}")
        client_socket.send(bytes(msg, "utf-8"))