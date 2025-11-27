#!/usr/bin/env python3
"""
Simple HTTP Server for Avro vs JSON Comparison Tool
Serves static HTML/CSS/JS files
"""

import http.server
import socketserver
import os
import sys
from pathlib import Path

PORT = 8000
Handler = http.server.SimpleHTTPRequestHandler

def run_server():
    # Change to the script directory
    script_dir = Path(__file__).parent.absolute()
    os.chdir(script_dir)
    
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"🚀 Server running!")
        print(f"📍 Open your browser to: http://localhost:{PORT}")
        print(f"📁 Serving from: {script_dir}")
        print(f"\nPress Ctrl+C to stop the server\n")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n👋 Server stopped")
            sys.exit(0)

if __name__ == "__main__":
    run_server()
