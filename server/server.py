import socket
from .request import Request
from .response import Response

class Server:
    """
    A simple HTTP server that accepts TCP connections, parses HTTP requests,
    and sends back HTTP responses.

    Attributes:
        host (str): The host/IP address the server will bind to. Defaults to "127.0.0.1".
        port (int): The TCP port the server will listen on. Defaults to 8080.
        socket (socket.socket | None): The underlying server socket, initialized in `start()`.

    Methods:
        start():
            Creates a socket, binds to (host, port), listens for incoming connections,
            and handles them sequentially.
        
        handle_client(client_connection):
            Reads raw request data from a client socket, parses it into a `Request`,
            builds a `Response`, and sends it back. Closes the client connection
            when finished. Sends a `500 Internal Server Error` if any exception occurs.
    """
        
    def __init__(self, host = "127.0.0.1", port = 8080, router = None):
        self.host = host
        self.port = port
        self.socket = None
        self.router = router


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
            
            if self.router:
                response = self.router.resolve(request)
            else:
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