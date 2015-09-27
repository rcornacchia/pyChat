import socket
import sys


if __name__ == "__main__":
    s = socket.socket()
    host = socket.gethostname()
    port = int(sys.argv[1])
    s.connect((host, port))

    print s.recv(1024)
    username = raw_input(s.recv(1024))

    s.send(username)
