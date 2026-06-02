import socket
import os
#Constants
HOST = "127.0.0.1" # Randomly Chosen
PORT = 5000 #Clean number no chance of accidents
BUFFER_SIZE= 1024 #2 power 10
USERS_FILE="users.txt" #Name of the file
SERVER_FILES_DIR="server_files"

#Self explanitory
def load_users():
    valid_users = set()

    try:
        with open(USERS_FILE, "r") as file:
            for line in file:
                username = line.strip()

                if username !="":
                    valid_users.add(username)
    except FileNotFoundError:
        print(f"Error: {USERS_FILE} was not found.")
    return valid_users
def receive_command(conn):
    data=b""

    while True:
        chunk = conn.recv(1)

        if not chunk:
            return None
        
        data += chunk

        if chunk == b"\n":
            break

    return data.decode().strip()
#Hardcoded valid logins taken from txt file
valid_users=load_users()
print(f"loaded users: {valid_users}")

#How you set this up inside of the assignments packet
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

#Actual linking stolen from the slides
server_socket.bind((HOST, PORT))
server_socket.listen(1)

#Rubber Duck
print(f"Server listening on {HOST}:{PORT}")

#Failsafe
try:
    while True:
        print("Waiting for a client...")
        
        #Client package
        conn,addr =server_socket.accept()
        print(f"Client connected from {addr}")
        logged_in=False
        current_user=None



        while True:
            message = receive_command(conn)

            if message is None:
                print("Client disconnected.")
                break

            
            if message =="":
                print("Empty message received.")
                conn.sendall("ERROR Empty message".encode())
                continue
            
            #Response message or termination notice
            #Gonna be alot
            print(f"Client says: {message}")
            
            parts = message.split(" ",1)
            command = parts[0].upper()

            if command =="LOGIN":
                if len(parts) < 2 or parts[1].strip()=="":
                    conn.sendall("ERROR LOGIN requires a username".encode())
                    continue
                username = parts[1].strip()
                if username in valid_users:
                    logged_in=True
                    current_user=username
                    conn.sendall(f"OK Logged in as {username}".encode())
                    
                    print(f"User logged in:{username}")
                    continue
                else:
                    conn.sendall("ERROR Invalid username".encode())
                    print(f"Invalid login attempt: {username}")
                    continue
            #Message handler
            elif command =="MSG":
                if not logged_in:
                    conn.sendall("ERROR You must LOGIN before sending messages".encode())
                    continue
                if len(parts) < 2 or parts[1].strip() =="":
                    conn.sendall("ERROR MSG requires message text".encode())
                    continue
                message_text = parts[1].strip()
                print(f"Message from {current_user}: {message_text}")
                conn.sendall("OK Message received by server".encode())
                continue
            #FILE handler
            elif command =="FILE":
                if not logged_in:
                    conn.sendall("ERROR You must LOGIN before sending files".encode())
                    continue

                file_parts=message.split(" ")

                if len(file_parts) !=3:
                    conn.sendall("ERROR FILE format must be: FILE filename filesize".encode())
                    continue 

                filename= file_parts[1]

                try:
                    filesize = int(file_parts[2])
                except ValueError:
                    conn.sendall("ERROR File size must be a number".encode())
                    continue
                
                if filesize <= 0:
                    conn.sendall("ERROR File size must be greater then zero".encode())
                    continue
                
                #Confirmation pleasentires 
                print(f"File command received from {current_user}: {filename} ({filesize} bytes)")
                conn.sendall(f"OK FILE command accepted for {filename}".encode())
                continue




            # Quit handler
            elif command =="QUIT":
                conn.sendall("OK Goodbye".encode())
                print("Client requested disconnect.")
                break
            
            conn.sendall("ERROR Invalid command".encode())

        conn.close()
        print("Client disconnected.")
        print()

except KeyboardInterrupt:
    print("\nServer manually terminated.")

finally:
    server_socket.close()
    print("Server socket closed.")