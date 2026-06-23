import socket
import threading

HOST = "0.0.0.0"
PORT = 5555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []

def broadcast(message):
    for client in clients:
        try:
            client.send(message)
        except:
            pass

def handle(client):
    while True:
        try:
            msg = client.recv(1024)
            broadcast(msg)
        except:
            if client in clients:
                clients.remove(client)
            client.close()
            break

print(f"Server running on port {PORT}")

while True:
    client, addr = server.accept()
    clients.append(client)

    thread = threading.Thread(target=handle, args=(client,))
    thread.start()