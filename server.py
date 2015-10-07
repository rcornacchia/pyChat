import socket
import sys
import thread



def authenticateClient(conn, addr):
        print "Client connected: " + addr[0] + " : " + str(addr[1])

        # Ask client for username
        conn.send(str.encode("Enter username: "))

        uname = ""
        recvdUsername = False
        recvdCorrectName = False
        recvdPass = False
        loggedIn = False
        loginAttempt = 0
        while 1:
                # if recvdCorrectName == False:

                # elif recvdPass == False:
                        # conn.send(str.encode("Enter password: "))
                data = conn.recv(1024)
                data = str(data)
                print "\n DATA RECEIVED " + data + "  END TRANSMISSION\n"
                if not data:
                        break
                else:
                        print str(data)

                        if recvdCorrectName:
                                if str(data) == str(users.get(uname)):
                                        # User has logged in
                                        conn.send(str.encode("Welcome to the chat server"))
                                        activeUsers.append(uname)
                                        print "\nCURENTLY ACTIVE USERS"
                                        print activeUsers
                                        print
                                        handleUser(conn, addr)
                                elif loginAttempt < 2:
                                        print "BAD LOGIN ATTEMPT"
                                        loginAttempt += 1
                                        conn.send(str.encode("Incorrect Password\nYou have " + str(3-loginAttempt) + " attempts left\nTry again"))
                                else:
                                        conn.send(str.encode("Incorrect Password. YOU HAVE NO ATTEMPTS LEFT! YOU WILL BE DROPPED!!!!"))
                                        # TODO drop connection and Block user for BLOCK_TIME

                        if recvdCorrectName == False and users.has_key(data):     # Check if username exists
                                if data in activeUsers:
                                        conn.send(str.encode(str(data) + " is already logged in.\nEnter different username"))
                                else:
                                        uname = data
                                        recvdCorrectName = True
                                        conn.send(str.encode("Enter password for " + data))
                        elif recvdCorrectName == False:
                                conn.send(str.encode("User does not exist\nEnter correct username"))


def handleUser(conn, addr):

    while 1:

            # Broadcast user has logged in
            data = conn.recv(1024)
            data = str(data)
            if not data:
                    break
            print str(data)
        # conn.close()


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

# Create a list of all users that are logged in
activeUsers = []

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

print "\n\nWaiting for connections on port %s" % (port)

while 1:
        conn, addr = server.accept()
        thread.start_new_thread(authenticateClient, (conn, addr))

server.close()
