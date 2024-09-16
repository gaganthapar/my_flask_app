import pika
import os

RABBITMQ_URL = os.getenv('RABBITMQ_URL', 'amqp://guest:guest@localhost:5672/')


def get_connection():
    return pika.BlockingConnection(pika.URLParameters(RABBITMQ_URL))


def send_to_queue(queue_name, message):
    connection = get_connection()
    channel = connection.channel()
    channel.queue_declare(queue=queue_name)
    channel.basic_publish(exchange='', routing_key=queue_name, body=message)
    connection.close()


def receive_from_queue(queue_name):
    connection = get_connection()
    channel = connection.channel()
    channel.queue_declare(queue=queue_name)

    def callback(ch, method, properties, body):
        print(f"Received {body}")
        # Process the message
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(queue=queue_name, on_message_callback=callback)
    channel.start_consuming()
