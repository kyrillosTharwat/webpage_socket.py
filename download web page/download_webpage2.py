import socket
import tkinter as tk


class PageDownloader:

    def __init__(self, url):
        self.url = url
        self.host = url.split('/')[2]
        self.response = ''

    def download(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.host, 80))
        print(f'connected to {self.host}')
        request = f'GET/HTTP/1.1\r\nHost:{self.host}\r\n\r\n'
        s.send(request.encode())
        print('downloading..')
        while True:
            data = s.recv(4096).decode('utf-8')
            if not data:
                break
            self.response += data
        print('downloaded !')
        s.close()

    def save_file(self):
        try:
            file = f"{self.host}.html"
            with open(file, "w", encoding="utf-8") as file:
                content = self.response.split('\r\n\r\n')[1]
                file.write(content)
            print('File saved successfully ')
        except Exception as e:
            print(f"Error: {e}")


class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Download Web Page")
        self.root.geometry("400x170")
        self.root.minsize(300, 160)

        url_label = tk.Label(self.root, text="Enter URL:", font=("Helvetica", 16), fg='purple')
        url_label.pack(padx=8, pady=8, side=tk.TOP, anchor=tk.W)

        self.url_entry = tk.Entry(self.root, font=("Helvetica", 14))
        self.url_entry.pack(padx=8, pady=8, side=tk.TOP, fill=tk.X)

        # Set the text style for the entry widget
        self.url_entry.insert(0, "Insert URL here")
        self.url_entry.config(fg='grey')

        download_button = tk.Button(self.root, text="Download Me", font=("Helvetica", 16), bg="#800080", fg="white",
                                    padx=10,
                                    pady=5, command=self.download)
        download_button.pack(padx=8, pady=8, side=tk.BOTTOM, anchor=tk.CENTER)
        self.root.eval('tk::PlaceWindow . center')

    def build(self):
        self.root.mainloop()

    def download(self):
        downloader = PageDownloader(self.url_entry.get())
        downloader.download()
        downloader.save_file()


if __name__ == "__main__":
    GUI().build()
