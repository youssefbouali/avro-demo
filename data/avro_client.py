#!/usr/bin/env python3
"""
Simple Avro vs JSON Client (Size Comparison Only)
Fetches and compares payload sizes of Avro vs JSON data
"""

import urllib.request
import json
import fastavro
import io
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
    """Simple Avro/JSON client focused on payload size comparison"""

    def __init__(self, server_url="http://localhost:8000"):
        self.server_url = server_url

    def get_avro_single(self):
        url = f"{self.server_url}/avro/single"
        response = urllib.request.urlopen(url)
        data = response.read()
        fo = io.BytesIO(data)
        user = fastavro.schemaless_reader(fo, SCHEMA)
        return {"user": user, "size_bytes": len(data), "format": "Avro"}

    def get_avro_batch(self):
        url = f"{self.server_url}/avro/batch"
        response = urllib.request.urlopen(url)
        data = response.read()
        fo = io.BytesIO(data)
        users = list(fastavro.reader(fo))
        return {"users": users, "count": len(users), "size_bytes": len(data), "format": "Avro"}

    def get_json_single(self):
        url = f"{self.server_url}/json/single"
        response = urllib.request.urlopen(url)
        data = response.read()
        user = json.loads(data.decode())
        return {"user": user, "size_bytes": len(data), "format": "JSON"}

    def get_json_batch(self):
        url = f"{self.server_url}/json/batch"
        response = urllib.request.urlopen(url)
        data = response.read()
        users = json.loads(data.decode())
        return {"users": users, "count": len(users), "size_bytes": len(data), "format": "JSON"}

    def health_check(self):
        try:
            response = urllib.request.urlopen(f"{self.server_url}/health")
            data = json.loads(response.read().decode())
            return data.get("status") == "ok"
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
    print("=" * 60)
    print("  Avro vs JSON — Payload Size Comparison")
    print("=" * 60)
    print()

    client = AvroClient()

    print("Checking server health...")
    if not client.health_check():
        print("Server not responding!")
        print("   Start the server with: python avro_server.py")
        return
    print("Server is running!")
    print()

    # Single record test
    print("=" * 60)
    print("SINGLE RECORD SIZE COMPARISON")
    print("=" * 60)
    print()

    print("Fetching single Avro record...")
    avro_single = client.get_avro_single()
    print(f"Avro:  {avro_single['size_bytes']} bytes")
    print_user(avro_single["user"])
    print()

    print("Fetching single JSON record...")
    json_single = client.get_json_single()
    print(f"JSON:  {json_single['size_bytes']} bytes")
    print_user(json_single["user"])
    print()

    size_reduction_single = ((json_single['size_bytes'] - avro_single['size_bytes']) / json_single['size_bytes']) * 100

    print("RESULT")
    print(f"  Avro is {size_reduction_single:.1f}% smaller than JSON")
    print(f"  ({avro_single['size_bytes']} bytes vs {json_single['size_bytes']} bytes)")
    print()

    # Batch test
    print("=" * 60)
    print("BATCH RECORDS SIZE COMPARISON (10 users)")
    print("=" * 60)
    print()

    print("Fetching Avro batch...")
    avro_batch = client.get_avro_batch()
    print(f"Avro batch: {avro_batch['size_bytes']} bytes ({avro_batch['count']} users)")
    print(f"  First user: {avro_batch['users'][0]['name']}")
    print()

    print("Fetching JSON batch...")
    json_batch = client.get_json_batch()
    print(f"JSON batch: {json_batch['size_bytes']} bytes ({json_batch['count']} users)")
    print(f"  First user: {json_batch['users'][0]['name']}")
    print()

    size_reduction_batch = ((json_batch['size_bytes'] - avro_batch['size_bytes']) / json_batch['size_bytes']) * 100

    print("RESULT")
    print(f"  Avro is {size_reduction_batch:.1f}% smaller than JSON for batch data")
    print(f"  ({avro_batch['size_bytes']} bytes vs {json_batch['size_bytes']} bytes)")
    print()

    # Summary table
    print("=" * 60)
    print("SUMMARY — PAYLOAD SIZES")
    print("=" * 60)
    print()
    print("Format  | Single Record | Batch (10 users)")
    print("--------|---------------|------------------")
    print(f"Avro    | {avro_single['size_bytes']:6d} bytes     | {avro_batch['size_bytes']:7d} bytes")
    print(f"JSON    | {json_single['size_bytes']:6d} bytes     | {json_batch['size_bytes']:7d} bytes")
    print()
    print(f"Avro saves ~{size_reduction_single:.0f}% on single records")
    print(f"Avro saves ~{size_reduction_batch:.0f}% on batch transfers")
    print()


if __name__ == "__main__":
    main()