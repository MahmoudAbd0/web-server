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
        self.headers = {k.lower(): v for k,v in (headers or {}).items()}
        self.body = body if isinstance(body, (str, bytes)) else str(body)
        self.cookies = []

        # Ensure a default content-type if not provided
        if "content-type" not in self.headers:
            self.headers["content-type"] = "text/plain; charset=utf-8"
        

    def _format_header_name(self, name: str) -> str:
        return "-".join(part.capitalize() for part in name.split("-"))


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

       status_reason = self.STATUS_MESSAGES.get(self.status, "Unknown")
       status_line = f"HTTP/1.1 {self.status} {status_reason}\r\n"

       self.headers["content-length"] = str(body_length)

       headers_in_str = "".join( f"{self._format_header_name(key)}: {value}\r\n" for key, value in self.headers.items() if key != "set-cookie")
       cookie_headers = "".join(f"Set-Cookie: {cookie}\r\n" for cookie in self.cookies)


       return (status_line + headers_in_str + cookie_headers + "\r\n").encode("utf-8") + body_in_bytes


    def set_cookie(
        self,
        name ,
        value ,
        path  = "/",
        domain  = None,
        max_age  = None,
        expires  = None,
        secure  = False,
        http_only = False,
        same_site  = None,
        ):
        cookie_parts = [f"{name}={value}"]

        if same_site:
            same_site = same_site.capitalize()
        if same_site not in ("Strict", "Lax", "None"):
            raise ValueError("Invalid SameSite value: must be Strict, Lax, or None")

        attributes = {
        "Path": (path, False),
        "Domain": (domain, False),
        "Max-Age": (max_age, False),
        "Expires": (expires, False),
        "Secure": (secure, True),
        "HttpOnly": (http_only, True),
        "SameSite": (same_site, False),
        } 


        for key, (value, is_flag) in attributes.items():
            if is_flag and value:
                cookie_parts.append(key)
            elif value is not None:
                cookie_parts.append(f"{key}={value}")

        self.cookies.append("; ".join(cookie_parts))

    def __repr__(self):
        return f"<Response {self.status} {self.STATUS_MESSAGES.get(self.status, '')}, Headers={self.headers}, Cookies = {self.cookies}, Body={self.body!r}>"


