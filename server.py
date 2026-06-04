import socket
import os

#All code completed in this document is done by that of a group collective
#All of our ideas and logic are our own, no other students current or previous work
#Was used to create this document 
# Constants
HOST = "127.0.0.1"  # Randomly Chosen
PORT = 5000  # Clean number no chance of accidents
BUFFER_SIZE = 1024  # 2 power 10
USERS_FILE = "users.txt"  # Name of the file
SERVER_FILES_DIR = "server_files"  # Folder where received files get saved


# Self explanitory
def load_users():
    valid_users = set()

    try:
        with open(USERS_FILE, "r") as file:
            for line in file:
                username = line.strip()

                if username != "":
                    valid_users.add(username)

    except FileNotFoundError:
        print(f"Error: {USERS_FILE} was not found.")

    return valid_users


# Reads one full command until it hits a newline
def receive_command(conn):
    data = b""

    while True:
        chunk = conn.recv(1)

        if not chunk:
            return None

        data += chunk

        if chunk == b"\n":
            break

    return data.decode().strip()


# Receives the exact file size instead of guessing with one recv
def receive_exact_bytes(conn, filesize):
    file_data = b""

    while len(file_data) < filesize:
        bytes_left = filesize - len(file_data)
        chunk = conn.recv(min(BUFFER_SIZE, bytes_left))

        if not chunk:
            return None

        file_data += chunk

    return file_data


# Stops sneaky path stuff 
def safe_filename(filename):
    return os.path.basename(filename)


# Hardcoded valid logins taken from txt file
valid_users = load_users()
print(f"loaded users: {valid_users}")

# Does the folder really exists budyd?
os.makedirs(SERVER_FILES_DIR, exist_ok=True)

# How you set this up inside of the assignments packet
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Actual linking stolen from the slides
server_socket.bind((HOST, PORT))
server_socket.listen(1)

# Rubber Duck emthod
print(f"Server listening on {HOST}:{PORT}")

# Failsafe
try:
    while True:
        print("Waiting for a client...")

        # Client package
        conn, addr = server_socket.accept()
        print(f"Client connected from {addr}")

        logged_in = False
        current_user = None

        try:
            while True:
                message = receive_command(conn)
                #Just some more error handling pretty forwars
                if message is None:
                    print("Client disconnected unexpectedly.")
                    break

                if message == "":
                    print("Empty message received.")
                    conn.sendall("ERROR Empty message".encode())
                    continue

                # Response message or termination notice
                # Gonna be alot
                print(f"Client says: {message}")

                parts = message.split(" ", 1)
                command = parts[0].upper()

                if command == "LOGIN":
                    if len(parts) < 2 or parts[1].strip() == "":
                        conn.sendall("ERROR LOGIN requires a username".encode())
                        continue

                    username = parts[1].strip()

                    if username in valid_users:
                        logged_in = True
                        current_user = username
                        conn.sendall(f"OK Logged in as {username}".encode())

                        print(f"User logged in: {username}")
                        continue

                    else:
                        conn.sendall("ERROR Invalid username".encode())
                        print(f"Invalid login attempt: {username}")
                        continue

                # Message handler
                elif command == "MSG":
                    if not logged_in:
                        conn.sendall("ERROR You must LOGIN before sending messages".encode())
                        continue

                    if len(parts) < 2 or parts[1].strip() == "":
                        conn.sendall("ERROR MSG requires message text".encode())
                        continue

                    message_text = parts[1].strip()
                    print(f"Message from {current_user}: {message_text}")
                    conn.sendall("OK Message received by server".encode())
                    continue

                # FILE handler
                elif command == "FILE":
                    if not logged_in:
                        conn.sendall("ERROR You must LOGIN before sending files".encode())
                        continue

                    file_parts = message.split(" ")

                    if len(file_parts) != 3:
                        conn.sendall("ERROR FILE format must be: FILE filename filesize".encode())
                        continue

                    filename = safe_filename(file_parts[1])

                    try:
                        filesize = int(file_parts[2])

                    except ValueError:
                        conn.sendall("ERROR File size must be a number".encode())
                        continue

                    if filesize <= 0:
                        conn.sendall("ERROR File size must be greater than zero".encode())
                        continue

                    # Confirmation pleasentires
                    print(f"File command received from {current_user}: {filename} ({filesize} bytes)")

                    # This tells the client the server is ready to take its load
                    conn.sendall("OK Ready to receive file".encode())

                    # Actual file receiving part
                    file_data = receive_exact_bytes(conn, filesize)

                    if file_data is None:
                        print("File transfer failed because the client disconnected.")
                        break

                    save_path = os.path.join(SERVER_FILES_DIR, filename)

                    try:
                        with open(save_path, "wb") as file:
                            file.write(file_data)

                    except OSError as error:
                        conn.sendall(f"ERROR Could not save file: {error}".encode())
                        print(f"File save error: {error}")
                        continue

                    print(f"File received from {current_user}: {filename} ({filesize} bytes)")
                    print(f"Saved to: {save_path}")

                    conn.sendall(f"OK File received: {filename}".encode())
                    continue

                # Quit handler
                elif command == "QUIT":
                    conn.sendall("OK Goodbye".encode())
                    print("Client requested disconnect.")
                    break

                # failsafe catch all because I am lazy 
                else:
                    conn.sendall("ERROR Invalid command".encode())
                    continue

        except ConnectionResetError:
            print("Error: client connection was reset.")

        except Exception as error:
            print(f"Server error: {error}")

        finally:
            conn.close()
            print("Client disconnected.")
            print()

except KeyboardInterrupt:
    print("\nServer manually terminated.")

finally:
    server_socket.close()
    print("Server socket closed.")