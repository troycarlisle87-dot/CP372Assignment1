import socket
#Constants
HOST = "127.0.0.1" # Randomly Chosen
PORT = 5000 #Clean number no chance of accidents
BUFFER_SIZE= 1024 #2 power 10
USERS_FILE="users.txt" #Name of the file

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
            data = conn.recv(BUFFER_SIZE)

            if not data:
                print("Client disconnected.")
                break

            message = data.decode().strip()

            if message =="":
                print("Empty message received.")
                conn.sendall("ERROR Empty message".encode())
                continue
            
            #Response message or termination notice
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
                else:
                    conn.sendall("ERROR Invalid username".encode())
                    print(f"Invalid login attempt: {username}")
                    continue

            elif command =="QUIT":
                conn.sendall("OK Goodbye".encode())
                print("Client requested disconnect.")
                break
            
            conn.sendall("OK Message recieved by server".encode())

        conn.close()
        print("Client disconnected.")
        print()

except KeyboardInterrupt:
    print("\nServer manually terminated.")

finally:
    server_socket.close()
    print("Server socket closed.")