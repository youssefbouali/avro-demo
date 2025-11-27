from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import avro.schema
import avro.io
import io
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Define Avro schema
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

# In-memory storage
users_db = {
    1: {
        "id": 1,
        "nom": "Alice",
        "email": "alice@example.com",
        "age": 25,
        "created_at": "2024-01-15T10:30:00"
    },
    2: {
        "id": 2,
        "nom": "Bob",
        "email": "bob@example.com",
        "age": 30,
        "created_at": "2024-02-20T14:45:00"
    }
}

# ==================== JSON REST API ENDPOINTS ====================

@app.route('/api/json/users', methods=['GET'])
def get_users_json():
    """Get all users as JSON"""
    return jsonify(list(users_db.values())), 200

@app.route('/api/json/users/<int:user_id>', methods=['GET'])
def get_user_json(user_id):
    """Get a specific user as JSON"""
    if user_id not in users_db:
        return jsonify({"error": "User not found"}), 404
    return jsonify(users_db[user_id]), 200

@app.route('/api/json/users', methods=['POST'])
def create_user_json():
    """Create a new user with JSON"""
    data = request.get_json()
    
    if not data or not all(k in data for k in ['nom', 'email', 'age']):
        return jsonify({"error": "Missing required fields: nom, email, age"}), 400
    
    user_id = max(users_db.keys()) + 1 if users_db else 1
    user = {
        "id": user_id,
        "nom": data['nom'],
        "email": data['email'],
        "age": data['age'],
        "created_at": datetime.now().isoformat()
    }
    
    users_db[user_id] = user
    return jsonify(user), 201

@app.route('/api/json/users/<int:user_id>', methods=['PUT'])
def update_user_json(user_id):
    """Update a user with JSON"""
    if user_id not in users_db:
        return jsonify({"error": "User not found"}), 404
    
    data = request.get_json()
    user = users_db[user_id]
    
    if 'nom' in data:
        user['nom'] = data['nom']
    if 'email' in data:
        user['email'] = data['email']
    if 'age' in data:
        user['age'] = data['age']
    
    return jsonify(user), 200

@app.route('/api/json/users/<int:user_id>', methods=['DELETE'])
def delete_user_json(user_id):
    """Delete a user"""
    if user_id not in users_db:
        return jsonify({"error": "User not found"}), 404
    
    deleted_user = users_db.pop(user_id)
    return jsonify({"message": "User deleted", "user": deleted_user}), 200

# ==================== AVRO REST API ENDPOINTS ====================

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

@app.route('/api/avro/users', methods=['GET'])
def get_users_avro():
    """Get all users as Avro binary"""
    users_list = list(users_db.values())
    response_data = json.dumps(users_list).encode('utf-8')
    return Response(response_data, mimetype='application/octet-stream', 
                   headers={"Content-Disposition": "attachment; filename=users.avro"})

@app.route('/api/avro/users/<int:user_id>', methods=['GET'])
def get_user_avro(user_id):
    """Get a specific user as Avro binary"""
    if user_id not in users_db:
        return jsonify({"error": "User not found"}), 404
    
    user = users_db[user_id]
    avro_data = encode_avro(user)
    return Response(avro_data, mimetype='application/octet-stream',
                   headers={"Content-Disposition": f"attachment; filename=user_{user_id}.avro"})

@app.route('/api/avro/users', methods=['POST'])
def create_user_avro():
    """Create a new user from Avro binary"""
    try:
        avro_data = request.get_data()
        user = decode_avro(avro_data)
        
        user_id = max(users_db.keys()) + 1 if users_db else 1
        user['id'] = user_id
        user['created_at'] = datetime.now().isoformat()
        
        users_db[user_id] = user
        return jsonify(user), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/avro/users/<int:user_id>', methods=['PUT'])
def update_user_avro(user_id):
    """Update a user from Avro binary"""
    if user_id not in users_db:
        return jsonify({"error": "User not found"}), 404
    
    try:
        avro_data = request.get_data()
        updated_fields = decode_avro(avro_data)
        user = users_db[user_id]
        
        for key in ['nom', 'email', 'age']:
            if key in updated_fields:
                user[key] = updated_fields[key]
        
        return jsonify(user), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# ==================== SCHEMA ENDPOINT ====================

@app.route('/api/schema', methods=['GET'])
def get_schema():
    """Get the Avro schema"""
    return jsonify(json.loads(USER_SCHEMA_STR)), 200

# ==================== HEALTH CHECK ====================

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "users_count": len(users_db)
    }), 200

# ==================== API DOCUMENTATION ====================

@app.route('/', methods=['GET'])
def documentation():
    """API documentation"""
    docs = {
        "title": "Avro REST API",
        "version": "1.0.0",
        "description": "Dual REST API supporting both JSON and Avro formats",
        "endpoints": {
            "JSON_API": {
                "GET /api/json/users": "Get all users as JSON",
                "GET /api/json/users/<id>": "Get a specific user as JSON",
                "POST /api/json/users": "Create a new user with JSON body",
                "PUT /api/json/users/<id>": "Update a user with JSON body",
                "DELETE /api/json/users/<id>": "Delete a user"
            },
            "AVRO_API": {
                "GET /api/avro/users": "Get all users (JSON format)",
                "GET /api/avro/users/<id>": "Get a specific user as Avro binary",
                "POST /api/avro/users": "Create a user from Avro binary body",
                "PUT /api/avro/users/<id>": "Update a user from Avro binary body"
            },
            "SCHEMA": {
                "GET /api/schema": "Get the Avro schema"
            },
            "HEALTH": {
                "GET /health": "Health check endpoint"
            }
        },
        "example_json_user": {
            "id": 1,
            "nom": "Alice",
            "email": "alice@example.com",
            "age": 25,
            "created_at": "2024-01-15T10:30:00"
        }
    }
    return jsonify(docs), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
