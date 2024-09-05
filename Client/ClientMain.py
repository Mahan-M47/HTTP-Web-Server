import socket

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 3000


request_template = """\nConnection: keep-alive
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Accept-Encoding: gzip, deflate, br, zstd
Accept-Language: en-US,en;q=0.9
"""

def generate_GET_request(path):
    request = f"GET /{path} HTTP/1.1" + f"\nHost: {SERVER_HOST}:{SERVER_PORT}" + request_template
    return request

def main():
    while True:
        try:
            # Connect to the server
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((SERVER_HOST, SERVER_PORT))
            print(f"Connected to {SERVER_HOST}:{SERVER_PORT}")

            address = input("Please enter the title of the webpage you wish to access (Leave empty to view the default page): ")

            # Send request to the server
            request = generate_GET_request(address)
            print("Request sent to the server: " + request.split("\n")[0])
            client_socket.sendall(request.encode())

            # Wait to receive a response from the server
            response = b''
            while True:
                packet = client_socket.recv(1024)
                if not packet:
                    break
                response += packet

            print("\n---------------HTTP RESPONSE---------------\n" + response.decode())

            if input("\nConnect again? y/n ") != 'y':
                break

        except ConnectionRefusedError:
            if input("Failed to connect to server. Try again? y/n ") != 'y':
                break

    print("\nClient disconnected.")
    client_socket.close()


if __name__ == "__main__":
    main()