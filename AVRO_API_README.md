# Avro REST API - Dual JSON/Avro Server

A Flask-based REST API server that supports both JSON and Avro binary formats without requiring Kafka. Perfect for testing and development.

## Features

✅ **JSON REST API** - Standard JSON endpoints for CRUD operations
✅ **Avro Binary API** - Avro binary format endpoints for efficient serialization
✅ **No Kafka Required** - Standalone container, no external dependencies
✅ **In-Memory Storage** - Quick testing without database setup
✅ **CORS Enabled** - Ready for web client integration
✅ **Comprehensive Tests** - Full test suite included

## Project Structure

```
avro-demo/
├── avro_rest_api.py          # Main Flask API application
├── test_avro_api.py          # Test client script
├── Dockerfile.avro           # Docker image for API
├── docker-compose.avro.yml   # Docker Compose configuration
└── README.md                 # This file
```

## Quick Start

### Using Docker Compose (Recommended)

```powershell
# Navigate to project directory
cd avro-demo

# Build and start the API server
docker compose -f docker-compose.avro.yml up -d

# Wait for container to be ready
Start-Sleep -Seconds 3

# Run the test suite
docker compose -f docker-compose.avro.yml exec avro-api python test_avro_api.py

# View logs
docker compose -f docker-compose.avro.yml logs -f avro-api

# Stop the server
docker compose -f docker-compose.avro.yml down
```

### Running Locally (Without Docker)

```powershell
# Install dependencies
pip install flask flask-cors avro-python3

# Run the API
python avro_rest_api.py

# In another terminal, run tests
python test_avro_api.py
```

## API Endpoints

### JSON REST API

```
GET    /api/json/users           - Get all users
GET    /api/json/users/<id>      - Get user by ID
POST   /api/json/users           - Create new user
PUT    /api/json/users/<id>      - Update user
DELETE /api/json/users/<id>      - Delete user
```

**Example Request (JSON):**
```powershell
# Create user with JSON
$body = @{
    nom = "John"
    email = "john@example.com"
    age = 30
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5000/api/json/users" `
    -Method POST `
    -ContentType "application/json" `
    -Body $body
```

### Avro Binary API

```
GET    /api/avro/users           - Get all users (JSON)
GET    /api/avro/users/<id>      - Get user as Avro binary
POST   /api/avro/users           - Create user from Avro binary
PUT    /api/avro/users/<id>      - Update user from Avro binary
```

### Schema Endpoint

```
GET    /api/schema               - Get Avro schema definition
```

### Health & Documentation

```
GET    /health                   - Health check
GET    /                          - API documentation
```

## User Schema

```json
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
```

## Sample Data

The API comes pre-loaded with sample users:

```json
{
  "1": {
    "id": 1,
    "nom": "Alice",
    "email": "alice@example.com",
    "age": 25,
    "created_at": "2024-01-15T10:30:00"
  },
  "2": {
    "id": 2,
    "nom": "Bob",
    "email": "bob@example.com",
    "age": 30,
    "created_at": "2024-02-20T14:45:00"
  }
}
```

## Testing with curl

### JSON Endpoints

```bash
# Get all users
curl http://localhost:5000/api/json/users

# Get user by ID
curl http://localhost:5000/api/json/users/1

# Create user
curl -X POST http://localhost:5000/api/json/users \
  -H "Content-Type: application/json" \
  -d '{"nom":"Charlie","email":"charlie@example.com","age":28}'

# Update user
curl -X PUT http://localhost:5000/api/json/users/1 \
  -H "Content-Type: application/json" \
  -d '{"nom":"Alice Updated","age":26}'

# Delete user
curl -X DELETE http://localhost:5000/api/json/users/1
```

### Health Check

```bash
curl http://localhost:5000/health
```

### API Documentation

```bash
curl http://localhost:5000/ | jq
```

## Docker Commands

```powershell
# Build the image
docker build -f Dockerfile.avro -t avro-api:latest .

# Run container
docker run -p 5000:5000 avro-api:latest

# Run with volume mount (for development)
docker run -p 5000:5000 -v ${PWD}:/app avro-api:latest

# View logs
docker logs <container_id>

# Open bash shell
docker exec -it <container_id> bash
```

## Python Test Script

The included `test_avro_api.py` tests all endpoints:

```powershell
# Run locally
python test_avro_api.py

# Run in container
docker compose -f docker-compose.avro.yml exec avro-api python test_avro_api.py
```

## Environment Variables

In `docker-compose.avro.yml`:

- `FLASK_ENV`: Set to `development` for auto-reload
- `FLASK_APP`: Application entry point

## Troubleshooting

**Container won't start:**
```powershell
docker compose -f docker-compose.avro.yml logs avro-api
```

**Port 5000 already in use:**
```powershell
# Change port in docker-compose.avro.yml
# ports:
#   - "5001:5000"  # Use 5001 instead
```

**Cannot connect to API:**
```powershell
# Check if container is running
docker compose -f docker-compose.avro.yml ps

# Restart service
docker compose -f docker-compose.avro.yml restart
```

## Architecture

```
┌─────────────────────────────────────┐
│   Docker Container (Python:3.11)    │
├─────────────────────────────────────┤
│                                     │
│   ┌─────────────────────────────┐   │
│   │   Flask Application         │   │
│   │  avro_rest_api.py          │   │
│   └─────────────────────────────┘   │
│            │              │          │
│      ┌─────┴──────┬──────┴────┐    │
│      │            │           │     │
│   ┌──▼────┐   ┌──▼────┐  ┌──▼────┐ │
│   │ JSON  │   │ Avro  │  │Schema │ │
│   │ REST  │   │ Binary│  │Health │ │
│   │ API   │   │ API   │  │ Docs  │ │
│   └───────┘   └───────┘  └───────┘ │
│                                     │
│   In-Memory User Database           │
│                                     │
└─────────────────────────────────────┘
         Port: 5000
```

## Next Steps

- Integrate with real database (PostgreSQL, MongoDB)
- Add authentication (JWT tokens)
- Implement pagination and filtering
- Add data validation and error handling
- Deploy to Kubernetes
- Add metrics and monitoring

## Requirements

- Docker & Docker Compose
- OR Python 3.11+ with pip

## Dependencies

- Flask 3.0.0
- Flask-CORS 4.0.0
- Avro Python 3 1.12.1

## License

MIT

## Support

For issues or questions, check the API documentation at `http://localhost:5000/`
