from response import Response

class Router:
    def __init__(self):
        self.routes = {}

    def add_route(self ,path, method, handler):
        if method not in self.routes:
            self.routes[method] = {}

        self.routes[method][path] = handler

    def get(self, path, handler):
        return self.add_route(path, "GET", handler )

    def post(self, path, handler):
        return self.add_route(path, "POST", handler )

    def put(self, path, handler):
        return self.add_route(path, "PUT", handler )

    def delete(self, path, handler):
        return self.add_route(path, "DELETE", handler )


    def resolve(self, request):
        method_routes = self.routes.get(request.method, {})
        handler = method_routes.get(request.path)

        if handler:
            return handler(request)
        else:
            return Response(status=404, body="Not Found")
        
