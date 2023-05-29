from confluent_kafka import Consumer

kafka_config = {
    'bootstrap.servers': 'localhost:9092',  # Kafka broker addresses
    'group.id': 'my_consumer_group',  # Consumer group ID
}

consumer = Consumer(kafka_config)

def consume_messages():
    consumer.subscribe(['movies_topic', 'tickets_topic'])

    while True:
        message = consumer.poll(timeout=1.0)

        if message is None:
            continue

        if message.error():
            print('Error: %s' % message.error())
            continue

        topic = message.topic()
        value = message.value()

        if topic == 'movies_topic':
            process_movie_message(value)
        elif topic == 'tickets_topic':
            process_ticket_message(value)

def process_movie_message(message):
    # Process movie message here
    print(f'Received movie message: {message}')

def process_ticket_message(message):
    # Process ticket message here
    print(f'Received ticket message: {message}')

consume_messages()
