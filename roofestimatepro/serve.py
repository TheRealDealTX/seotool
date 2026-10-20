#!/usr/bin/env python3
"""Local preview of public/ that mimics the host: "/" serves home.html and
unknown paths get 404.html with a 404 status (redirects need PHP, so they are
not emulated). Usage: python3 serve.py [port] [dir]"""
import http.server
import os
import sys

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
DIR = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "public")


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=DIR, **k)

    def send_head(self):
        path = self.path.split("?")[0]
        if path == "/":
            self.path = "/home.html"
        fs = self.translate_path(self.path)
        if not os.path.exists(fs) or (os.path.isdir(fs) and not os.path.exists(os.path.join(fs, "index.html"))):
            self.send_response(404)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            return open(os.path.join(DIR, "404.html"), "rb")
        return super().send_head()


http.server.ThreadingHTTPServer(("", PORT), Handler).serve_forever()
