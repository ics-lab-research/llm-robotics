import socket

mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# change the robot IP address here
# host = '192.168.56.101'
host = '192.168.1.100'
port = 30001

mySocket.connect((host, port))

# with open("custom.script", 'r') as ur_file:
with open("pick_and_place.script", 'r') as ur_file:
    script_text = ur_file.read()

mySocket.send((script_text + "\n").encode())
mySocket.close()
