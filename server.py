# Robert Cornacchia
# rlc2160
# Python multithreading server


import  socket,
        sys,
        time,
        thread,
        signal

def authenticateClient(conn, addr):
        print "Client connected: " + addr[0] + " : " + str(addr[1])

        # Ask client for username
        conn.send(str.encode("Username:").strip())

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
                                        conn.send(str.encode("You have logged in. Welcome!"))
                                        # Remove client from clients dict
                                        del clients[conn]
                                        # Add user to activeUsers
                                        activeUsers[uname] = [conn, addr]
                                        print "\nCURENTLY ACTIVE USERS"
                                        print activeUsers.keys()
                                        handleUser(conn, addr, uname)
                                elif loginAttempt < 2:
                                        print "BAD LOGIN ATTEMPT"
                                        loginAttempt += 1
                                        conn.send(str.encode("Incorrect Password\nYou have " + str(3-loginAttempt) + " attempts left\nRe-enter password"))
                                else:
                                        conn.send(str.encode("Incorrect Password. YOU HAVE NO ATTEMPTS LEFT! YOU WILL BE DROPPED!!!!"))
                                        # TODO drop connection and Block user for BLOCK_TIME

                        if recvdCorrectName == False and users.has_key(data):     # Check if username exists
                                if data in activeUsers:
                                        conn.send(str.encode(str(data) + " is already logged in.\nEnter different username"))
                                else:
                                        uname = data
                                        recvdCorrectName = True
                                        conn.send(str.encode("Password:").strip())
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
                                # get number: commands[1]
                                # 0 < number < 60
                                # use timestamp and function that iterates through activeUsers and time they logged in
                                print "wholast"
                        elif command == "broadcast":
                                if commands[1] == "user":           # broadcast to specific user set
                                        msg = uname + ": "
                                        doneAddingUsers = False
                                        for i in range(2, len(commands)):    # check data for list of users
                                                # print command
                                                word = commands[i]
                                                if word in activeUsers and doneAddingUsers == False:
                                                        # if user, add to list
                                                        # broadcast to specific users
                                                        print word
                                                        broadcastTo.append(word)
                                                else:           # notice when done adding users and change boolean
                                                    doneAddingUsers = True
                                                # Now add all words to msg string. Even if the message includes another user's name
                                                # it will be added to the broadcast message.
                                                if doneAddingUsers is True:
                                                        # No more users, now check for message
                                                        msg += word + " "

                                        if len(broadcastTo) > 0:
                                                for person in broadcastTo:
                                                        print broadcastTo
                                                        activeUsers[person][0].send(str.encode(msg))
                                        else:
                                                msg = "Incorrect usage of broadcast, add a message after listing users\n"
                                                conn.send(str.encode(msg))
                                elif commands[1] == "message":      # broadcast to all
                                        # create message
                                        msg = str(uname + ": ")
                                        for x in range(2, len(commands)):
                                                msg += commands[x] + " "

                                        for user in activeUsers:
                                                # user[0].send(str.encode(msg))
                                                if user is not uname:
                                                        activeUsers[user][0].send(str.encode(msg))
                                else:
                                        msg = "Incorrect use of broadcast\n"
                                        msg = msg + "broadcast to all = broadcast message 'message'\n"
                                        msg = msg + "broadcast to specific users = broadcast user user 'message'\n"
                                        msg = msg + "You can add as many users as you want, as long as they are active\n"
                                        msg = msg + "and as long as their is at least one user"
                                        conn.send(str.encode(msg))
                        elif command == "message":
                                # create message for specific user
                                msg = str(uname + ": ")
                                for x in range(2, len(commands)):
                                        msg += commands[x] + " "
                                target = commands[1]
                                if target in activeUsers:
                                        activeUsers[target][0].send(str.encode(msg))
                                else:
                                        conn.send(str.encode(target + " is not logged in currently."))
                        elif command == "logout":
                                del activeUsers[uname]
                                conn.send(str.encode("LOGOUT"))
                                thread.exit()
                        elif command == "SHUT_DOWN":
                                del activeUsers[uname]
                                thread.exit()
                        else:
                                conn.send(str.encode("Error: %s is not a valid command\nEnter 'help' for a list of valid commands" % command))

#signal handling
def signal_handler(signal, frame):
        print '\nYou pressed Ctrl+C!\nServer Shutting Down\n'
        if len(activeUsers) is not 0:
                for client in activeUsers:
                        msg = "SERVER_SHUTDOWN"
                        activeUsers[client][0].send(str.encode(msg))
                        print "User: %s has been logged out" % client
        # For clients that logged in yet
        for client in clients:
                msg = "SERVER_SHUTDOWN"
                try:
                        client.send(str.encode(msg))
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
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

if not sys.argv[1]:
        print "Incorrect usage"

# Read list of username-password combinations
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
clients = {}

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
        # accept new client
        conn, addr = server.accept()
        # Add client to list of clients
        clients[conn] = addr
        # Spawn a new thread to handle client
        thread.start_new_thread(authenticateClient, (conn, addr))

server.close()
