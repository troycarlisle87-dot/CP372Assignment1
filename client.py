import socket

HOST = "127.0.0.1"
PORT = 5000
BUFFER_SIZE=1024
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

print("Connected to server.")
print("Type messages to send to the server.")
print("Type QUIT to disconnect.")
print()

while True:
    message= input("> ").strip()

    if message =="":
        print("Error: empty input. Please type a message or QUIT.")
        continue
    client_socket.sendall(message.encode())

    response = client_socket.recv(BUFFER_SIZE).decode()
    print(f"Server sayus: {response}")

    if message.upper() =="QUIT":
        break
client_socket.close()
print("client closed")
