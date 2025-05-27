#!/usr/bin/env python3
"""
Simple HTTP server for serving the React app build folder
"""
import http.server
import socketserver
import os

PORT = 3000
DIRECTORY = "build"

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        # Add CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    if not os.path.isdir(DIRECTORY):
        print(f"Error: '{DIRECTORY}' directory not found.")
        print("Please run 'npm run build' first to create the build directory.")
        exit(1)
        
    print(f"Starting server at http://localhost:{PORT}")
    print(f"Serving files from the '{DIRECTORY}' directory")
    print("Press Ctrl+C to stop the server")
    
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.") 