from .base_server import BaseServer

class SequentialServer(BaseServer):
    def __init__(self, host = "127.0.0.1", port = 8080, router = None):
        super().__init__(host, port, router)
    
    def start(self):
        self._create_socket()
        
        while True:
            client_connection, client_address = self.socket.accept()
            print(f"New connection from {client_address}")
            client_connection.settimeout(10)
            self.handle_client(client_connection)