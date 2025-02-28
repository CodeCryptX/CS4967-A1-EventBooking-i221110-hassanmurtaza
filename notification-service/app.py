import pika
from dotenv import load_dotenv
import os

load_dotenv()
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='notifications')

def callback(ch, method, properties, body):
    print(f"Notification sent: {body}")

channel.basic_consume(queue='notifications', on_message_callback=callback, auto_ack=True)
print('Waiting for messages...')
channel.start_consuming()