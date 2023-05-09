import socket
import tkinter as tk
from tkinter import filedialog


class GUI:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = socket.gethostname()
        port = 12321
        self.s.bind((host, port))
        print('server started')

        self.root = tk.Tk()
        self.root.title("Transfer Files - Sender")
        self.root.geometry("400x170")
        self.root.minsize(300, 160)

        self.send_button = tk.Button(self.root, text="Select & Send", font=("Helvetica", 16), bg="#800080", fg="white",
                                     padx=10,
                                     pady=5, command=self.select_file)
        self.send_button.pack(padx=8, pady=44)

    def build(self):
        self.root.mainloop()

    def select_file(self):
        file_path = filedialog.askopenfilename(initialdir="./", title="Select File")
        # self.status_label.text = 'You sending : ' + file_path
        print(f' You sending : {file_path}')
        self.send_file(file_path)

    def send_file(self, file_path):
        self.s.listen()
        client_socket, address = self.s.accept()
        file_name = file_path.split('/')[-1]
        client_socket.send(file_name.encode('utf-8'))
        file = open(file_path, "rb")
        data = file.read(2048)
        while data:
            client_socket.send(data)
            data = file.read(2048)
        file.close()
        client_socket.close()
        # self.status_label.text = 'File ' + file_name + ' sent'
        print(f' File {file_name} sent ')


if __name__ == "__main__":
    GUI().build()
