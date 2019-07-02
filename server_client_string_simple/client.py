import socket
import datetime
import time

# ------------------------------ CONSTS
HEADERSIZE = 10
SLEEP_TIME = 2
BUFF_SIZE = 20

# ------------------------------ VARS
msg_full = ''
msg_new = True
msg_len = 0

# ------------------------------ SERVER SOCKET CONFIG
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 1234))

while True:
    msg_full = ''
    msg_new = True
    while True:
        if msg_new:
            msg_new = False
            msg_full += s.recv(BUFF_SIZE).decode("utf-8")
            msg_len = int(msg_full[:HEADERSIZE])

        msg_full += s.recv(BUFF_SIZE).decode("utf-8")

        if len(msg_full) >= msg_len - HEADERSIZE:
            msg_new = True
            print(f"{datetime.datetime.now()}: New message from server: {msg_full[HEADERSIZE:]}")
            msg_full = ''
