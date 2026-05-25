import socket

HOST = "127.0.0.1"
PORT = 5000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

print("Connected to server.")

message = input("Enter a message: ")
client_socket.sendall(message.encode())

response = client_socket.recv(1024).decode()
print(f"Server says: {response}")

client_socket.close()