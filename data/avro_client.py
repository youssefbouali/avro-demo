#!/usr/bin/env python3
"""
Simple Avro Client
Fetches and decodes Avro data from server
"""

import urllib.request
import json
import fastavro
import io
import time
from datetime import datetime

# Avro Schema (must match server schema)
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


class AvroClient:
    """Simple Avro client for fetching and decoding data"""

    def __init__(self, server_url="http://localhost:8000"):
        self.server_url = server_url

    def get_avro_single(self):
        """Fetch and decode single Avro user"""
        url = f"{self.server_url}/avro/single"
        start = time.time()
        
        response = urllib.request.urlopen(url)
        data = response.read()
        
        fo = io.BytesIO(data)
        user = fastavro.schemaless_reader(fo, SCHEMA)
        
        elapsed = (time.time() - start) * 1000  # Convert to ms
        
        return {
            "user": user,
            "size_bytes": len(data),
            "time_ms": elapsed,
            "format": "Avro"
        }

    def get_avro_batch(self):
        """Fetch and decode batch of Avro users"""
        url = f"{self.server_url}/avro/batch"
        start = time.time()
        
        response = urllib.request.urlopen(url)
        data = response.read()
        
        fo = io.BytesIO(data)
        users = list(fastavro.reader(fo))
        
        elapsed = (time.time() - start) * 1000
        
        return {
            "users": users,
            "count": len(users),
            "size_bytes": len(data),
            "time_ms": elapsed,
            "format": "Avro"
        }

    def get_json_single(self):
        """Fetch and decode single JSON user"""
        url = f"{self.server_url}/json/single"
        start = time.time()
        
        response = urllib.request.urlopen(url)
        data = response.read()
        user = json.loads(data.decode())
        
        elapsed = (time.time() - start) * 1000
        
        return {
            "user": user,
            "size_bytes": len(data),
            "time_ms": elapsed,
            "format": "JSON"
        }

    def get_json_batch(self):
        """Fetch and decode batch of JSON users"""
        url = f"{self.server_url}/json/batch"
        start = time.time()
        
        response = urllib.request.urlopen(url)
        data = response.read()
        users = json.loads(data.decode())
        
        elapsed = (time.time() - start) * 1000
        
        return {
            "users": users,
            "count": len(users),
            "size_bytes": len(data),
            "time_ms": elapsed,
            "format": "JSON"
        }

    def health_check(self):
        """Check server health"""
        try:
            url = f"{self.server_url}/health"
            response = urllib.request.urlopen(url)
            data = json.loads(response.read().decode())
            return data["status"] == "ok"
        except:
            return False


def print_user(user):
    """Pretty print a user record"""
    print(f"  ID: {user['id']}")
    print(f"  Name: {user['name']}")
    print(f"  Email: {user['email']}")
    print(f"  Age: {user['age']}")
    print(f"  Country: {user['country']}")
    print(f"  Active: {user['active']}")


def main():
    """Main client demo"""
    print("=" * 60)
    print("  Simple Avro vs JSON Client")
    print("=" * 60)
    print()

    client = AvroClient()

    # Check server health
    print("📍 Checking server health...")
    if not client.health_check():
        print("❌ Server not responding!")
        print("   Start the server with: python avro_server.py")
        return

    print("✓ Server is running!")
    print()

    # Single record test
    print("=" * 60)
    print("SINGLE RECORD TEST")
    print("=" * 60)
    print()

    print("📥 Fetching single Avro user...")
    avro_result = client.get_avro_single()
    print(f"✓ Received {avro_result['size_bytes']} bytes in {avro_result['time_ms']:.2f}ms")
    print("  Data:")
    print_user(avro_result["user"])
    print()

    print("📥 Fetching single JSON user...")
    json_result = client.get_json_single()
    print(f"✓ Received {json_result['size_bytes']} bytes in {json_result['time_ms']:.2f}ms")
    print("  Data:")
    print_user(json_result["user"])
    print()

    # Calculate difference
    size_reduction = ((json_result['size_bytes'] - avro_result['size_bytes']) / json_result['size_bytes']) * 100
    time_improvement = ((json_result['time_ms'] - avro_result['time_ms']) / json_result['time_ms']) * 100
    
    print("📊 SINGLE RECORD COMPARISON")
    print(f"  Avro is {size_reduction:.1f}% smaller ({avro_result['size_bytes']} vs {json_result['size_bytes']} bytes)")
    print(f"  Avro is {time_improvement:.1f}% faster ({avro_result['time_ms']:.2f}ms vs {json_result['time_ms']:.2f}ms)")
    print()

    # Batch test
    print("=" * 60)
    print("BATCH RECORDS TEST (10 users)")
    print("=" * 60)
    print()

    print("📥 Fetching batch Avro users...")
    avro_batch = client.get_avro_batch()
    print(f"✓ Received {avro_batch['count']} users in {avro_batch['size_bytes']} bytes ({avro_batch['time_ms']:.2f}ms)")
    print(f"  First user: {avro_batch['users'][0]['name']}")
    print()

    print("📥 Fetching batch JSON users...")
    json_batch = client.get_json_batch()
    print(f"✓ Received {json_batch['count']} users in {json_batch['size_bytes']} bytes ({json_batch['time_ms']:.2f}ms)")
    print(f"  First user: {json_batch['users'][0]['name']}")
    print()

    # Calculate batch differences
    batch_size_reduction = ((json_batch['size_bytes'] - avro_batch['size_bytes']) / json_batch['size_bytes']) * 100
    batch_time_improvement = ((json_batch['time_ms'] - avro_batch['time_ms']) / json_batch['time_ms']) * 100

    print("📊 BATCH RECORDS COMPARISON (10 users)")
    print(f"  Avro is {batch_size_reduction:.1f}% smaller ({avro_batch['size_bytes']} vs {json_batch['size_bytes']} bytes)")
    print(f"  Avro is {batch_time_improvement:.1f}% faster ({avro_batch['time_ms']:.2f}ms vs {json_batch['time_ms']:.2f}ms)")
    print()

    # Overall stats
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print()
    print("Format  | Single Record | Batch (10 users)")
    print("--------|---------------|------------------")
    print(f"Avro    | {avro_result['size_bytes']:6d} bytes  | {avro_batch['size_bytes']:6d} bytes")
    print(f"JSON    | {json_result['size_bytes']:6d} bytes  | {json_batch['size_bytes']:6d} bytes")
    print()
    print(f"🎯 Avro advantage: {size_reduction:.0f}% smaller for single records")
    print(f"🎯 Avro advantage: {batch_size_reduction:.0f}% smaller for batch records")
    print()


if __name__ == "__main__":
    main()
