import socket

mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# change the robot IP address here
host = '192.168.56.101'
port = 30001

mySocket.connect((host, port))

script_text="def test_move():\n" \
            "   global P_start_p=p[.6206, -.1497, .2609, 2.2919, -2.1463, -.0555]\n" \
            "   global P_mid_p=p[.6206, -.1497, .3721, 2.2919, -2.1463, -.0555]\n" \
            "   global P_end_p=p[.6206, -.1497, .4658, 2.2919, -2.1463, -.0555]\n" \
            "   while (True):\n" \
            "     movel(P_start_p, a=1.2, v=0.25)\n" \
            "     movel(P_mid_p, a=1.2, v=0.25)\n" \
            "     movel(P_end_p, a=1.2, v=0.25)\n" \
            "   end\n" \
            "end\n"

mySocket.send((script_text + "\n").encode())
mySocket.close()