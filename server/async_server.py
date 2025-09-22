from .base_server import BaseServer
import asyncio
from .request import Request
from .static import serve_static
from .response import Response

class AsyncServer(BaseServer):
    def __init__(self, host="127.0.0.1", port=8080, router=None):
        super().__init__(host, port, router)

    async def start_server(self):
        server = await asyncio.start_server(self.handle_client, self.host, self.port)
        address = server.sockets[0].getsockname()
        print(f"Async server running on http://{address[0]}:{address[1]}")

        async with server:
            server.serve_forever()

    def start(self):
        try:
            asyncio.run(self.start_server())
        except KeyboardInterrupt:
            print("\nServer stopped manually")

    async def handle_client(self, reader, writer):
        try:
             
            data = (await reader.read(1024).decode("utf-8"))
            if not data:
                return
            
            request = Request(data)
            print("Incoming request:", request)

            if request.path.startswith("/static/"):
                response = serve_static(request.path.replace("/static/", ""))
            elif self.router:
                    response = self.router.resolve(request)
            else:
                    response = Response(body="Hello from AsyncServer!")

            writer.write(response.convert_to_bytes())
            await writer.drain()

        except Exception as e:
            print("Error handling request:", e)
            error_response = Response(status=500, body="Internal Server Error")
            writer.write(error_response.convert_to_bytes())
            await writer.drain()

        finally:
            writer.close()
            await writer.wait_closed()

