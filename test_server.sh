#!/bin/bash

port=$RANDOM

osascript -e 'tell app "Terminal"
    do script with command "python ~/code/pychat/server.py '$port'" in window 1
end tell'

sleep .1
python client.py $port
