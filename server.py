import Queue
import socket
import sys
import select

# Read list of usernmae-password combinations
f = open("user_pass.txt", "r")
raw_txt = f.read()
f.close()

# Split by lines
slices = raw_txt.split('\n')

# Create dictionary for usernames/password combos
users = {}
for i in slices:
        if i != '':
                key, val = i.split(' ')
                users[key] = val

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#server.setblocking(0)

host = socket.gethostname()
port = int(sys.argv[1])
server_address = (host, port)

server.bind(server_address)
server.listen(5)

# Set up for select
inputs = [server]
outputs = []
message_queues = {}

while inputs:
        print "Server online"

        read, write, exceptional = select.select(inputs, outputs, inputs)

        for s in readable:
                if s is server:
                        conn, addr = server.accept()
                        conn.setblocking(0)
                        print "Connection received from: ", addr
                        inputs.append(conn)
                        message_queues[conn] = Queue.Queue()
                else:
                        data = s.recv(1024)
                        if data:
                                # A readable client has data
                                print "received '%s' from %s" % (data, s.getpeername())
                                message_queues[s].put(data)

                        # interpret empty result as closed connection
                        print "closing", client_address, 'after reading no data'
                        if s not in outputs:
                                outputs.append(s)
                        else:
                                print "closing", client_address, "after reading no data"
                                if s in outputs:
                                        outputs.remove(s)
                                inputs.remove(s)
                                s.close()

                                # Remove message queue
                                del message_queue[s]
                        
        for s in writeable:
                try:
                        next_msg = message_queues[s].get_nowait()
                except Queue.Empty:
                        print "output queue for ", s.getpeername(), "is empty"
                        outputs.remove(s)
                else:
                        print "Sending '%s' to %s" % (next_msg, s.getpeername())
                        s.send(next_msg)
                         

