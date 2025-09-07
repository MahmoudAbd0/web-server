class Response:
    
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
        self.status = status
        self.headers = headers or {}
        self.body = body if isinstance(body, (str, bytes)) else str(body)

        if "content-type" not in self.headers:
            self.headers["content-type"] = "text/plain; charset=utf-8"
        


    def convert_to_bytes(self):
       body_in_bytes = self.body.encode("utf-8") if isinstance(self.body, str) else self.body
       body_length = len(body_in_bytes)

       status_reason = self.STATUS_MESSAGES.get(self.status, "")
       status_line = f"HTTP/1.1 {self.status} {status_reason}\r\n"

       self.headers["content-length"] = str(body_length)

       headers_in_str = "".join(f"{key}: {value}\r\n" for key, value in self.headers.items())

       return (status_line + headers_in_str + "\r\n").encode("utf-8") + body_in_bytes


