#!/usr/bin/env python
"""
Simple HTTP server for testing frontend connectivity
Serves static files from the frontend directory
"""
import http.server
import socketserver
import os
import sys
import mimetypes

PORT = 5173
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), 'frontend')

# Add custom MIME types for TypeScript and JSX/TSX
mimetypes.add_type('text/javascript', '.js')
mimetypes.add_type('text/javascript', '.mjs')
mimetypes.add_type('text/javascript', '.ts')
mimetypes.add_type('text/javascript', '.tsx')
mimetypes.add_type('text/javascript', '.jsx')
mimetypes.add_type('application/json', '.json')

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=FRONTEND_DIR, **kwargs)

    def do_GET(self):
        # Serve index_simple.html for root path
        if self.path == '/' or self.path == '':
            self.path = '/index_simple.html'
        return super().do_GET()

    def end_headers(self):
        # Add CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def guess_type(self, path):
        """Override to handle TypeScript files"""
        mimetype, encoding = mimetypes.guess_type(path)
        if mimetype is None:
            # Default to text/javascript for .ts/.tsx files
            if path.endswith(('.ts', '.tsx', '.jsx')):
                mimetype = 'text/javascript'
            else:
                mimetype = 'text/plain'
        return mimetype, encoding

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

def main():
    os.chdir(FRONTEND_DIR)
    
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Frontend server running at http://localhost:{PORT}")
        print(f"Serving files from: {FRONTEND_DIR}")
        print("Press Ctrl+C to stop")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped")

if __name__ == "__main__":
    main()
