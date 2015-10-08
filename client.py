import socket
import sys
import select

timeout = 10
port = int(sys.argv[1])
host = socket.gethostname()
server_address = (host, port)

# Create socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to server port
sock.connect(server_address)
# print "Connected to Server at %s" % server_address

while 1:
        sys.stdout.write("> ")
        sys.stdout.flush()

        (sread, swrite, sexc) = select.select([0, sock], [],[])
        for s in sread:
        	if s == 0:
        		data = sys.stdin.readline().strip()
        		if data: sock.sendall(data)
        	elif s == sock:
        		data = sock.recv(1024)
        		if not data:
        			break
        		else:
        			sys.stdout.write(data + '\n')
        			sys.stdout.flush()

        #
        #
        # data = sock.recv(1024)
        # if not data:
        #         break
        # print str(data)
        # if data == "LOGOUT":
        #         print "You have been successfully logged out"
        #         sock.close()
        #         sys.exit()
        # msg = raw_input("")
        # if not msg:
        #         break
        # else:
        #         sock.send(str.encode(msg))






sock.close()
