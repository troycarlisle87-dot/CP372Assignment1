import socket

HOST = "127.0.0.1"
PORT = 5000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

print(f"Server listening on {HOST}:{PORT}")

conn, addr = server_socket.accept()
print(f"Client connected from {addr}")

message = conn.recv(1024).decode()
print(f"Client says: {message}")

conn.sendall("Message received by server".encode())

conn.close()
server_socket.close()