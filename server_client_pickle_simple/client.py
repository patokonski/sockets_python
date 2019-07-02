import socket
import datetime
import time
import pickle

# ------------------------------ CONSTS
HEADERSIZE = 10
SLEEP_TIME = 2
BUFF_SIZE = 20

# ------------------------------ VARS
msg_full = b''
msg_new = True
msg_len = 0

# ------------------------------ SERVER SOCKET CONFIG
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 1234))

while True:
    msg_full = b''
    msg_new = True
    while True:
        if msg_new:
            msg_new = False
            msg_full += s.recv(BUFF_SIZE)
            msg_len = int(msg_full[:HEADERSIZE])

        msg_full += s.recv(BUFF_SIZE)

        if len(msg_full) - HEADERSIZE == msg_len:
            print(msg_full)
            d = pickle.loads(msg_full[HEADERSIZE:])
            print(d)

            msg_new = True
            msg_full = b''