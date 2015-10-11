#!/bin/bash

port=$RANDOM

osascript -e 'tell app "Terminal"
    do script with command "python ~/code/pyChat/server.py '$port'" in window 2
    do script with command "./xtest_client.sh '$port'" in window 3
    do script with command "./xtest_client.sh '$port'" in window 4
end tell'

sleep .1
python client.py 127.0.0.1 $port
