import socket
import threading
import sys


class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.clients = []
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen()

    def start(self):
        print(f"Server listening on {self.host}:{self.port}")
        while True:
            conn, addr = self.server_socket.accept()
            print(f"Client {addr[0]}:{addr[1]} connected!")
            client_thread = ClientThread(conn, addr, self)
            client_thread.start()
            self.clients.append(client_thread)

    def broadcast(self, message, sender=None):
        for client in self.clients:
            if client != sender:
                client.send(message)


class ClientThread(threading.Thread):
    def __init__(self, conn, addr, server):
        threading.Thread.__init__(self)
        self.conn = conn
        self.addr = addr
        self.server = server

    def run(self):
        username = self.receive()
        print(f"{self.addr[0]}:{self.addr[1]} set username to {username}")
        self.username = username
        self.server.broadcast(f"Server: {username} joined the chat\n")

        while True:
            try:
                message = self.receive()
                if message:
                    print(f"{self.addr[0]}:{self.addr[1]} ({self.username}): {message}")
                    self.server.broadcast(f"{self.username}: {message}\n", sender=self)
                else:
                    self.conn.close()
                    self.server.clients.remove(self)
                    self.server.broadcast(f"Server: {self.username} left the chat\n")
                    return
            except:
                print(f"Error receiving message from {self.addr[0]}:{self.addr[1]}")
                return

    def receive(self):
        try:
            message = self.conn.recv(1024).decode("utf-8")
            return message.strip()
        except:
            return ""

    def send(self, message):
        try:
            self.conn.sendall(message.encode("utf-8"))
        except:
            print(f"Error sending message to {self.addr[0]}:{self.addr[1]}")


if __name__ == "__main__":
    host = "localhost"
    port = 5000
    server = Server(host, port)
    try:
        server.start()
    except KeyboardInterrupt:
        print("Server stopped")
        sys.exit(0)
