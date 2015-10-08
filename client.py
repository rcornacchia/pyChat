import socket
import sys
import select

timeout = 10
port = int(sys.argv[1])
host = socket.gethostname()
server_address = (host, port)

# Create socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print "TEST"
# Connect to server port
sock.connect(server_address)
# print "Connected to Server at %s" % server_address
print "TEST"
while 1:
        sys.stdout.write("> ")
        sys.stdout.flush()

        (sread, swrite, sexc) = select.select([0, sock], [],[])
        for s in sread:
                if s == 0:
                        data = sys.stdin.readline().strip()
            	        if data:
                                sock.sendall(data)
            	elif s == sock:
                        data = sock.recv(1024)
                        if not data:
                                break
                        elif data == "SERVER_SHUTDOWN":
                                print "Server shutting down\nYou have been logged out."
                                sock.close()
                                sys.exit()
                        elif data == "LOGOUT":
                                print "You are successfully logged out"
                                sock.close()
                                sys.exit()
                        else:
                                sys.stdout.write(data + '\n')
                                sys.stdout.flush()


        # Could use keyboard interrupt to spawn new thread and handle user input
        # add queue so that all messages can be handled



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
