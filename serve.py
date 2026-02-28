#!/usr/bin/env python3
"""Local dev server that mimics GitHub Pages clean URL routing."""

import http.server
import os

PORT = 8888
DIRECTORY = os.path.dirname(os.path.abspath(__file__))


class CleanURLHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        # Strip query string for file lookup
        path = self.path.split("?")[0]

        # If path has no extension and isn't a directory, try .html
        if "." not in os.path.basename(path):
            html_path = os.path.join(DIRECTORY, path.lstrip("/") + ".html")
            if os.path.isfile(html_path):
                self.path = path + ".html"

        return super().do_GET()


if __name__ == "__main__":
    with http.server.HTTPServer(("", PORT), CleanURLHandler) as httpd:
        print(f"Serving at http://localhost:{PORT}")
        httpd.serve_forever()
