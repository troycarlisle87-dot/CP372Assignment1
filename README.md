CP372 Assignmnet 1 -TCP Client-Server Application

Brief Overview
This project is a TCP application made in python using the socket library. The client connects to the server, logs in with a valid username, sends messages, transfers files, and disconnects using a custom set of commands set by the system. This is meant to mimic the triple handshake method of TCP along with its numerous error handling methods 

Dependencies:

Python 3.x

Libraries used:

socket
os

nothing external nessesary to run

Folder Strucure:

CP372_Assignment1/
│   .gitignore
│   client.py
│   server.py
│   users.txt
│   README.md
│  
│
├───client_files
│       test.txt
│
└───server_files
        test.txt

How to Run:

Start server
python server.py

Start client
python client.py

The program will then prompt you possible commands

Example commands:
LOGIN Alice
MSG Hello World
FILE client_files/test.txt
QUIT

Before any commands can be executed you must login
the system will tell you this if you do not

a list of valid login user names can be found in users.txt. Feel free to change theses names at whim if they are not to your liking

The command structure goes COMMAND (space) Content

Extra comments:
Only one client at a time
The server will continue running after you disconnect if you so choose to start a new session
Files sent by client are in server_files
FIles needing to be send should be placed in client_files
The program handles has error handling for invalid commands, missuing files, empty messages, invalid logins, and agreable disconnects