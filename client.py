# Robert Cornacchia
# rlc2160
# Python client
import socket
import sys
import select
import signal

#signal handling
def signal_handler(signal, frame):
    print '\nYou pressed Ctrl+C!\nShutting Down\n'
    sock.send(str.encode("SHUT_DOWN"))
    sock.close()
    sys.exit()
signal.signal(signal.SIGINT, signal_handler)

timeout = 0
host = sys.argv[1]
# host = socket.gethostname()
port = int(sys.argv[2])
server_address = (host, port)

# Create socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect to server port
sock.connect(server_address)

# print "Connected to Server at %s" % server_address

loggedIn = False

while 1:
    if loggedIn:
            sys.stdout.write("Command: ")
    sys.stdout.flush()
    (sread, swrite, sexc) = select.select([0, sock], [],[])
    for s in sread:
        if s == 0:
            data = sys.stdin.readline().strip()

            if data:
                sock.sendall(data)
    	elif s == sock:
            try:
                data = sock.recv(1024)
            except socket.error, e:
                if isinstance(e.args, tuple):
                    print "errno is %d" % e[0]
                    if e[0] == errno.EPIPE:
                        # remote peer disconnected
                        print "Detected remote disconnect"
                    else:
                        # determine and handle different error
                        pass
                else:
                    print "socket error ", e
                    remote.close()
                    break
            except IOError, e:
                print "IOError:, ", e
                break
            else:
                # data = sock.recv(1024)
                if not data:
                    sock.send(str.encode("LOGOUT"))
                    print("Server shut down\nClient shutting down\n")
                    sock.close()
                    sys.exit()
                    break
                elif data == "SERVER_SHUTDOWN":
                    print "\nServer shutting down\nYou have been logged out."
                    sock.send("SHUT_DOWN")
                    sock.close()
                    sys.exit()
                elif data == "LOGOUT":
                    print "\nYou have successfully logged out"
                    sock.send("SHUT_DOWN")
                    sock.close()
                    sys.exit()
                elif data == "INACTIVE":
                    print "\nYou have been removed for being inactive for 30 minutes\nShutting Down\n"
                    sock.close()
                    sys.exit()
                elif data == "BLOCKED":
                    print "\nDue to being blocked, server no longer responding. Server shutting down."
                    sock.close()
                    sys.exit()
                elif data == "KICKED":
                    print "\nYou have been kicked"
                    sock.close()
                    sys.exit
                elif data == "Username:" or data == "Password:":
                    data = str(data).strip() + " "
                    sys.stdout.write(data)
                    sys.stdout.flush()
                elif data == "LOGGED_IN":
                    data = str(data).strip() + " "
                    sys.stdout.write("\nYou have logged in. Welcome!\n")
                    sys.stdout.flush()
                    loggedIn = True
                elif loggedIn == True:
                    sys.stdout.write("\n" + data + "\n")
                    sys.stdout.flush()
                else:
                    sys.stdout.write("\n" + data)
                    sys.stdout.flush()

sock.close()
