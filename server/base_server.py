from abc import ABC, abstractmethod
from .request import Request
from .static import serve_static
from .response import Response
import socket

class BaseServer(ABC):
    def __init__(self, host = "127.0.0.1", port = 8080, router = None):
        self.host = host
        self.port = port
        self.router = router
        self.socket = None

    @abstractmethod
    def start(self):
        pass

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
   

    def _create_socket(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)
        print(f"Server running on http://{self.host}:{self.port}")

