#!/usr/bin/env python
"""
Test client for Avro REST API
Tests both JSON and Avro endpoints
"""

import requests
import json
import avro.schema
import avro.io
import io
from datetime import datetime

BASE_URL = "http://localhost:5000"

# Avro schema for encoding/decoding
USER_SCHEMA_STR = """
{
  "type": "record",
  "name": "User",
  "namespace": "com.example",
  "fields": [
    { "name": "id", "type": "long" },
    { "name": "nom", "type": "string" },
    { "name": "email", "type": "string" },
    { "name": "age", "type": "int" },
    { "name": "created_at", "type": "string" }
  ]
}
"""

user_schema = avro.schema.parse(USER_SCHEMA_STR)

def encode_avro(record):
    """Encode a record to Avro binary format"""
    writer = avro.io.DatumWriter(user_schema)
    bytes_writer = io.BytesIO()
    encoder = avro.io.BinaryEncoder(bytes_writer)
    writer.write(record, encoder)
    return bytes_writer.getvalue()

def decode_avro(data):
    """Decode Avro binary data to record"""
    bytes_reader = io.BytesIO(data)
    decoder = avro.io.BinaryDecoder(bytes_reader)
    reader = avro.io.DatumReader(user_schema)
    return reader.read(decoder)

# ==================== JSON API TESTS ====================

def test_json_api():
    print("\n" + "="*60)
    print("TESTING JSON REST API")
    print("="*60)
    
    # Get all users
    print("\n1. GET /api/json/users")
    resp = requests.get(f"{BASE_URL}/api/json/users")
    print(f"Status: {resp.status_code}")
    print(f"Response: {json.dumps(resp.json(), indent=2)}")
    
    # Get specific user
    print("\n2. GET /api/json/users/1")
    resp = requests.get(f"{BASE_URL}/api/json/users/1")
    print(f"Status: {resp.status_code}")
    print(f"Response: {json.dumps(resp.json(), indent=2)}")
    
    # Create new user
    print("\n3. POST /api/json/users")
    new_user = {
        "nom": "Charlie",
        "email": "charlie@example.com",
        "age": 28
    }
    resp = requests.post(f"{BASE_URL}/api/json/users", json=new_user)
    print(f"Status: {resp.status_code}")
    print(f"Response: {json.dumps(resp.json(), indent=2)}")
    
    # Update user
    print("\n4. PUT /api/json/users/1")
    update_data = {
        "nom": "Alice Updated",
        "age": 26
    }
    resp = requests.put(f"{BASE_URL}/api/json/users/1", json=update_data)
    print(f"Status: {resp.status_code}")
    print(f"Response: {json.dumps(resp.json(), indent=2)}")

# ==================== AVRO API TESTS ====================

def test_avro_api():
    print("\n" + "="*60)
    print("TESTING AVRO REST API")
    print("="*60)
    
    # Get specific user as Avro
    print("\n1. GET /api/avro/users/1 (Avro binary)")
    resp = requests.get(f"{BASE_URL}/api/avro/users/1")
    print(f"Status: {resp.status_code}")
    print(f"Content-Type: {resp.headers.get('content-type')}")
    print(f"Binary size: {len(resp.content)} bytes")
    
    # Decode and display
    try:
        user = decode_avro(resp.content)
        print(f"Decoded: {json.dumps(user, indent=2)}")
    except Exception as e:
        print(f"Error decoding: {e}")
    
    # Create user with Avro
    print("\n2. POST /api/avro/users (Create with Avro binary)")
    new_user = {
        "id": 0,  # Will be assigned by server
        "nom": "David",
        "email": "david@example.com",
        "age": 32,
        "created_at": datetime.now().isoformat()
    }
    avro_data = encode_avro(new_user)
    resp = requests.post(f"{BASE_URL}/api/avro/users", data=avro_data)
    print(f"Status: {resp.status_code}")
    print(f"Response: {json.dumps(resp.json(), indent=2)}")
    
    # Update user with Avro
    print("\n3. PUT /api/avro/users/2 (Update with Avro binary)")
    update_user = {
        "id": 2,
        "nom": "Bob Updated",
        "email": "bob.updated@example.com",
        "age": 31,
        "created_at": "2024-02-20T14:45:00"
    }
    avro_data = encode_avro(update_user)
    resp = requests.put(f"{BASE_URL}/api/avro/users/2", data=avro_data)
    print(f"Status: {resp.status_code}")
    print(f"Response: {json.dumps(resp.json(), indent=2)}")

# ==================== SCHEMA TEST ====================

def test_schema():
    print("\n" + "="*60)
    print("TESTING SCHEMA ENDPOINT")
    print("="*60)
    
    print("\nGET /api/schema")
    resp = requests.get(f"{BASE_URL}/api/schema")
    print(f"Status: {resp.status_code}")
    print(f"Response: {json.dumps(resp.json(), indent=2)}")

# ==================== HEALTH CHECK ====================

def test_health():
    print("\n" + "="*60)
    print("TESTING HEALTH CHECK")
    print("="*60)
    
    print("\nGET /health")
    resp = requests.get(f"{BASE_URL}/health")
    print(f"Status: {resp.status_code}")
    print(f"Response: {json.dumps(resp.json(), indent=2)}")

# ==================== DOCUMENTATION ====================

def test_documentation():
    print("\n" + "="*60)
    print("API DOCUMENTATION")
    print("="*60)
    
    print("\nGET /")
    resp = requests.get(f"{BASE_URL}/")
    print(f"Status: {resp.status_code}")
    print(json.dumps(resp.json(), indent=2))

if __name__ == "__main__":
    try:
        print("Waiting for API to be ready...")
        import time
        time.sleep(2)
        
        # Run tests
        test_documentation()
        test_health()
        test_schema()
        test_json_api()
        test_avro_api()
        
        print("\n" + "="*60)
        print("ALL TESTS COMPLETED")
        print("="*60)
        
    except requests.exceptions.ConnectionError:
        print("ERROR: Cannot connect to API at", BASE_URL)
        print("Make sure the API is running: docker compose -f docker-compose.avro.yml up")
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
