import socket
import sys
import threading

def handleClient(conn, addr):
        print "Client connected: " + addr[0] + " : " + str(addr[1]) 
        while 1:
                data = conn.recv(1024)
                reply = "OK" + data
                print(reply)
                conn.sendall(reply)

        conn.close()


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

try:
        server.bind(server_address)
except:
        print("Error: Bind() failed. %s") % (socket.error)
        sys.exit()

server.listen(10)

print "Waiting for connections on port %s" % (port)

while 1:
        conn, addr = server.accept()
        threading.Thread(target=handleClient, args=(conn, addr)).start()
