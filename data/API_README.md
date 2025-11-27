# Avro REST API - Test Without Kafka

This is a Flask-based REST API server for testing Avro serialization/deserialization without requiring Kafka.

## Features

- ✓ Encode/Decode Avro data with schema v1 and v2
- ✓ In-memory user storage with Avro binary format
- ✓ Schema compatibility testing (v1 ↔ v2)
- ✓ Full CRUD operations on users
- ✓ RESTful API with JSON payloads

## Installation

```bash
# Install dependencies
pip install -r requirements_api.txt
```

## Running the Server

```bash
# Start the API server
python api_server.py
```

The server will start on `http://localhost:5000`

## Running Tests

In another terminal:

```bash
# Run the comprehensive test suite
python test_api_client.py
```

## API Endpoints

### Health & Info
- `GET /health` - Health check
- `GET /api/schema/v1` - Get schema v1
- `GET /api/schema/v2` - Get schema v2

### Encoding/Decoding
- `POST /api/users/encode/v1` - Encode data with schema v1
- `POST /api/users/encode/v2` - Encode data with schema v2
- `POST /api/users/decode/v1` - Decode Avro binary with schema v1
- `POST /api/users/decode/v2` - Decode Avro binary with schema v2

### Storage Operations
- `POST /api/users/store` - Store user (stored as Avro binary)
- `GET /api/users` - List all stored users
- `GET /api/users/<id>` - Get user by ID
- `DELETE /api/users/<id>` - Delete user by ID

## Example Usage

### 1. Encode with Schema V1

```bash
curl -X POST http://localhost:5000/api/users/encode/v1 \
  -H "Content-Type: application/json" \
  -d '{
    "id": 1,
    "nom": "Alice",
    "age": 25
  }'
```

Response:
```json
{
  "schema_version": "v1",
  "avro_binary": "00020a416c6963671832",
  "original_data": {
    "id": 1,
    "nom": "Alice",
    "age": 25
  }
}
```

### 2. Decode Binary Data

```bash
curl -X POST http://localhost:5000/api/users/decode/v1 \
  -H "Content-Type: application/json" \
  -d '{
    "avro_binary": "00020a416c6963671832"
  }'
```

Response:
```json
{
  "schema_version": "v1",
  "decoded_data": {
    "id": 1,
    "nom": "Alice",
    "age": 25
  }
}
```

### 3. Encode with Schema V2 (with optional fields)

```bash
curl -X POST http://localhost:5000/api/users/encode/v2 \
  -H "Content-Type: application/json" \
  -d '{
    "id": 2,
    "nom": "Bob",
    "age": 30,
    "email": "bob@example.com",
    "actif": true
  }'
```

### 4. Store User

```bash
curl -X POST http://localhost:5000/api/users/store \
  -H "Content-Type: application/json" \
  -d '{
    "id": 101,
    "nom": "Charlie",
    "age": 28,
    "email": "charlie@example.com",
    "actif": true
  }'
```

### 5. List All Users

```bash
curl http://localhost:5000/api/users
```

### 6. Get Specific User

```bash
curl http://localhost:5000/api/users/101
```

### 7. Delete User

```bash
curl -X DELETE http://localhost:5000/api/users/101
```

## Schema Versions

### Schema V1
```json
{
  "type": "record",
  "name": "User",
  "namespace": "com.example",
  "fields": [
    { "name": "id", "type": "long" },
    { "name": "nom", "type": "string" },
    { "name": "age", "type": "int" }
  ]
}
```

### Schema V2 (Extended with optional fields)
```json
{
  "type": "record",
  "name": "User",
  "namespace": "com.example",
  "fields": [
    { "name": "id", "type": "long" },
    { "name": "nom", "type": "string" },
    { "name": "age", "type": "int" },
    { "name": "email", "type": ["null", "string"], "default": null },
    { "name": "actif", "type": "boolean", "default": true }
  ]
}
```

## Testing Schema Compatibility

The API allows you to test forward/backward compatibility:

1. **Encode with V1, Decode with V2** - Tests forward compatibility
2. **Encode with V2, Decode with V1** - Would test backward compatibility (data loss expected)

Run the full test suite to see compatibility tests in action:

```bash
python test_api_client.py
```

## Architecture

- **api_server.py** - Flask REST API server with Avro serialization
- **test_api_client.py** - Comprehensive test suite
- **user_v1.avsc** - Avro schema v1
- **user_v2.avsc** - Avro schema v2
- **requirements_api.txt** - Python dependencies

## Notes

- The server uses in-memory storage (data is lost on restart)
- Avro binary data is returned as hex strings in JSON
- All timestamps and sensitive data handling should be added as needed
- For production use, add authentication, logging, and persistent storage
