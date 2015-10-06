import socket
import sys

port = int(sys.argv[1])
host = socket.gethostname()
server_address = (host, port)

# Create socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to server port
sock.connect(server_address)
print "connecting to server"

greetings = "My name is Rob"
sock.send(str.encode(greetings))
