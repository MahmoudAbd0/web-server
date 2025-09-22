import time
import threading

class TokenBucket:
    def __init__(self, capacity, refill_rate):
        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()
        self._lock = threading.Lock()
    

    def _refill(self):
        time_now = time.monotonic()
        elapsed = time_now - self.last_refill
        if elapsed <= 0:
            return
        
        self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)
        self.last_refill = time_now

    def allow_request(self, tokens = 1.0):
        with self._lock:
            self._refill()
            if self.tokens >= tokens:
                self.tokens -= tokens
                return True, 0.0
            
            needed = tokens - self.tokens
            if self.refill_rate <= 0:
                return False, float('inf')
            retry_after = needed / self.refill_rate
            return False, retry_after

