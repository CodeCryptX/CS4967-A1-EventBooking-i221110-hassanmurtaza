from flask import Flask, request, jsonify
import pika
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
QUEUE_NAME = os.getenv("RABBITMQ_QUEUE", "notifications")

def send_notification(message):
    connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
    channel = connection.channel()

    # Declare queue
    channel.queue_declare(queue=QUEUE_NAME)

    # Publish message
    channel.basic_publish(exchange='', routing_key=QUEUE_NAME, body=message)

    connection.close()

@app.route("/notify", methods=["POST"])
def notify():
    data = request.json
    message = data.get("message", "No message provided")

    send_notification(message)
    return jsonify({"status": "Notification sent"}), 200

if __name__ == "__main__":
    app.run(debug=True, port=5004)
