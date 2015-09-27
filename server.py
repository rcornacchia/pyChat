import socket
import sys
import select
import Queue

def authenticate(c):
    print "TEST"


def initializeServer():
    # Create socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setblocking(0)

    host = socket.gethostname()
    port = int(sys.argv[1])
    server_address = (host, port)

    server.bind(server_address)
    server.listen(5)

    # sockets to be read
    inputs = [ server ]

    # sockets to write to
    outputs = [ ]

    # outgoing message queus (socket:queue)
    message_queues = {}

    while inputs:
        # Wait for at least one of the sockets to be ready for processing
        print >>sys.stderr, '\nwatiing for the next event'
        readable, writeable, exceptional = select.select(inputs, outputs, inputs)

        # print "_________________________"
        # print "READABLE"
        # print readable
        # print "_________________________"

        for s in readable:
            if s is server:
                connection, client_address = s.accept()
                print >>sys.stderr, 'new connection from', client_address
                connection.setblocking(0)
                inputs.append(connection)
                message_queues[connection] = Queue.Queue()
            else:
                data = s.recv(1024)
                if data:
                    # A readable client socket has data
                    print >>sys.stderr, 'received "%s" from %s' % (data, s.getpeername())
                    message_queues[s].put(data)

                # interpret empty result as closed connection
                print >>sys.stderr, 'closing', client_address, 'after reading no data'
                #stop listening for input on the connection
                if s not in outputs:
                    outputs.append(s)
                else:
                    #interpret empty results as closed connection
                    print >>sys.stderr, 'closing', client_address, 'after reading no data'
                    # Stop listeining for input on the connection
                    if s in outputs:
                        outputs.remove(s)
                    inputs.remove(s)
                    s.close()

                    # Remove message queue
                    del message_queues[s]

        #
        # print "_________________________"
        # print "WRITEABLE"
        # print writeable
        # print "_________________________"
        # Handle outputs
        for s in writeable:
            try:
                next_msg = message_queues[s].get_nowait()
            except Queue.Empty:
                # No messages waiting so stop checking for writeability.
                print >>sys.stderr, 'output queue for', s.getpeername(), 'is empty'
                outputs.remove(s)
            else:
                print >>sys.stderr, 'sending "%s" to %s' % (next_msg, s.getpeername())
                s.send(next_msg)




        #
        # sread, swrite, sexcept = select.select(server, [], [])
        #
        # for s in sread:
        #     if s == server:
        #         # handle the server socket
        #         client, address = server.accept()
        #
        #     elif s == sys.stdin:
        #         # handle standard input
        #         junk = sys.stdin.readline()
        #         running = 0
        #     else:
        #         #handle all other sockets
        #         data = s.recv(size)
        #         if data:
        #             s.send(data)
        #         else:
        #             s.close()
        #             input.remove(s)

        # client, address = s.serveraccept()
        # print 'Connection received from', addr
        # print server.recv(1024)
        # c.send("What is your username")
        # #authenticate user
        # c.authenticate(c)

if __name__ == "__main__":
    # Read list of username-password combinations
    f = open ("user_pass.txt", "r")
    combos = f.read()
    f.close()

    # split by lines
    slices = combos.split('\n')

    # Create dictionary for usernames/password combos
    users = {}
    for i in slices:
            if i != '':
                    key, val = i.split(' ')
                    users[key] = val
    print users
    initializeServer()
