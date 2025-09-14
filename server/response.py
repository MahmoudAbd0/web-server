class Response:
    """
    Represents an HTTP response.

    This class constructs an HTTP response message from:
    - Status code (e.g., 200, 404)
    - Headers
    - Body

    It can then serialize the response into raw bytes to be sent
    over a TCP socket.

    Attributes:
        STATUS_MESSAGES (dict[int, str]): Mapping of common HTTP status codes
            to their reason phrases.
        status (int): The HTTP status code (default: 200).
        headers (dict[str, str]): HTTP headers as a dictionary.
        body (str | bytes): The response body.

    Example:
        >>> response = Response(
        ...     status=200,
        ...     headers={"Content-Type": "text/plain"},
        ...     body="Hello, World!"
        ... )
        >>> response_bytes = response.convert_to_bytes()
        >>> print(response_bytes.decode())
        HTTP/1.1 200 OK
        Content-Type: text/plain
        Content-Length: 13

        Hello, World!
    """
    
    STATUS_MESSAGES = {
        200: "OK",
        201: "Created",
        400: "Bad Request",
        401: "Unauthorized",
        403: "Forbidden",
        404: "Not Found",
        500: "Internal Server Error",
    }
  

    def __init__(self, status = 200, headers = None, body = ""):
        """
        Initialize a Response object.

        Args:
            status (int): The HTTP status code (default: 200).
            headers (dict[str, str] | None): Optional HTTP headers.
            body (str | bytes): The response body (default: "").
        """

        self.status = status
        self.headers = headers or {}
        self.body = body if isinstance(body, (str, bytes)) else str(body)

        # Ensure a default content-type if not provided
        if "content-type" not in self.headers:
            self.headers["content-type"] = "text/plain; charset=utf-8"
        

    def convert_to_bytes(self):
       """
        Convert the response into raw HTTP bytes.

        Returns:
            bytes: The full HTTP response message (status line, headers, body).

        Example:
            >>> Response(200, body="OK").convert_to_bytes()
            b'HTTP/1.1 200 OK\\r\\nContent-Type: text/plain; charset=utf-8\\r\\nContent-Length: 2\\r\\n\\r\\nOK'
       """

       body_in_bytes = self.body.encode("utf-8") if isinstance(self.body, str) else self.body
       body_length = len(body_in_bytes)

       status_reason = self.STATUS_MESSAGES.get(self.status, "")
       status_line = f"HTTP/1.1 {self.status} {status_reason}\r\n"

       self.headers["content-length"] = str(body_length)

       headers_in_str = "".join(f"{key}: {value}\r\n" for key, value in self.headers.items())

       return (status_line + headers_in_str + "\r\n").encode("utf-8") + body_in_bytes


    def __repr__(self):
        return f"<Response {self.status} {self.STATUS_MESSAGES.get(self.status, '')}, Headers={self.headers}, Body={self.body!r}>"

