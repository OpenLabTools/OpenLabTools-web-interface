import socket
# TCP_IP = '127.0.0.1'
TCP_IP = 'lz307.user.srcf.net'
TCP_PORT = 7080
BUFFER_SIZE = 1024
MESSAGE = "Hello, World!"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send(MESSAGE)
data = s.recv(BUFFER_SIZE)
print data