import socket
import threading


class Server:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = socket.gethostname()
        port = 12321
        self.s.bind((host, port))
        self.s.listen()
        print('server started')

        self.clients = []
        self.usernames = []

    def sent_to_all(self, message):
        for client in self.clients:
            client.send(message)

    def start(self):
        while True:
            client_socket, client_address = self.s.accept()
            print(f"New client connected: {client_address}")
            username = client_socket.recv(1024).decode('utf8')
            print(f"his username : {username}")
            self.clients.append(client_socket)
            self.usernames.append(username)
            self.sent_to_all(f'{username} joined to room'.encode('utf8'))
            threat = threading.Thread(target=self.handle_client, args=(client_socket,))
            threat.start()

    def handle_client(self, client_socket):
        while True:
            try:
                message = client_socket.recv(1024)
                self.sent_to_all(message)
            except:
                index = self.clients.index(client_socket)
                self.clients.remove(client_socket)
                unused_username = self.usernames[index]
                print(f'{unused_username} left the Chatroom')
                self.usernames.remove(unused_username)
                break


if __name__ == '__main__':
    Server().start()
