import socket

mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# change the robot IP address here
# host = "10.0.2.15"
host = "192.168.56.101"
port = 29999

mySocket.connect((host, port))
print(mySocket.recv(4096).decode())
mySocket.send("robotmode\n".encode())
print(mySocket.recv(4096).decode())
mySocket.close()
