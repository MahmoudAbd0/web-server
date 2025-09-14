"""
Template rendering utility for the web server.

This module provides a simple function to render HTML templates from the
server's `templates` directory. It supports basic placeholder substitution
using a context dictionary.

Constants:
    TEMPLATES_DIR (str): Absolute path to the server's templates directory.
"""

import os
from .response import Response
import re

# Absolute path to the templates directory
TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "..", "templates")

def render_template(filename, context = None):
    """
    Render an HTML template with optional context data.

    Args:
        filename (str): The name of the template file to render (e.g., "index.html").
        context (dict, optional): A dictionary of key-value pairs to replace
                                  placeholders in the template. Defaults to {}.

    Returns:
        Response: A Response object containing the rendered HTML content and
                  appropriate "Content-Type" header, or a 404 Response if the
                  template file does not exist.

    Behavior:
        - Reads the template file from the TEMPLATES_DIR.
        - Returns 404 Not Found if the file does not exist.
        - Replaces placeholders in the form {{ key }} with corresponding values
          from the context dictionary.
        - If a placeholder key is not found in context, it remains unchanged.
        - Returns the final HTML content as a Response object with
          "Content-Type: text/html; charset=utf-8".
    """

    context = context or {}
    file_path = os.path.join(TEMPLATES_DIR, filename)

    if not os.path.exists(file_path):
        return Response(status=404, body="NOT FOUND")


    with open(file_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    template_pattern = re.compile(r"{{\s*(\w+)\s*}}")

    def replacer(match):
        key = match.group(1)
        return str(context.get(key, match.group(0)))

    html_content = template_pattern.sub(replacer, html_content)

    return Response(body=html_content, headers={"Content-Type": "text/html; charset=utf-8"})
