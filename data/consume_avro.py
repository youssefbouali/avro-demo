from confluent_kafka.avro import AvroConsumer

# Configure the AvroConsumer
avro_consumer = AvroConsumer({
    'bootstrap.servers': 'kafka:9092',
    'group.id': 'test-group',
    'schema.registry.url': 'http://schema-registry:8081',
    'auto.offset.reset': 'earliest'
})

avro_consumer.subscribe(['users'])

# Consume messages
print("Consuming messages...")
while True:
    try:
        msg = avro_consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print(f"Error: {msg.error()}")
            continue
        print(f"Received message: {msg.value()}")
    except KeyboardInterrupt:
        break

avro_consumer.close()