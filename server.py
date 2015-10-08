# Robert Cornacchia
# rlc2160
# Python multithreading server


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
                data = conn.recv(1024)
                data = str(data)
                print "\n DATA RECEIVED " + data + " END TRANSMISSION\n"
                if not data:
                        break
                else:
                        print str(data)

                        if recvdCorrectName:
                                if str(data) == str(users.get(uname)):
                                        # User has logged in
                                        conn.send(str.encode("Welcome to the chat server"))
                                        activeUsers[uname] = [conn, addr]
                                        print "\nCURENTLY ACTIVE USERS"
                                        print activeUsers.keys()
                                        handleUser(conn, addr, uname)
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


def handleUser(conn, addr, uname):
        while 1:
                # Broadcast user has logged in
                data = conn.recv(1024)
                data = str(data)
                if not data:
                        break
                else:
                        commands = data.split(' ')
                        broadcastTo = []
                        command = str(commands[0])
                        if command == "whoelse":
                                others = "\nOthers in the chat:\n"
                                for person in activeUsers:
                                        if person is not uname:
                                                    others = others + "\n" + person
                                if others == "\nOthers in the chat:\n":
                                        others = "\nThere is no one else here.\n"
                                conn.send(str.encode(others))
                        elif command == "wholast":
                                #get number: commands[1]
                                #0 < number < 60
                                #use timestamp and function that iterates through ActiveUsers and time they logged in
                                print "wholast"

                        elif command == "broadcast":
                                if commands[1] == "user":
                                        for command in commands:
                                                if users.has_key(command):
                                                        # broadcast to specific users
                                                        broadcastTo.append(command)
                                elif commands[1] == "message":
                                        # broadcast to all

                                        #create message
                                        msg = str(uname + ": ")
                                        for x in range(2, len(commands)):
                                                msg += commands[x] + " "

                                        for user in activeUsers:
                                                # user[0].send(str.encode(msg))
                                                temp = activeUsers[user]
                                                temp[0].send(str.encode(msg))
                        elif command == "message":
                                print "message"
                        elif command == "logout":
                                del activeUsers[uname]
                                conn.send(str.encode("LOGOUT"))
                                thread.exit()


                        # elif command == wholast <time in minutes between 0-60>

                        else:
                                conn.send(str.encode("Error: %s is not a valid command" % command))

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
activeUsers = {}

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server.setblocking(0)

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
