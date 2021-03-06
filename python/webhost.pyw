import http.server  # Our http server handler for http requests
import socketserver  # Establish the TCP Socket connections

PORT = 8008


class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '../web/router.html'
        else:
            self.path = '../web/index.html'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)


Handler = MyHttpRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("Http Server Serving at port", PORT)
    httpd.serve_forever()
