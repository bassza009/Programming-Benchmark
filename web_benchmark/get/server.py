#!/usr/bin/env python3
"""Simple GET HTTP server for benchmarking in Python."""

import http.server
import socketserver
import json
import sys
import os

PORT = int(os.getenv('PORT', 8001))

class GetHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests."""
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = json.dumps({
                "status": "ok",
                "message": "Hello from Python GET Server",
                "language": "Python"
            })
            self.wfile.write(response.encode())
        
        elif self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = json.dumps({"status": "healthy"})
            self.wfile.write(response.encode())
        
        elif self.path.startswith('/api/data'):
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = json.dumps({
                "data": "benchmark_data",
                "timestamp": 1234567890,
                "value": 42
            })
            self.wfile.write(response.encode())
        
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = json.dumps({"error": "Not found"})
            self.wfile.write(response.encode())
    
    def log_message(self, format, *args):
        """Suppress logging."""
        pass

if __name__ == '__main__':
    with socketserver.TCPServer(("", PORT), GetHandler) as httpd:
        print(f"Python GET Server running on port {PORT}", file=sys.stderr)
        httpd.serve_forever()
