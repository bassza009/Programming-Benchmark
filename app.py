#!/usr/bin/env python3
"""Simple landing page web server using Python's built-in HTTP server."""

import http.server
import socketserver
import os

PORT = 8000
HANDLER = http.server.SimpleHTTPRequestHandler


class LandingPageHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(self.get_landing_page().encode())
        else:
            super().do_GET()

    def get_landing_page(self):
        return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Welcome to My Website</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
        }
        
        header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem 0;
            text-align: center;
        }
        
        header h1 {
            font-size: 3rem;
            margin-bottom: 0.5rem;
        }
        
        header p {
            font-size: 1.2rem;
            opacity: 0.9;
        }
        
        main {
            max-width: 1200px;
            margin: 3rem auto;
            padding: 0 2rem;
        }
        
        .intro {
            background: #f4f4f4;
            padding: 2rem;
            border-radius: 8px;
            margin-bottom: 2rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 2rem;
            margin: 2rem 0;
        }
        
        .feature {
            background: white;
            padding: 1.5rem;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }
        
        .feature:hover {
            transform: translateY(-5px);
        }
        
        .feature h3 {
            color: #667eea;
            margin-bottom: 0.5rem;
        }
        
        footer {
            background: #333;
            color: white;
            text-align: center;
            padding: 2rem;
            margin-top: 3rem;
        }
        
        .cta-button {
            display: inline-block;
            background: #667eea;
            color: white;
            padding: 0.75rem 1.5rem;
            border-radius: 4px;
            text-decoration: none;
            margin-top: 1rem;
            transition: background 0.3s ease;
        }
        
        .cta-button:hover {
            background: #764ba2;
        }
    </style>
</head>
<body>
    <header>
        <h1> Welcome!</h1>
        <p>Your Amazing Python-Powered Website</p>
    </header>
    
    <main>
        <section class="intro">
            <h2>Hello, Welcome to My Website</h2>
            <p>This is a simple landing page created with Python's built-in HTTP server. It demonstrates how you can build web applications using Python without external frameworks.</p>
            <a href="#" class="cta-button">Get Started</a>
        </section>
        
        <section class="features">
            <div class="feature">
                <h3> Fast</h3>
                <p>Lightning-quick response times with Python's efficient HTTP server implementation.</p>
            </div>
            <div class="feature">
                <h3> Simple</h3>
                <p>No complex frameworks needed. Just pure Python serving your content.</p>
            </div>
            <div class="feature">
                <h3> Beautiful</h3>
                <p>Modern responsive design that looks great on all devices.</p>
            </div>
        </section>
    </main>
    
    <footer>
        <p>&copy; 2026 My Website. Built with Python.</p>
    </footer>
</body>
</html>'''


if __name__ == '__main__':
    with socketserver.TCPServer(("", PORT), LandingPageHandler) as httpd:
        print(f" Server running at http://localhost:{PORT}")
        print("Press Ctrl+C to stop the server")
        httpd.serve_forever()
