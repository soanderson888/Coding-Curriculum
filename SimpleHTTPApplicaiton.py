from http.server import BaseHTTPRequestHandler, HTTPServer


class simpleServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)

        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write("Hey Teymor! Whats up? Hope you are having a blast reading my python files!! This website was made to remind you to text sophie telling her she is the best!!!".encode())


host = 'localhost'
port = 8000

httpd = HTTPServer((host, port),simpleServer)
print(f"Server listening on {host}:{port}")

httpd.serve_forever()


