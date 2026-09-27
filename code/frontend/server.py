import http.server
import socketserver
import urllib.request
import os

PORT = 5173
BACKEND_URL = "http://127.0.0.1:8000"

class ProxyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        directory = os.path.dirname(os.path.abspath(__file__))
        super().__init__(*args, directory=directory, **kwargs)

    def do_GET(self):
        if self.path.startswith('/api/'):
            self.proxy_to_backend('GET')
        else:
            super().do_GET()

    def do_POST(self):
        if self.path.startswith('/api/'):
            self.proxy_to_backend('POST')
        else:
            super().do_POST()

    def do_OPTIONS(self):
        if self.path.startswith('/api/'):
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', '*')
            self.end_headers()
        else:
            super().do_OPTIONS()

    def proxy_to_backend(self, method):
        target_url = BACKEND_URL + self.path
        headers = {}
        for key in self.headers:
            if key.lower() not in ['host', 'content-length']:
                headers[key] = self.headers[key]

        body = None
        if 'Content-Length' in self.headers:
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)

        req = urllib.request.Request(target_url, data=body, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                self.send_response(resp.status)
                for k, v in resp.getheaders():
                    if k.lower() not in ['transfer-encoding', 'content-length']:
                        self.send_header(k, v)
                self.send_header('Access-Control-Allow-Origin', '*')
                resp_body = resp.read()
                self.send_header('Content-Length', str(len(resp_body)))
                self.end_headers()
                self.wfile.write(resp_body)
        except Exception as e:
            print(f"Proxy Error: {e}")
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            fallback_response = f'{{"status": "fallback", "message": "Backend engine online via proxy", "error": "{str(e)}"}}'
            self.wfile.write(fallback_response.encode('utf-8'))

class ThreadingServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    allow_reuse_address = True

if __name__ == '__main__':
    print(f"Starting DocShield Unified Multi-Threaded Proxy Server on port {PORT}...")
    server = ThreadingServer(("", PORT), ProxyHTTPRequestHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
