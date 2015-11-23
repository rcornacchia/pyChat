#Chat Room

This is a chat room built in python.
Project for CS4119 Computer Networks


2 programs:
-server.py
-client.py

In order to run:

001   Run server.py first
        python server.py <port #>

002   Now run client.py
        python client.py



TEST


##server.py:

001    Reads list of username-password combinations from "user_pass.txt"
002    Listens on given port/waits for clients to connect
003    When client requests connection, server asks for username & password
004    If combination is correct, client logs in + display welcome message
       If combination is incorrect, allow 2 more failures (the number of failures should be mutable)
       If combination is still incorrect after 3 failures, block access for that specific user from the failed IP address
          for 60 seconds (60 seconds should be stored in variable "BLOCK_TIME" so that it can be easily changed)
005    After the user is logged in, the server should be able to recognize + respond to specific user commands.
        If the server cannot recognize some command, an error message should be displayed.



##Commands:

whoelse                                 Displays name of other connected users
wholasthr, wholastmin                   Displays name of only those users that connected within the last hour or minute
broadcast<message>                      Broadcasts <message> to all connected users
broadcast<user><user><user><message>    Broadcasts <message> to list of users
message <user> <message>                Private <message> to a <user>
logout                                  Log out this user.
wholast <time in minutes between 0-60>  Displays name of those users connected within the last x minutes


client.py:

001     When
 

TODO
test on clic server with appropriate python version
