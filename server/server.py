import socket
from .request import Request
from .response import Response
from .static import serve_static
import threading
import multiprocessing
class Server:
    """
    A simple multithreaded HTTP server that accepts TCP connections,
    parses HTTP requests, and sends back HTTP responses.

    Attributes:
        host (str): The host/IP address the server will bind to. Defaults to "127.0.0.1".
        port (int): The TCP port the server will listen on. Defaults to 8080.
        socket (socket.socket | None): The underlying server socket, initialized in `start()`.
        router (Router | None): Optional router instance for handling dynamic routes.

    Methods:
        start():
            Creates a socket, binds to (host, port), and listens for incoming
            connections. Each client connection is handled in a separate
            thread for concurrent request processing.
        
        handle_client(client_connection):
            Runs in its own thread. Reads raw request data from a client socket,
            parses it into a `Request`, and determines the appropriate `Response`:
                - Serves static files if the path starts with "/static/".
                - Uses the configured `Router` if available.
                - Falls back to a "Hello, World!" response if no router is set.
            Sends the response back to the client and closes the connection.
            Returns a `500 Internal Server Error` if any exception occurs.
    """
     
    def __init__(self, host = "127.0.0.1", port = 8080, router = None, mode = "threading"):
        self.host = host
        self.port = port
        self.socket = None
        self.router = router
        self.mode = mode


    def start(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)
        print(f"Server running on http://{self.host}:{self.port}")

        while True:
            client_connection, client_address = self.socket.accept()
            print(f"New connection from {client_address}")

            match self.mode:
                case "sequential":
                    self.handle_client(client_connection)
                
                case "threading":
                    thread = threading.Thread(target=self.handle_client, args=(client_connection,))
                    thread.start()

                case "multiprocessing":
                    process = multiprocessing.Process(target=self.handle_client, args=(client_connection,))
                    process.start()
                
                case _:
                    raise ValueError(f"Unknown mode: {self.mode}")

    def handle_client(self, client_connection):
        try:
            data = client_connection.recv(1024).decode("utf-8")
            if not data:
                return
            
            request = Request(data)
            print("Incoming request:", request)
            if request.path.startswith("/static/"):
                response = serve_static(request.path.replace("/static/", ""))
            elif self.router:
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