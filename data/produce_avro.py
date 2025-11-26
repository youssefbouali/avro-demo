from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer

# Define the schema
value_schema_str = """
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

value_schema = avro.loads(value_schema_str)

# Configure the AvroProducer
avro_producer = AvroProducer({
    'bootstrap.servers': 'kafka:9092',
    'schema.registry.url': 'http://schema-registry:8081'
}, default_value_schema=value_schema)

# Produce a message
avro_producer.produce(topic='users', value={"id": 1, "nom": "Alice", "age": 25})
avro_producer.flush()
print("Message sent to Kafka!")