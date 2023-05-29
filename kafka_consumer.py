# kafkaapp/kafka_consumer.py

from kafka import KafkaConsumer

KAFKA_TOPIC = 'DeleteMovieRequested'
consumer = KafkaConsumer(KAFKA_TOPIC)

for message in consumer:
    print('Received message:', message.value)

consumer.close()
