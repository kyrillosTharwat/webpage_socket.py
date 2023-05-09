import socket
import threading
import sys


class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.username = None
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.socket.connect((self.host, self.port))
        print(f"Connected to {self.host}:{self.port}")
        self.username = input("Enter username: ")
        self.socket.sendall(self.username.encode("utf-8"))

    def receive(self):
        while True:
            try:
                message = self.socket.recv(1024).decode("utf-8")
                print(message, end="")
            except:
                print("Error receiving message")
                self.disconnect()
                return

    def send(self, message):
        try:
            self.socket.sendall(message.encode("utf-8"))
        except:
            print("Error sending message")
            self.disconnect()

    def disconnect(self):
        try:
            self.socket.close()
            sys.exit(0)
        except:
            pass


if __name__ == "__main__":
    host = "localhost"
    port = 5000
    client = Client(host, port)
    client.connect()

    receive_thread = threading.Thread(target=client.receive)
    receive_thread.start()

    while True:
        try:
            message = input("")
            client.send(message)
        except KeyboardInterrupt:
            print("Disconnecting...")
            client.disconnect()
            sys.exit(0)
