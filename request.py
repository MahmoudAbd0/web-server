class Request:
    """
    Represents an HTTP request.

    This class parses a raw HTTP request string into its components:
    - HTTP method (e.g., GET, POST)
    - Path (endpoint)
    - Query parameters
    - HTTP version
    - Headers
    - Body

    Attributes:
        data (str): The raw HTTP request string.
        method (str): The HTTP method (e.g., GET, POST).
        path (str): The request path (e.g., /users).
        query_params (dict): Parsed query parameters from the URL.
        http_version (str): HTTP version (e.g., HTTP/1.1).
        headers (dict): Parsed HTTP headers.
        body (str): The request body.

    Example:
        >>> data = (
        ...     "POST /users?id=42&flag HTTP/1.1\\r\\n"
        ...     "Host: localhost:8080\\r\\n"
        ...     "User-Agent: curl/7.68.0\\r\\n"
        ...     "Content-Type: application/json\\r\\n"
        ...     "Content-Length: 15\\r\\n"
        ...     "\\r\\n"
        ...     '{"name": "Ali"}'
        ... )
        >>> request = Request(data)
        >>> request.method
        'POST'
        >>> request.path
        '/users'
        >>> request.query_params
        {'id': '42', 'flag': True}
    """
    
    def __init__(self, data):
        """
        Initialize a Request object by parsing the raw HTTP request string.

        Args:
            data (str): The raw HTTP request string.
        """

        self.data = data.strip()
        self.method = None
        self.path = None
        self.query_params = {}
        self.http_version = None
        self.headers = {}
        self.body = ""

        self.parse_request()

    def parse_request(self):
        """
        Parse the raw request string into its components.

        Raises:
            ValueError: If the body length does not match the Content-Length header.
        """

        splitted_data = self.data.split("\r\n\r\n",1)
        request_head = splitted_data[0]
        request_body = splitted_data[1] if len(splitted_data) > 1 else ""
        self.body = request_body

        head_lines = request_head.splitlines()

        start_line = head_lines[0]
        self._parse_start_line(start_line)
        self._parse_head_lines(head_lines)
        
        declared_length = int(self.get_header("content-length", 0))
        actual_length = len(self.body.encode("utf-8"))
        if declared_length and declared_length != actual_length:
            raise ValueError(f"Body length ({actual_length}) does not match Content-Length ({declared_length})")
     
    
    def get_header(self, key, default = None):
        """
        Retrieve a header value by key.

        Args:
            key (str): Header name (case-insensitive).
            default (Any): Value to return if the header is not found.

        Returns:
            str | Any: Header value if found, otherwise `default`.
        """
            
        return self.headers.get(key, default)
    

    def json(self):
        """
        Parse the request body as JSON if the Content-Type is application/json.

        Returns:
            dict | None: Parsed JSON body, or None if not JSON.
        """
         
        if self.get_header("content-type") == "application/json":
            import json
            return json.loads(self.body)
        return None

    def _parse_start_line(self, start_line):
        """
        Parse the request start line into method, path, query params, and HTTP version.

        Example:
            "GET /users?id=42 HTTP/1.1" ->
                method = "GET"
                path = "/users"
                query_params = {"id": "42"}
                http_version = "HTTP/1.1"

        Args:
            start_line (str): The HTTP start line.
        
        Raises:
            IndexError: If the start line format is invalid.
        """ 
         
        splitted_start_line = start_line.split()
        try:
            self.method = splitted_start_line[0]
            self.http_version = splitted_start_line[2]
        except IndexError:
            raise IndexError('Invalid request start line format')
        
        path_and_params = splitted_start_line[1]
        splitted_path_and_params = path_and_params.split("?")
        self.path = splitted_path_and_params[0]

        if len(splitted_path_and_params) > 1:
            params = splitted_path_and_params[1].split("&")

            for param in params:
                param_key, _, param_value = param.partition('=')
                self.query_params[param_key] = param_value or True

    def _parse_head_lines(self, head_lines):
        """
        Parse raw header lines into a dictionary of headers.

        Args:
            head_lines (list[str]): List of header lines (excluding start line).

        Notes:
            Header keys are stored in lowercase for case-insensitive access.
        """

        if len(head_lines) > 1:
            for header in head_lines[1:]:
                if not header:
                    continue
                try:
                        header_key, header_value = header.split(": ",1)
                        self.headers[header_key.lower().strip()] = header_value
                except ValueError:
                    pass


    def __repr__(self):
        """Return a human-readable string representation of the Request object."""

        return f"<Request \n METHOD: {self.method} \n PATH: {self.path} \n HTTP_VERSION: {self.http_version} \n QUERY PARAMS: {self.query_params} \n HEADERS: {self.headers} \n BODY: {self.body}>"



data = """POST /users?id=42&flag HTTP/1.1\r\nHost: localhost:8080\r\nUser-Agent:curl/7.68.0\r\nContent-Type: application/json\r\nContent-Length: 15\r\n\r\n{"name": "Ali"}"""
request = Request(data)
print(request)



"""
POST /users?id=42 HTTP/1.1
Host: localhost:8080
User-Agent: curl/7.68.0
Content-Type: application/json
Content-Length: 18

{"name": "Ali"}
"""