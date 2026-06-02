import socket
import os

# Constants
HOST = "127.0.0.1"  # Randomly Chosen
PORT = 5000  # Clean number no chance of accidents
BUFFER_SIZE = 1024  # 2 power 10


# Reads one full response from the server
def receive_response(client_socket):
    data = b""

    while True:
        chunk = client_socket.recv(1)

        if not chunk:
            return None

        data += chunk

        # Server responses are normal text so this catches the end if newline is used
        # Also works fine for short simple responses
        if chunk == b"\n":
            break

        # Failsafe so the client does not wait forever on older responses without newline
        if len(data) >= BUFFER_SIZE:
            break

    return data.decode().strip()


# Sends one command to the server with a newline
def send_command(client_socket, message):
    client_socket.sendall((message + "\n").encode())


# Sends raw file bytes after the server says it is ready
def send_file_bytes(client_socket, filepath):
    with open(filepath, "rb") as file:
        while True:
            chunk = file.read(BUFFER_SIZE)

            if not chunk:
                break

            client_socket.sendall(chunk)


# How you set this up inside of the assignments packet
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Failsafe
try:
    # Actual linking stolen from the slides
    client_socket.connect((HOST, PORT))

    # Rubber Duck
    print("Connected to server.")
    print("Type commands to send to the server.")
    print("Available commands:")
    print("LOGIN username")
    print("MSG message")
    print("FILE filepath")
    print("QUIT")
    print()

    while True:
        message = input("> ").strip()

        if message == "":
            print("Error: empty input. Please type a command.")
            continue

        parts = message.split(" ", 1)
        command = parts[0].upper()

        # FILE Command
        if command == "FILE":
            if len(parts) < 2 or parts[1].strip() == "":
                print("Error: FILE requires a filepath.")
                continue

            filepath = parts[1].strip()

            if not os.path.exists(filepath):
                print("Error: file does not exist.")
                continue

            if not os.path.isfile(filepath):
                print("Error: path is not a file.")
                continue

            filesize = os.path.getsize(filepath)

            if filesize == 0:
                print("Error: cannot send an empty file.")
                continue

            filename = os.path.basename(filepath)
            file_command = f"FILE {filename} {filesize}"

            # Confirmation pleasentires
            print(f"Sending file command: {file_command}")

            # First send the file command, not the actual bytes yet
            send_command(client_socket, file_command)

            # Wait until the server says it is ready
            response = client_socket.recv(BUFFER_SIZE).decode()
            print(f"Server says: {response}")

            if response != "OK Ready to receive file":
                continue

            # Actual file sending part
            send_file_bytes(client_socket, filepath)

            # Final response after the server saves the file
            final_response = client_socket.recv(BUFFER_SIZE).decode()
            print(f"Server says: {final_response}")
            continue

        # Normal command handling for LOGIN, MSG, and QUIT
        send_command(client_socket, message)

        response = client_socket.recv(BUFFER_SIZE).decode()

        if response == "":
            print("Server disconnected.")
            break

        print(f"Server says: {response}")

        # Quit handler
        if command == "QUIT":
            break

except ConnectionRefusedError:
    print("Error: server unavailable. Make sure server.py is running first.")

except ConnectionResetError:
    print("Error: connection was reset by the server.")

except KeyboardInterrupt:
    print("\nClient manually terminated.")

except Exception as error:
    print(f"Client error: {error}")

finally:
    client_socket.close()
    print("Client closed.")