# Robert Cornacchia
# rlc2160
# Python multithreading server

import socket
import sys
import time
import thread
import signal
import errno

def authenticateClient(conn, addr):
    print "Client connected: " + addr[0] + " : " + str(addr[1])
    # Ask client for username
    conn.send(str.encode("Username:").strip())

    # Check if user is blocked
    if addr[0] in blockedClients:
        # Check how long since the user has been blocked
        now = time.time()
        timeBlocked = blockedClients[addr[0]]
        if timeBlocked - time <= BLOCK_TIME:
            # User is still blocked
            conn.send("You are currently blocked\n")
        else:
            del blockedClients[addr[0]]
    uname = ""
    recvdUsername = False
    recvdPass = False
    loggedIn = False
    # Number of failures the client is allowed to make logging in
    numFailures = 0

    timeSinceLastMessage[conn] = time.time()

    while 1:
        data = conn.recv(1024)
        # print "\n DATA RECEIVED " + data + " END TRANSMISSION\n"
        if not data:
            break
        else:
            data = str(data)
            timeSinceLastMessage[conn] = timeSinceLastMessage[conn] = time.time()
            if numFailures >= 3:
                # TODO drop connection and Block user for BLOCK_TIME
                # Drop connection
                conn.send(str.encode("Incorrect Password. YOU HAVE NO ATTEMPTS LEFT! YOU WILL BE DROPPED!!!!"))
                blockedClients[addr[0]] = time.time()
                conn.close()
                del clients[conn]

                thread.exit()

                conn.send(str.encode("Incorrect Password. YOU HAVE NO ATTEMPTS LEFT! YOU WILL BE DROPPED!!!!"))
            elif data == "SHUT_DOWN":
                conn.close()
                print addr[0] + " : " + str(addr[1]) + " Shut Down"
                thread.exit()
            elif recvdUsername == False:
                # incoming data is username
                uname = data
                conn.send(str.encode("Password:").strip())
                recvdUsername = True
            else:
                # incoming data is password
                password = data
                recvdUsername = False
                if uname in activeUsers:
                    # User already logged in
                    # Not counted as a failure
                    msg = data + " is already logged in.\nEnter different username\nUsername: "
                    conn.send(str.encode(msg))
                    # conn.send(str.encode("Username:").strip())
                elif uname not in users.keys():
                    # Username does not exist in text file
                    conn.send(str.encode("User: " + uname + " does not exist\nUsername: "))
                    numFailures += 1
                elif password != str(users.get(uname)):
                    # Password incorrect
                    msg = "Incorrect Password\nYou have " + str(3-numFailures) + " attempts left\nUsername: "
                    conn.send(str.encode(msg))
                    numFailures += 1
                else:
                    # Password correct, log in user
                    conn.send(str.encode("You have logged in. Welcome!"))
                    # Move client from clients dict to activeUsers dict
                    del clients[conn]
                    activeUsers[uname] = [conn, addr]
                    # print "\nCURENTLY ACTIVE USERS"
                    # print activeUsers.keys()
                    handleUser(conn, addr, uname)

def handleUser(conn, addr, uname):
    while 1:
        # Broadcast user has logged in
        data = conn.recv(1024)
        data = str(data)
        if not data:
            # print "Broken pipe"
            # if len(activeUsers) is not 0:
            #         for client in activeUsers:
            #                 msg = "SERVER_SHUTDOWN"
            #                 activeUsers[client][0].send(str.encode(msg))
            #                 print "User: %s has been logged out" % client
            # # For clients that logged in yet
            # for client in clients:
            #         msg = "SERVER_SHUTDOWN"
            #         client.send(str.encode(msg))
            # conn.close()
            # sys.exit()
            break
        else:
            timeSinceLastMessage[conn] = time.time()
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
                durationInMinutes = commands[1]
                # convert duration to seconds
                duration = durationInMinutes * 60

                recentlyActive = []

                if len(commands) != 2:
                        msg = "\nIncorrect usage of wholast\n"
                        msg = "Correct usage is wholast <number>\n"
                        conn.send(msg)
                # 0 < number < 60
                # use timestamp and function that iterates through activeUsers and duration they logged in
                else:
                    now = time.time()
                    for client in activeUsers:
                        recentlyActive.append(str(client))
                    for client in logoutRecord:
                        diff = now - logoutRecord[client]
                        if diff <= duration and client not in recentlyActive:
                            recentlyActive.append(client)
                    if len(recentlyActive) == 0:
                        conn.send(str.encode("No one else has been active in the past " + durationInMinutes + " minutes."))
                    else:
                        msg = ""
                        for name in recentlyActive:
                            if name is not uname:
                                msg += str(name) + "\n"
                        conn.send(str.encode(msg).strip())
            elif command == "broadcast":
                if commands[1] == "user":           # broadcast to specific user set
                    msg = "\n" + uname + ": "
                    doneAddingUsers = False
                    for i in range(2, len(commands)):    # check data for list of users
                        # print command
                        word = commands[i]
                        if word in activeUsers and doneAddingUsers == False:
                            # if user active, add to list
                            # broadcast to specific users
                            broadcastTo.append(word)
                        else:           # notice when done adding users and change boolean
                            doneAddingUsers = True
                        # Now add all words to msg string. Even if the message includes another user's name
                        # it will be added to the broadcast message.
                        if doneAddingUsers is True:
                            # No more users, now check for message
                            msg += word + " "

                    msg += "\n"
                    if len(broadcastTo) > 0:
                        for person in broadcastTo:
                            print broadcastTo
                            activeUsers[person][0].send(str.encode(msg))
                    else:
                        msg = "\nIncorrect usage of broadcast, add a message after listing users.\n"
                        conn.send(str.encode(msg))
                elif commands[1] == "message":      # broadcast to all
                    # create message
                    msg = str("\n" + uname + ": ")
                    for x in range(2, len(commands)):
                        msg += commands[x] + " "
                    msg += "\n"
                    for user in activeUsers:
                        # user[0].send(str.encode(msg))
                        if user is not uname:
                            activeUsers[user][0].send(str.encode(msg))
                else:
                    msg = "\nIncorrect use of broadcast\n"
                    msg = msg + "broadcast to all = broadcast message 'message'\n"
                    msg = msg + "broadcast to specific users = broadcast user user 'message'\n"
                    msg = msg + "You can add as many users as you want, as long as they are active\n"
                    msg = msg + "and as long as there is at least one user\n"
                    conn.send(str.encode(msg))
            elif command == "message":
                # create message for specific user
                msg = str(uname + ": ")
                for x in range(2, len(commands)):
                    msg += commands[x] + " "
                msg += "\n"
                target = commands[1]
                if target in activeUsers:
                    activeUsers[target][0].send(str.encode(msg))
                else:
                    conn.send(str.encode(target + " is not logged in currently."))
            elif command == "logout":
                del activeUsers[uname]
                logoutRecord[uname] = time.time()
                conn.send(str.encode("LOGOUT"))
                thread.exit()
            elif command == "SHUT_DOWN":
                del activeUsers[uname]
                logoutRecord[uname] = time.time()
                print "User: " + uname + " at " + addr[0] + " : " + str(addr[1]) + " Shut Down"
                thread.exit()
            else:
                conn.send(str.encode("Error: %s is not a valid command\nEnter 'help' for a list of valid commands" % command))

def monitorActivity(a, b):
    while 1:
        removable = []
        if len(timeSinceLastMessage) is not 0:
            for i in range(0, len(timeSinceLastMessage)):
                # Get time since last message
                diff = time.time() - timeSinceLastMessage.values()[i]
                # Check if time since last message is greater than 30 minutes
                if diff > 1800:
                    inactiveClient = timeSinceLastMessage.keys()[i]
                    print inactiveClient + " has been logged out due to inactivity"
                    inactiveClient.send(str.encode("INACTIVE"))
                    inactiveClient.close()
                    removable.append(inactiveClient)
                    # inactiveClient = timeSinceLastMessage.keys()[i]
                    if inactiveClient in activeUsers:
                        del activeUsers[inactiveClient]
                        logoutRecord[inactiveClient] = time.time()
                    else:
                        del clients[inactiveClient]
        for client in removable:
            del timeSinceLastMessage[client]

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
                # print "errno is %d" % e[0]
                if e[0] == errno.EPIPE:
                    # remote peer disconnected
                    print "Detected remote disconnect from client"
                else:
                    # determine and handle different error
                    pass
            else:
                print "socket error ", e
                conn.close()
                break
        except IOError, e:
            print "IOError:, ", e
            break
        else:
            conn.close()
            sys.exit(0)
        conn.close()
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

BLOCK_TIME = 60

# Create a dict of all users that are logged in
activeUsers = {}
# Create a dict of all clients, that maintains the socket until they log in
clients = {}
# Create a dict to record when a client logs out. Key = username, value = time Logged out (for wholast)
logoutRecord = {}
# Dictionary that records activity. Key = clientSocket, Value = time of last message
timeSinceLastMessage = {}
# Dictionary that records blocked users and time they are blocked. Key = IP addr, Value = time blocked
blockedClients = {}


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server.setblocking(0)

a = 0
b = 0

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

thread.start_new_thread(monitorActivity, (a, b))

while 1:
    # accept new client
    try:
        conn, addr = server.accept()
    except:
        sys.exit()
    # Add client to list of clients
    clients[conn] = addr
    # Spawn a new thread to handle client
    thread.start_new_thread(authenticateClient, (conn, addr))

server.close()
