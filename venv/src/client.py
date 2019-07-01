import socket

# conf socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect to socket, server and client are on same machine for now so gethostname can be used
s.connect((socket.gethostname(), 1234))

# determine HEADERSIZE
HEADERSIZE = 10

while True:
    # empty variable for message
    full_msg = ''
    # to track if its new message or we are receing rest of the buffor
    new_msg = True
    while True:
        msg = s.recv(16)
        if new_msg:
            print("new message length: {}".format(msg[:HEADERSIZE]))
            msglen = int(msg[:HEADERSIZE])
            new_msg = False

        full_msg += msg.decode("utf-8")

        if len(full_msg)-HEADERSIZE == msglen:
            print("full msg received")
            print(full_msg[HEADERSIZE:])
            new_msg = True
            full_msg = ''
    print(full_msg)
