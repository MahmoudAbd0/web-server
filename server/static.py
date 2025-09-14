"""
Static file serving utility for the web server.

This module provides a simple function to serve files from the server's
`static` directory. It ensures security by preventing directory traversal
attacks, checks file existence, and automatically sets the correct
Content-Type header using Python's `mimetypes` module.

Constants:
    STATIC_DIR (str): Absolute path to the server's static directory.
"""

import mimetypes
import os
from .response import Response

# Absolute path to the static files directory
STATIC_DIR = os.path.join(os.path.dirname(__file__), "..", "static")

def serve_static(path):
    """
    Serve a file from the static directory.

    Args:
        path (str): The URL path of the requested static file (e.g., "/css/style.css").

    Returns:
        Response: A Response object containing the file content and headers,
                  or an error response if the file is not found or access is forbidden.

    Behavior:
        - Normalizes the requested path to prevent directory traversal attacks.
        - Checks that the requested file is inside STATIC_DIR.
        - Returns 403 Forbidden if the path attempts to escape STATIC_DIR.
        - Returns 404 Not Found if the file does not exist.
        - Determines MIME type using `mimetypes.guess_type` and sets
          "Content-Type" header accordingly. Defaults to "application/octet-stream".
        - Returns the file content as bytes with a 200 OK response if successful.
    """
     
    file_path = os.path.normpath(os.path.join(STATIC_DIR, path.lstrip("/")))

    # Security check: prevent access outside STATIC_DIR
    if not file_path.startswith(os.path.abspath(STATIC_DIR)):
        return Response(status=403, body="Forbidden")
    
    if not os.path.exists(file_path):
        return Response(status=404, body="Not Found")
    
    mime, _ = mimetypes.guess_type(file_path)
    with open(file_path, "rb") as f:
        return Response(status=200, body=f.read(), headers={"Content-Type": mime or "application/octet-stream"})