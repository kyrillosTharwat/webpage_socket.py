import socket

HOST = 'www.google.com'
PORT = 80
PAGE = '/'

# Create a TCP socket and connect to the web server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

# Construct an HTTP GET request for the webpage
request = f'GET {PAGE} HTTP/1.1\r\nHost: {HOST}\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)\r\n\r\n'

# Send the HTTP GET request to the web server
s.sendall(request.encode())

# Receive the HTTP response from the web server
response = b''
while True:
    data = s.recv(1024)
    if not data:
        break
    response += data

# Parse the HTTP response to extract the HTML content of the webpage
html_start = response.find(b'\r\n\r\n') + 4
html = response[html_start:]

# Print the HTML content of the webpage
print(html.decode())

# Close the TCP socket connection
s.close()