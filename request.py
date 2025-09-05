class Request:
    def __init__(self, data):
        self.data = data.strip()
        self.method = None
        self.path = None
        self.query_params = {}
        self.http_version = None
        self.headers = {}
        self.body = {}

        self.parse_request()

        def parse_request(self):
            splitted_data = self.data.split("\r\n\r\n",1)
            request_head = splitted_data[0]
            self.body = splitted_data[1] if len(splitted_data) > 1 else ""

            pass



"""
POST /users?id=42 HTTP/1.1
Host: localhost:8080
User-Agent: curl/7.68.0
Content-Type: application/json
Content-Length: 18

{"name": "Ali"}



NOTES:
*  The body is separated from the request start-line and headers with an empty line.
"""