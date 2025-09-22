import threading
import queue
import time
from .base_server import BaseServer
from .response import Response
from .token_bucket import TokenBucket

class ThreadPoolServer(BaseServer):
    def __init__(self, host="127.0.0.1", port=8080, router=None, max_workers=5, max_queue_size=20,
                 rate_limit_capacity=10, rate_limit_refill=1, bucket_ttl=300,
                 global_limit_capacity=100, global_limit_refill=20
                 ):
        super().__init__(host, port, router)
        self.max_workers = max_workers
        self.request_queue = queue.Queue(maxsize=max_queue_size)
        self.workers = []
        self.client_buckets = {}
        self.bucket_capacity = rate_limit_capacity
        self.bucket_refill = rate_limit_refill
        self.bucket_ttl = bucket_ttl
        self.global_bucket = TokenBucket(global_limit_capacity, global_limit_refill)
        self._bucket_lock = threading.Lock()

        cleaner = threading.Thread(target=self._cleanup_buckets, daemon=True)
        cleaner.start()


    def start(self):
        self._create_socket()

        for i in range(self.max_workers):
            worker = threading.Thread(target=self.worker_loop, daemon= True)
            worker.start()
            self.workers.append(worker)

        while True:
            client_connection, client_address = self._accept_client()
            try:
                self.request_queue.put_nowait((client_connection, client_address))
            except queue.Full:
                print(f"Queue full! Rejecting connection from {client_address}")
                response = Response(status=503, body="Service Unavailable (Queue Full)")
                client_connection.sendall(response.convert_to_bytes())
                client_connection.close()


    def _get_client_bucket(self, client_ip):
        with self._bucket_lock:
            if client_ip not in self.client_buckets:
                self.client_buckets[client_ip] = TokenBucket(self.bucket_capacity, self.bucket_refill)
            return self.client_buckets[client_ip]


    def worker_loop(self):
        while True:
            task = self.request_queue.get()
            if task is None:
                break
            
            client_connection, client_address = task
            client_ip = client_address[0]
            bucket = self._get_client_bucket(client_ip)
            
            global_request_allowed, global_retry_after = self.global_bucket.allow_request()
            if not global_request_allowed:
                print(f"GLOBAL rate limit exceeded. Retry after {global_retry_after:.2f}s")
                response = Response(
                    status = 503,
                    body="Service Unavailable (Global Rate Limit)",
                    headers={"Retry-After": str(int(global_retry_after))}
                )

                client_connection.sendall(response.convert_to_bytes())
                client_connection.close()
                self.request_queue.task_done()
                continue

            request_allowed, retry_after = bucket.allow_request()
            if request_allowed:
                self.handle_client(client_connection)
            else:    
                print(f"Rate limit exceeded. Retry after {retry_after:.2f}s")
                response = Response(
                    status=429,
                    body="Too Many Requests. Please retry later.",
                    headers={"Retry-After": str(int(retry_after))}
                )
                client_connection.sendall(response.convert_to_bytes())
                client_connection.close()
                
            self.request_queue.task_done()


    def _cleanup_buckets(self):
        while True:
            time.sleep(self.bucket_ttl/2)
            time_now = time.monotonic()
            
            with self._bucket_lock:
                buckets_to_delete =  [
                ip for ip, bucket in self.client_buckets.items() if time_now - bucket.last_seen > self.bucket_ttl
                ]
                
                for ip in buckets_to_delete:
                    print(f"Cleaning up idle bucket for {ip}")
                    del self.client_buckets[ip]
