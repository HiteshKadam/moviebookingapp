from confluent_kafka import Producer

kafka_config = {
    'bootstrap.servers': 'localhost:9092',  # Kafka broker addresses
}

producer = Producer(kafka_config)

def publish_message(topic, message):
    producer.produce(topic, value=message)
    producer.flush()
