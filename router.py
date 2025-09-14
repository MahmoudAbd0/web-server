from response import Response

class Router:
    def __init__(self):
        self.routes = {}

    def add_route(self ,path, method, handler):
        if method not in self.routes:
            self.routes[method] = {}

        self.routes[method][path] = handler

    def resolve(self, request):
        method_routes = self.routes.get(request.method, {})
        handler = method_routes.get(request.path)

        if handler:
            return handler(request)
        else:
            return Response(status=404, body="Not Found")
        
