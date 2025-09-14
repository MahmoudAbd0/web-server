import os
from .response import Response
import re

TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "..", "templates")

def render_template(filename, context = None):
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
