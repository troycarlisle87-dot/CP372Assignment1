import socket
import os

HOST = "127.0.0.1"
PORT = 5000
BUFFER_SIZE = 1024

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client_socket.connect((HOST, PORT))

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

        # FILE command handling
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

            print(f"Sending file command: {file_command}")

            client_socket.sendall((file_command + "\n").encode())

            response = client_socket.recv(BUFFER_SIZE).decode()
            print(f"Server says: {response}")

            continue

        # Normal command handling for LOGIN, MSG, and QUIT
        client_socket.sendall((message + "\n").encode())

        response = client_socket.recv(BUFFER_SIZE).decode()

        if response == "":
            print("Server disconnected.")
            break

        print(f"Server says: {response}")

        if command == "QUIT":
            break

except ConnectionRefusedError:
    print("Error: server unavailable. Make sure server.py is running first.")

except ConnectionResetError:
    print("Error: connection was reset by the server.")

except KeyboardInterrupt:
    print("\nClient manually terminated.")

finally:
    client_socket.close()
    print("Client closed.")