class SessionMiddleware:
    def __init__(self, store):
        self.store = store

    def process(self, request, response):
        session_id = request.cookies.get("session_id")

        if not session_id or not self.store.get_session(session_id):
            session_id = self.store.create_session()
            response.set_cookie("session_id", session_id, http_only=True)

        request.session_id = session_id
        request.session = self.store.get_session(session_id)