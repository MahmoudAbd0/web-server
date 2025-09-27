class SessionMiddleware:
    def __init__(self, store):
        self.store = store

    def process_request(self, request):
        session_id = request.cookies.get("session_id")

        if not session_id or not self.store.get_session(session_id):
            request._new_session = True
            session_id = self.store.create_session()

        request.session_id = session_id
        request.session = self.store.get_session(session_id)

        visits = request.session.get("visits", 0) + 1
        self.store.set_session(session_id, "visits", visits)
        request.session["visits"] = visits

    def process_response(self, request, response):
        if getattr(request, "_new_session", False):
            response.set_cookie("session_id", request.session_id, http_only=True)
