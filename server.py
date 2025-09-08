import socket
from request import Request
from response import Response

class Server:
    def __init__(self, host = "127.0.0.1", port = 8080):
        self.host = host
        self.port = port
        self.socket = None


    def start(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)
        print(f"Server running on http://{self.host}:{self.port}")

        while True:
            client_connection, client_address = self.socket.accept()
            print(f"New connection from {client_address}")
            self.handle_client(client_connection)

    def handle_client(self, client_connection):
        try:
            data = client_connection.recv(1024).decode("utf-8")
            if not data:
                return
            
            request = Request(data)
            print("Incoming request:", request)

            response = Response(body="Hello, World!")
            client_connection.sendall(response.convert_to_bytes())

        except Exception as e:
            print("Error handling request:", e)
            error_response = Response(status=500, body="Internal Server Error")
            client_connection.sendall(error_response.convert_to_bytes())

        finally:
            client_connection.close()

if __name__ == "__main__":
    server = Server(host="127.0.0.1", port=8080)
    server.start()