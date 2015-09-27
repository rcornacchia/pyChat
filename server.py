import socket
import sys


def initializeServer():
    # Create socket
    s = socket.socket()
    host = socket.gethostname()
    port = int(sys.argv[1])
    print port
    s.bind((host, port))

    s.listen(5)
    while True:
        c, addr = s.accept()
        print 'Connection received from', addr

        #authenticate user
        c.send("What is your username")
        data = c.recv(1024)
        if data is not None:
            print data




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
