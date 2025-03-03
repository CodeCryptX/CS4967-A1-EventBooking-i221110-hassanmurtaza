import pika
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
QUEUE_NAME = os.getenv("RABBITMQ_QUEUE", "notifications")

def receive_notification():
    connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
    channel = connection.channel()
    
    # Declare queue to ensure it exists
    channel.queue_declare(queue=QUEUE_NAME)

    def callback(ch, method, properties, body):
        print(f"📩 Received Notification: {body.decode()}")

    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback, auto_ack=True)
    
    print("🔔 Waiting for messages...")
    channel.start_consuming()

if __name__ == "__main__":
    receive_notification()
