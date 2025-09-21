from .base_server import BaseServer
import threading
class MultiThreadingServer(BaseServer):
    def __init__(self, host = "127.0.0.1", port = 8080, router = None):
        super().__init__(host, port, router)

    def start(self):
        self._create_socket()

        while True:
            client_connection, _ = self._accept_client()
            thread = threading.Thread(target=self.handle_client, args=(client_connection,))
            thread.start()