from flask import Flask, request, jsonify
from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer, AvroConsumer
import json
import threading
from collections import deque

app = Flask(__name__)

# Define Avro schemas
USER_SCHEMA_STR = """
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
"""

USER_SCHEMA = avro.loads(USER_SCHEMA_STR)

# Global producer and consumer configuration
KAFKA_CONFIG = {
    'bootstrap.servers': 'kafka:9092',
    'schema.registry.url': 'http://schema-registry:8081'
}

# Message buffer for consuming
message_buffer = deque(maxlen=100)
consumer_running = False

# Initialize producer
try:
    producer = AvroProducer(KAFKA_CONFIG, default_value_schema=USER_SCHEMA)
    print("✓ Producer initialized successfully")
except Exception as e:
    print(f"✗ Producer initialization failed: {e}")
    producer = None

# Consumer thread function
def consume_messages():
    global consumer_running
    try:
        consumer = AvroConsumer(
            {
                'bootstrap.servers': 'kafka:9092',
                'schema.registry.url': 'http://schema-registry:8081',
                'group.id': 'avro-api-consumer',
                'auto.offset.reset': 'earliest'
            },
            reader_value_schema=USER_SCHEMA
        )
        consumer.subscribe(['users'])
        print("✓ Consumer subscribed to 'users' topic")
        
        consumer_running = True
        while consumer_running:
            try:
                msg = consumer.poll(timeout=1.0)
                if msg is None:
                    continue
                
                if msg.error():
                    print(f"Consumer error: {msg.error()}")
                    continue
                
                message_buffer.append({
                    'key': msg.key(),
                    'value': msg.value(),
                    'partition': msg.partition(),
                    'offset': msg.offset(),
                    'timestamp': msg.timestamp()
                })
                print(f"✓ Consumed message: {msg.value()}")
            except Exception as e:
                print(f"Error in consumer loop: {e}")
                continue
    except Exception as e:
        print(f"✗ Consumer initialization failed: {e}")
    finally:
        if 'consumer' in locals():
            consumer.close()
        consumer_running = False

# Start consumer in background thread
consumer_thread = threading.Thread(target=consume_messages, daemon=True)
consumer_thread.start()

# ============ API ENDPOINTS ============

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'producer': 'connected' if producer else 'disconnected',
        'consumer': 'running' if consumer_running else 'stopped'
    }), 200

@app.route('/messages/produce', methods=['POST'])
def produce_message():
    """Produce an Avro message to Kafka"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not all(k in data for k in ['id', 'nom', 'age']):
            return jsonify({
                'error': 'Missing required fields: id, nom, age'
            }), 400
        
        # Validate data types
        if not isinstance(data['id'], int) or not isinstance(data['age'], int):
            return jsonify({
                'error': 'id and age must be integers'
            }), 400
        
        if not isinstance(data['nom'], str):
            return jsonify({
                'error': 'nom must be a string'
            }), 400
        
        if producer is None:
            return jsonify({
                'error': 'Producer not initialized'
            }), 503
        
        # Produce message
        producer.produce(
            topic='users',
            value={
                'id': data['id'],
                'nom': data['nom'],
                'age': data['age']
            }
        )
        producer.flush()
        
        return jsonify({
            'status': 'success',
            'message': 'Message produced successfully',
            'data': data
        }), 201
    
    except Exception as e:
        return jsonify({
            'error': f'Producer error: {str(e)}'
        }), 500

@app.route('/messages/consume', methods=['GET'])
def get_messages():
    """Get consumed messages from buffer"""
    try:
        messages = list(message_buffer)
        return jsonify({
            'status': 'success',
            'count': len(messages),
            'messages': messages
        }), 200
    
    except Exception as e:
        return jsonify({
            'error': f'Consumer error: {str(e)}'
        }), 500

@app.route('/messages/clear', methods=['POST'])
def clear_messages():
    """Clear message buffer"""
    try:
        message_buffer.clear()
        return jsonify({
            'status': 'success',
            'message': 'Message buffer cleared'
        }), 200
    
    except Exception as e:
        return jsonify({
            'error': f'Clear error: {str(e)}'
        }), 500

@app.route('/schema', methods=['GET'])
def get_schema():
    """Get the Avro schema"""
    return jsonify({
        'schema': json.loads(USER_SCHEMA_STR)
    }), 200

@app.route('/topics', methods=['GET'])
def get_topics():
    """Get information about Kafka topics"""
    return jsonify({
        'topics': ['users'],
        'schema': 'User (id: long, nom: string, age: int)'
    }), 200

@app.route('/stats', methods=['GET'])
def get_stats():
    """Get statistics"""
    return jsonify({
        'messages_in_buffer': len(message_buffer),
        'buffer_capacity': message_buffer.maxlen,
        'consumer_status': 'running' if consumer_running else 'stopped'
    }), 200

# ============ ERROR HANDLERS ============

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Endpoint not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'error': 'Internal server error'
    }), 500

if __name__ == '__main__':
    print("\n" + "="*50)
    print("Avro REST API Server Starting...")
    print("="*50)
    print("Available endpoints:")
    print("  GET  /health              - Health check")
    print("  POST /messages/produce    - Produce message")
    print("  GET  /messages/consume    - Get consumed messages")
    print("  POST /messages/clear      - Clear message buffer")
    print("  GET  /schema              - Get Avro schema")
    print("  GET  /topics              - Get topics info")
    print("  GET  /stats               - Get statistics")
    print("="*50 + "\n")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
