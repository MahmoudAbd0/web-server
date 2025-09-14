import mimetypes
import os
from .response import Response

STATIC_DIR = os.path.join(os.path.dirname(__file__), "..", "static")

def serve_static(path):
    file_path = os.path.normpath(os.path.join(STATIC_DIR, path.lstrip("/")))

    if not file_path.startswith(os.path.abspath(STATIC_DIR)):
        return Response(status=403, body="Forbidden")
    
    if not os.path.exists(file_path):
        return Response(status=404, body="Not Found")
    
    mime, _ = mimetypes.guess_type(file_path)
    with open(file_path, "rb") as f:
        return Response(status=200, body=f.read(), headers={"Content-Type": mime or "application/octet-stream"})