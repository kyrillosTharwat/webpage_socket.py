import socket
import threading


class Client:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = socket.gethostname()
        port = 12321
        self.client.connect((host, port))
        self.username = input('Whats ur username : ')
        self.client.send(self.username.encode('utf-8'))

    def receive(self):
        while True:
            message = self.client.recv(1024).decode('utf-8')
            print(message)

    def typing(self):
        while True:
            msg = f'{self.username}: {input()}'
            self.client.send(msg.encode('utf-8'))

    def start(self):
        typing_thread = threading.Thread(target=self.typing)
        typing_thread.start()
        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()


if __name__ == '__main__':
    Client().start()
