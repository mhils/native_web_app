#!/usr/bin/env python3
# The .pyw extension signals that this script should be run without a console window.

import http.server
import sys
import threading

import native_web_app


# Setting up a HTTP server with Python's stdlib is a bit clunky, but we don't want to introduce new dependencies.
class RequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        if self.path == "/favicon.svg":
            self.send_header("content-type", "image/svg+xml")
            self.end_headers()
            self.wfile.write(
                b"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
                    <path d="M34,93l11,-29a15,15 0,1,1 9,0l11,29a45,45 0,1,0 -31,0z" stroke="#142" stroke-width="2" fill="#4a5"/>
                    </svg>""")
        else:
            self.send_header("content-type", "text/html")
            self.end_headers()
            self.wfile.write(
                b"""<html>
                    <head>
                        <title>Demo App</title>
                        <link rel="icon" type="image/svg+xml" href="/favicon.svg">
                        <style>
                        html, body {
                            margin: 0;
                            padding: 0;
                            display: flex;
                            align-items: center;
                            justify-content: center;
                            font-family: sans-serif;
                        }
                        </style>
                    </head>
                    <body>
                        <span><input type="checkbox" checked> A browser window without Electron &#x1F64C;</span>
                        <script>
                        /* send a POST request on window close to shut down the backend */
                        window.addEventListener("unload", function() {
                            navigator.sendBeacon("/shutdown");
                        }, false);
                        </script>
                    </body>
                    </html>"""
            )

    def do_POST(self):
        print("Shutting down!")
        # server.shutdown must be called from another thread
        threading.Thread(target=self.server.shutdown).start()


if __name__ == "__main__":
    if sys.stdout is None:  # .pyw (which hides the console window) does not have stdout attached.
        sys.stdout = sys.stderr = open("log.txt", "w")

    # We use a random free port here, this could of course be hardcoded.
    httpd = http.server.HTTPServer(("", 0), RequestHandler)
    url = f"http://localhost:{httpd.server_port}"
    try:
        native_web_app.open(url)
    except Exception:
        print(f"No web browser found. Please open a browser and point it to {url}.")
    httpd.serve_forever()
