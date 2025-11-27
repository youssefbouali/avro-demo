#!/usr/bin/env python3
"""
Simple Avro Server
Runs on port 8000 and serves Avro-encoded data
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import fastavro
import io
import random
from datetime import datetime

# Avro Schema
SCHEMA = {
    "type": "record",
    "name": "User",
    "namespace": "com.example",
    "fields": [
        {"name": "id", "type": "int"},
        {"name": "name", "type": "string"},
        {"name": "email", "type": "string"},
        {"name": "age", "type": "int"},
        {"name": "country", "type": "string"},
        {"name": "active", "type": "boolean"},
    ]
}

# Sample data
NAMES = ["Alice", "Bob", "Charlie", "Diana", "Edward", "Fiona"]
COUNTRIES = ["USA", "UK", "France", "Germany", "Japan", "Canada"]


def generate_user():
    """Generate a random user record"""
    return {
        "id": random.randint(1, 1000),
        "name": random.choice(NAMES),
        "email": f"user{random.randint(100, 999)}@example.com",
        "age": random.randint(20, 60),
        "country": random.choice(COUNTRIES),
        "active": random.choice([True, False]),
    }


class AvroServerHandler(BaseHTTPRequestHandler):
    """HTTP request handler for Avro server"""

    def do_GET(self):
        """Handle GET requests"""
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"""
            <html>
            <body>
            <h1>Simple Avro Server</h1>
            <ul>
            <li><a href="/avro/single">/avro/single</a> - Get single user (Avro)</li>
            <li><a href="/avro/batch">/avro/batch</a> - Get 10 users (Avro)</li>
            <li><a href="/json/single">/json/single</a> - Get single user (JSON)</li>
            <li><a href="/json/batch">/json/batch</a> - Get 10 users (JSON)</li>
            <li><a href="/health">/health</a> - Health check</li>
            </ul>
            </body>
            </html>
            """)

        elif self.path == "/health":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok"}).encode())

        elif self.path == "/avro/single":
            user = generate_user()
            fo = io.BytesIO()
            fastavro.schemaless_writer(fo, SCHEMA, user)
            avro_bytes = fo.getvalue()

            self.send_response(200)
            self.send_header("Content-type", "application/octet-stream")
            self.send_header("Content-Length", str(len(avro_bytes)))
            self.send_header("X-User-Name", user["name"])
            self.end_headers()
            self.wfile.write(avro_bytes)
            print(f"✓ Sent Avro user: {user['name']} ({len(avro_bytes)} bytes)")

        elif self.path == "/avro/batch":
            users = [generate_user() for _ in range(10)]
            fo = io.BytesIO()
            fastavro.writer(fo, SCHEMA, users)
            avro_bytes = fo.getvalue()

            self.send_response(200)
            self.send_header("Content-type", "application/octet-stream")
            self.send_header("Content-Length", str(len(avro_bytes)))
            self.send_header("X-Record-Count", "10")
            self.end_headers()
            self.wfile.write(avro_bytes)
            print(f"✓ Sent Avro batch: 10 users ({len(avro_bytes)} bytes)")

        elif self.path == "/json/single":
            user = generate_user()
            json_str = json.dumps(user)
            json_bytes = json_str.encode()

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.send_header("Content-Length", str(len(json_bytes)))
            self.end_headers()
            self.wfile.write(json_bytes)
            print(f"✓ Sent JSON user: {user['name']} ({len(json_bytes)} bytes)")

        elif self.path == "/json/batch":
            users = [generate_user() for _ in range(10)]
            json_str = json.dumps(users)
            json_bytes = json_str.encode()

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.send_header("Content-Length", str(len(json_bytes)))
            self.end_headers()
            self.wfile.write(json_bytes)
            print(f"✓ Sent JSON batch: 10 users ({len(json_bytes)} bytes)")

        else:
            self.send_response(404)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Not found"}).encode())

    def log_message(self, format, *args):
        """Suppress default logging"""
        return


def run_server(port=8000):
    """Run the Avro server"""
    server = HTTPServer(("0.0.0.0", port), AvroServerHandler)
    print(f"🚀 Avro Server started on http://localhost:{port}/")
    print(f"   Endpoints:")
    print(f"   - http://localhost:{port}/avro/single")
    print(f"   - http://localhost:{port}/avro/batch")
    print(f"   - http://localhost:{port}/json/single")
    print(f"   - http://localhost:{port}/json/batch")
    print(f"\nPress Ctrl+C to stop\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\n✓ Server stopped")


if __name__ == "__main__":
    run_server()
