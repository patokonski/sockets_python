import socket

# conf socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect to socket, server and client are on same machine for now so gethostname can be used
s.connect((socket.gethostname(), 1234))

# accept message from server (dataframe size is 1024)
msg = s.recv(1024)

# decode
msg.decode("utf-8")

# print message from server
print(msg)
