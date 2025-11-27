from flask import Flask, request, jsonify
from avro.io import DatumWriter, DatumReader, BinaryEncoder, BinaryDecoder
from avro.schema import parse
import avro.schema
import json
import io
import os

app = Flask(__name__)

# Load schemas
script_dir = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(script_dir, 'user_v1.avsc'), 'r') as f:
    schema_v1 = parse(f.read())

with open(os.path.join(script_dir, 'user_v2.avsc'), 'r') as f:
    schema_v2 = parse(f.read())

# Store for in-memory data
users_db = {}

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "ok"}), 200

@app.route('/api/users/encode/v1', methods=['POST'])
def encode_v1():
    """
    Encode user data to Avro binary using schema v1
    Expected JSON: {"id": 1, "nom": "Alice", "age": 25}
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        if not all(k in data for k in ['id', 'nom', 'age']):
            return jsonify({"error": "Missing required fields: id, nom, age"}), 400
        
        # Encode to Avro binary
        writer = DatumWriter(schema_v1)
        bytes_io = io.BytesIO()
        encoder = BinaryEncoder(bytes_io)
        writer.write(data, encoder)
        
        avro_bytes = bytes_io.getvalue()
        
        return jsonify({
            "schema_version": "v1",
            "avro_binary": avro_bytes.hex(),
            "original_data": data
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/users/encode/v2', methods=['POST'])
def encode_v2():
    """
    Encode user data to Avro binary using schema v2
    Expected JSON: {"id": 1, "nom": "Alice", "age": 25, "email": "alice@example.com", "actif": true}
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        if not all(k in data for k in ['id', 'nom', 'age']):
            return jsonify({"error": "Missing required fields: id, nom, age"}), 400
        
        # Set defaults for optional fields
        if 'email' not in data:
            data['email'] = None
        if 'actif' not in data:
            data['actif'] = True
        
        # Encode to Avro binary
        writer = DatumWriter(schema_v2)
        bytes_io = io.BytesIO()
        encoder = BinaryEncoder(bytes_io)
        writer.write(data, encoder)
        
        avro_bytes = bytes_io.getvalue()
        
        return jsonify({
            "schema_version": "v2",
            "avro_binary": avro_bytes.hex(),
            "original_data": data
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/users/decode/v1', methods=['POST'])
def decode_v1():
    """
    Decode Avro binary data using schema v1
    Expected JSON: {"avro_binary": "hex_encoded_string"}
    """
    try:
        data = request.get_json()
        
        if 'avro_binary' not in data:
            return jsonify({"error": "Missing 'avro_binary' field"}), 400
        
        # Convert hex to bytes
        avro_bytes = bytes.fromhex(data['avro_binary'])
        
        # Decode from Avro binary
        reader = DatumReader(schema_v1)
        bytes_io = io.BytesIO(avro_bytes)
        decoder = BinaryDecoder(bytes_io)
        decoded_data = reader.read(decoder)
        
        return jsonify({
            "schema_version": "v1",
            "decoded_data": decoded_data
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/users/decode/v2', methods=['POST'])
def decode_v2():
    """
    Decode Avro binary data using schema v2
    Expected JSON: {"avro_binary": "hex_encoded_string"}
    """
    try:
        data = request.get_json()
        
        if 'avro_binary' not in data:
            return jsonify({"error": "Missing 'avro_binary' field"}), 400
        
        # Convert hex to bytes
        avro_bytes = bytes.fromhex(data['avro_binary'])
        
        # Decode from Avro binary
        reader = DatumReader(schema_v2)
        bytes_io = io.BytesIO(avro_bytes)
        decoder = BinaryDecoder(bytes_io)
        decoded_data = reader.read(decoder)
        
        return jsonify({
            "schema_version": "v2",
            "decoded_data": decoded_data
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/users/store', methods=['POST'])
def store_user():
    """
    Store user in memory as Avro binary using schema v2
    Expected JSON: {"id": 1, "nom": "Alice", "age": 25, "email": "alice@example.com", "actif": true}
    """
    try:
        data = request.get_json()
        
        if not all(k in data for k in ['id', 'nom', 'age']):
            return jsonify({"error": "Missing required fields: id, nom, age"}), 400
        
        user_id = data['id']
        
        # Set defaults
        if 'email' not in data:
            data['email'] = None
        if 'actif' not in data:
            data['actif'] = True
        
        # Encode to Avro
        writer = DatumWriter(schema_v2)
        bytes_io = io.BytesIO()
        encoder = BinaryEncoder(bytes_io)
        writer.write(data, encoder)
        
        users_db[user_id] = bytes_io.getvalue()
        
        return jsonify({
            "message": f"User {user_id} stored successfully",
            "user_data": data
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Retrieve stored user by ID"""
    try:
        if user_id not in users_db:
            return jsonify({"error": f"User {user_id} not found"}), 404
        
        # Decode from Avro
        avro_bytes = users_db[user_id]
        reader = DatumReader(schema_v2)
        bytes_io = io.BytesIO(avro_bytes)
        decoder = BinaryDecoder(bytes_io)
        decoded_data = reader.read(decoder)
        
        return jsonify({
            "user_id": user_id,
            "data": decoded_data
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/users', methods=['GET'])
def list_users():
    """List all stored users"""
    try:
        users_list = []
        for user_id, avro_bytes in users_db.items():
            reader = DatumReader(schema_v2)
            bytes_io = io.BytesIO(avro_bytes)
            decoder = BinaryDecoder(bytes_io)
            decoded_data = reader.read(decoder)
            users_list.append(decoded_data)
        
        return jsonify({
            "total": len(users_list),
            "users": users_list
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete a user by ID"""
    try:
        if user_id not in users_db:
            return jsonify({"error": f"User {user_id} not found"}), 404
        
        del users_db[user_id]
        return jsonify({"message": f"User {user_id} deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/schema/v1', methods=['GET'])
def get_schema_v1():
    """Get schema v1"""
    return jsonify(json.loads(schema_v1.to_json())), 200

@app.route('/api/schema/v2', methods=['GET'])
def get_schema_v2():
    """Get schema v2"""
    return jsonify(json.loads(schema_v2.to_json())), 200

if __name__ == '__main__':
    print("Starting Avro REST API Server...")
    print("Available endpoints:")
    print("  GET  /health                      - Health check")
    print("  POST /api/users/encode/v1         - Encode data with schema v1")
    print("  POST /api/users/encode/v2         - Encode data with schema v2")
    print("  POST /api/users/decode/v1         - Decode Avro binary with schema v1")
    print("  POST /api/users/decode/v2         - Decode Avro binary with schema v2")
    print("  POST /api/users/store             - Store user (Avro binary)")
    print("  GET  /api/users                   - List all users")
    print("  GET  /api/users/<id>              - Get user by ID")
    print("  DELETE /api/users/<id>            - Delete user by ID")
    print("  GET  /api/schema/v1               - Get schema v1")
    print("  GET  /api/schema/v2               - Get schema v2")
    app.run(debug=True, host='0.0.0.0', port=5000)
