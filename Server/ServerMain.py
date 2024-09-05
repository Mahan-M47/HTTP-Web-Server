import socket
import threading

HOST = '127.0.0.1'
PORT = 3000

HTML_WEBPAGE_PATH = "webpage.html"
HTML_404_PATH = 'notfound.html'

STATUS_200 = "HTTP/1.1 200 OK"
STATUS_404 = "HTTP/1.1 404 Not Found"


def generate_GET_response(path):
    path = HTML_WEBPAGE_PATH if path == '' else path
    response_headers = ""

    # Open and read the requested HTML file
    try:
        file = open(path, 'r')
        print("Requested file found - Status Code 200")
        response_body = file.read()
        response_headers += STATUS_200

    except FileNotFoundError:
        file = open(HTML_404_PATH, 'r')
        print("Requested file not found - Status Code 404")
        response_body = file.read()
        response_headers += STATUS_404

    response_headers += f"\nContent-Type: text/html\nContent-Length: {len(response_body)}\n\n"
    return response_headers + response_body


def handle_client(client_socket, address):
    print(f"Connected to {address}")

    request_data = client_socket.recv(1024).decode()
    print(f"Received request from {address}")
    print("\n---------------HTTP REQUEST---------------\n" + request_data)

    # Extract the file path from the request
    request_lines = request_data.split('\n')
    request_type = request_lines[0].split()[0]
    path = request_lines[0].split()[1].replace('/', '', 1)

    print(f"Request Type: {request_type} - Path: {path}")

    # Send a response to the client
    response = generate_GET_response(path)
    print(f"Sending response to {address}")
    client_socket.sendall(response.encode())

    print(f"Connection with {address} closed.")
    client_socket.close()


def main():
    # Create a server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))

    # Listen for incoming connections and create a new thread for each client
    print(f"Server listening on http://{HOST}:{PORT}")
    server_socket.listen(10)

    try:
        while True:
            client_socket, address = server_socket.accept()
            client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
            client_thread.start()
    finally:
        print("Server shutting down...")
        server_socket.close()


if __name__ == "__main__":
    main()
