from .sequential_server import SequentialServer

SERVER_TYPES = {
"sequential": SequentialServer
}

class ServerFactory:
    @staticmethod
    def create_server(server_type, host = "127.0.0.1", port = 8080, router = None):
        try:
            return SERVER_TYPES[server_type](host, port, router)
        except KeyError:
            raise ValueError(f"Unknown server type: {server_type}")