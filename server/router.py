from .response import Response

class Router:
    """
    A simple HTTP router that maps request methods and paths to handler functions.

    The Router allows registering handlers for different HTTP methods (GET, POST, PUT, DELETE)
    and resolving incoming requests to the appropriate handler. If no matching route
    is found, a 404 response is returned.

    Attributes:
        routes (dict): A nested dictionary of registered routes in the format:
            {
                "GET": {"/path": handler_function},
                "POST": {"/path": handler_function},
                ...
            }

    Methods:
        add_route(path, method, handler):
            Registers a handler for a specific HTTP method and path.

        get(path, handler):
            Shortcut to register a GET route.

        post(path, handler):
            Shortcut to register a POST route.

        put(path, handler):
            Shortcut to register a PUT route.

        delete(path, handler):
            Shortcut to register a DELETE route.

        resolve(request):
            Finds and executes the handler for the given request.
            Returns a `Response` with 404 status if no route matches.
    """

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
        
