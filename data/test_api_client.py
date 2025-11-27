import requests
import json
from time import sleep

BASE_URL = "http://localhost:5000"

def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def test_health():
    print_section("1. Testing Health Check")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

def test_get_schemas():
    print_section("2. Getting Schemas")
    
    response_v1 = requests.get(f"{BASE_URL}/api/schema/v1")
    print("Schema V1:")
    print(json.dumps(response_v1.json(), indent=2))
    
    response_v2 = requests.get(f"{BASE_URL}/api/schema/v2")
    print("\nSchema V2:")
    print(json.dumps(response_v2.json(), indent=2))

def test_encode_decode_v1():
    print_section("3. Testing Encode/Decode V1")
    
    user_data = {"id": 1, "nom": "Alice", "age": 25}
    print(f"Original Data: {user_data}")
    
    # Encode
    encode_response = requests.post(f"{BASE_URL}/api/users/encode/v1", json=user_data)
    print(f"\nEncoded Response: {encode_response.status_code}")
    encoded = encode_response.json()
    print(json.dumps(encoded, indent=2))
    
    # Decode
    avro_binary = encoded['avro_binary']
    decode_response = requests.post(f"{BASE_URL}/api/users/decode/v1", 
                                     json={"avro_binary": avro_binary})
    print(f"\nDecoded Response: {decode_response.status_code}")
    decoded = decode_response.json()
    print(json.dumps(decoded, indent=2))

def test_encode_decode_v2():
    print_section("4. Testing Encode/Decode V2")
    
    user_data = {
        "id": 2, 
        "nom": "Bob", 
        "age": 30,
        "email": "bob@example.com",
        "actif": True
    }
    print(f"Original Data: {user_data}")
    
    # Encode
    encode_response = requests.post(f"{BASE_URL}/api/users/encode/v2", json=user_data)
    print(f"\nEncoded Response: {encode_response.status_code}")
    encoded = encode_response.json()
    print(json.dumps(encoded, indent=2))
    
    # Decode
    avro_binary = encoded['avro_binary']
    decode_response = requests.post(f"{BASE_URL}/api/users/decode/v2", 
                                     json={"avro_binary": avro_binary})
    print(f"\nDecoded Response: {decode_response.status_code}")
    decoded = decode_response.json()
    print(json.dumps(decoded, indent=2))

def test_store_and_retrieve():
    print_section("5. Testing Store and Retrieve")
    
    users = [
        {"id": 101, "nom": "Charlie", "age": 28, "email": "charlie@example.com", "actif": True},
        {"id": 102, "nom": "Diana", "age": 32, "email": "diana@example.com", "actif": False},
        {"id": 103, "nom": "Eve", "age": 26, "email": None, "actif": True},
    ]
    
    print("Storing users...")
    for user in users:
        response = requests.post(f"{BASE_URL}/api/users/store", json=user)
        print(f"  Stored {user['nom']}: {response.status_code}")
    
    print("\nRetrieving all users...")
    response = requests.get(f"{BASE_URL}/api/users")
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    
    print("\nRetrieving specific user (ID=101)...")
    response = requests.get(f"{BASE_URL}/api/users/101")
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))

def test_delete():
    print_section("6. Testing Delete")
    
    print("Deleting user ID=101...")
    response = requests.delete(f"{BASE_URL}/api/users/101")
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    
    print("\nListing remaining users...")
    response = requests.get(f"{BASE_URL}/api/users")
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))

def test_schema_compatibility():
    print_section("7. Testing Schema Compatibility")
    
    # V1 data with v2 schema decode should work (forward compatibility)
    print("Encoding with V1, then decoding with V2 (testing compatibility)...")
    
    v1_data = {"id": 999, "nom": "Test User", "age": 40}
    
    encode_response = requests.post(f"{BASE_URL}/api/users/encode/v1", json=v1_data)
    avro_binary = encode_response.json()['avro_binary']
    
    # Try to decode V1 data with V2 schema
    decode_response = requests.post(f"{BASE_URL}/api/users/decode/v2",
                                     json={"avro_binary": avro_binary})
    print(f"Decode with V2: {decode_response.status_code}")
    if decode_response.status_code == 200:
        print("✓ Forward compatible!")
        print(json.dumps(decode_response.json(), indent=2))
    else:
        print("✗ Not compatible")
        print(decode_response.json())

if __name__ == "__main__":
    try:
        print("Avro REST API Client Test Suite")
        print("Waiting for API to be ready...")
        sleep(1)
        
        test_health()
        test_get_schemas()
        test_encode_decode_v1()
        test_encode_decode_v2()
        test_store_and_retrieve()
        test_delete()
        test_schema_compatibility()
        
        print_section("Tests Completed!")
        
    except requests.exceptions.ConnectionError:
        print("ERROR: Cannot connect to API server!")
        print(f"Make sure the server is running at {BASE_URL}")
        print("Run: python api_server.py")
