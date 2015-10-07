import socket
import sys

port = int(sys.argv[1])
host = socket.gethostname()
server_address = (host, port)

# Create socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to server port
sock.connect(server_address)
print "Connected to Server"

# greetings = "My name is Rob"
# sock.send(str.encode(greetings))


while 1:
        data = sock.recv(1024)
        if not data:
                break
        print str(data)
        msg = raw_input()
        if not msg:
                break
        else:
                sock.send(str.encode(msg))
sock.close()
