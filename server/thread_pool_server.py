from .base_server import BaseServer
import threading
import queue

class ThreadPoolServer(BaseServer):
    def __init__(self, host="127.0.0.1", port=8080, router=None, max_workers=5, max_queue_size=20):
        super().__init__(host, port, router)
        self.max_workers = max_workers
        self.request_queue = queue.Queue(maxsize=max_queue_size)
        self.workers = []

    def start(self):
        self._create_socket()

        for i in range(self.max_workers):
            worker = threading.Thread(target=self.worker_loop, daemon= True)
            worker.start()
            self.workers.append(worker)

        while True:
            client_connection, client_address = self._accept_client()
            try:
                self.request_queue.put_nowait(client_connection)
            except queue.Full:
                print(f"Queue full! Rejecting connection from {client_address}")
                client_connection.close()


    def worker_loop(self):
        while True:
            client_connection = self.request_queue.get()
            if client_connection is None:
                break
            self.handle_client(client_connection)
            self.request_queue.task_done()