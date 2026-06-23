import socket
import threading
import os

HOST = "0.0.0.0"
PORT = int(os.environ.get("PORT", 5555))

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []

def broadcast(message):
    for client in clients[:]:
        try:
            client.send(message)
        except:
            clients.remove(client)

def handle(client):
    while True:
        try:
            msg = client.recv(1024)
            if not msg:
                break
            broadcast(msg)
        except:
            break

    if client in clients:
        clients.remove(client)

    client.close()

print(f"Server running on port {PORT}")

while True:
    client, addr = server.accept()
    print(f"Connected: {addr}")

    clients.append(client)

    threading.Thread(
        target=handle,
        args=(client,),
        daemon=True
    ).start()