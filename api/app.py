from flask import Flask, Response, jsonify, send_file
from flask_cors import CORS
import json
import random
import time
import io
import fastavro
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# Avro schema for User data
USER_SCHEMA = {
    "type": "record",
    "name": "User",
    "namespace": "com.example",
    "fields": [
        {"name": "id", "type": "long"},
        {"name": "name", "type": "string"},
        {"name": "email", "type": "string"},
        {"name": "age", "type": "int"},
        {"name": "country", "type": "string"},
        {"name": "created_at", "type": "string"},
        {"name": "score", "type": "double"},
        {"name": "active", "type": "boolean"}
    ]
}

# Sample data templates
NAMES = ["Alice", "Bob", "Charlie", "Diana", "Edward", "Fiona", "George", "Hannah", "Isaac", "Julia"]
EMAILS = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "example.com"]
COUNTRIES = ["USA", "UK", "France", "Germany", "Japan", "Canada", "Australia", "Brazil", "India", "Mexico"]

def generate_user():
    """Generate a random user record"""
    return {
        "id": random.randint(1, 10000),
        "name": random.choice(NAMES),
        "email": f"{random.randint(100, 9999)}@{random.choice(EMAILS)}",
        "age": random.randint(18, 80),
        "country": random.choice(COUNTRIES),
        "created_at": datetime.utcnow().isoformat(),
        "score": round(random.uniform(0, 100), 2),
        "active": random.choice([True, False])
    }

@app.route('/', methods=['GET'])
def index():
    """Serve the dashboard HTML"""
    try:
        return send_file('index.html', mimetype='text/html')
    except:
        return jsonify({"error": "index.html not found"}), 404

@app.route('/index.html', methods=['GET'])
def index_html():
    """Serve the dashboard HTML via /index.html path"""
    try:
        return send_file('index.html', mimetype='text/html')
    except:
        return jsonify({"error": "index.html not found"}), 404

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "ok"})

@app.route('/api/json/stream', methods=['GET'])
def json_stream():
    """Stream data as JSON"""
    def generate():
        try:
            for i in range(100):
                user = generate_user()
                start_time = time.time()
                json_data = json.dumps(user)
                end_time = time.time()
                
                response = {
                    "sequence": i + 1,
                    "data": user,
                    "format": "json",
                    "size_bytes": len(json_data.encode()),
                    "processing_time_ms": (end_time - start_time) * 1000,
                    "timestamp": datetime.utcnow().isoformat()
                }
                yield json.dumps(response) + "\n"
                time.sleep(0.05)  # Small delay between records
        except GeneratorExit:
            pass
    
    return Response(generate(), mimetype='application/json')

@app.route('/api/avro/stream', methods=['GET'])
def avro_stream():
    """Stream data as Avro (base64 encoded for HTTP)"""
    import base64
    
    def generate():
        try:
            for i in range(100):
                user = generate_user()
                
                # Encode to Avro
                start_time = time.time()
                fo = io.BytesIO()
                fastavro.schemaless_writer(fo, USER_SCHEMA, user)
                avro_bytes = fo.getvalue()
                end_time = time.time()
                
                response = {
                    "sequence": i + 1,
                    "data": base64.b64encode(avro_bytes).decode('utf-8'),
                    "format": "avro",
                    "size_bytes": len(avro_bytes),
                    "processing_time_ms": (end_time - start_time) * 1000,
                    "timestamp": datetime.utcnow().isoformat()
                }
                yield json.dumps(response) + "\n"
                time.sleep(0.05)
        except GeneratorExit:
            pass
    
    return Response(generate(), mimetype='application/json')

@app.route('/api/json/batch', methods=['GET'])
def json_batch():
    """Get JSON data in batch"""
    records = [generate_user() for _ in range(100)]
    start_time = time.time()
    json_data = json.dumps(records)
    end_time = time.time()
    
    return jsonify({
        "format": "json",
        "count": len(records),
        "data": records,
        "size_bytes": len(json_data.encode()),
        "processing_time_ms": (end_time - start_time) * 1000,
        "timestamp": datetime.utcnow().isoformat()
    })

@app.route('/api/avro/batch', methods=['GET'])
def avro_batch():
    """Get Avro data in batch"""
    import base64
    
    records = [generate_user() for _ in range(100)]
    
    start_time = time.time()
    fo = io.BytesIO()
    fastavro.writer(fo, USER_SCHEMA, records)
    avro_bytes = fo.getvalue()
    end_time = time.time()
    
    return jsonify({
        "format": "avro",
        "count": len(records),
        "data": base64.b64encode(avro_bytes).decode('utf-8'),
        "size_bytes": len(avro_bytes),
        "processing_time_ms": (end_time - start_time) * 1000,
        "timestamp": datetime.utcnow().isoformat()
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
