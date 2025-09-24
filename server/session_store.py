import threading
import uuid
import time

class SessionStore():
    def __init__(self, ttl = 1800):
        self.sessions = {}
        self.ttl = ttl
        self.lock = threading.Lock()


    def create_session(self):
        session_id = str(uuid.uuid4())
        with self.lock:
            self.sessions[session_id] = {"data": {}, "last_seen": time.monotonic()}
        return session_id
    

    def get_session(self, session_id):
        with self.lock:
            session = self.sessions.get(session_id)
            if not session:
                return None
            if time.monotonic() - session["last_seen"] > self.ttl:
                del self.sessions[session_id]
                return None
            session["last_seen"] = time.monotonic()
            return session["data"]


    def set_session(self, session_id, key, value):
        with self.lock:
            if session_id in self.sessions:
                self.sessions[session_id]["data"][key] = value
                self.sessions[session_id]["last_seen"] = time.monotonic()

   
    def delete_session(self, session_id):
        with self.lock:
            self.sessions.pop(session_id, None)


    def start_cleaner(self):
        cleaner = threading.Thread(target=self._cleanup_sessions, daemon=True)
        cleaner.start()


    def _cleanup_sessions(self):
        while True:
            time.sleep(self.ttl/2)
            time_now  = time.monotonic()
            with self.lock:
                expired_sessions = [session_id for session_id, session in self.sessions.items() if time_now - session["last_seen"] > self.ttl ]
                for session in expired_sessions:
                    print(f"Cleaning expired session {session}")
                    del self.sessions[session]

