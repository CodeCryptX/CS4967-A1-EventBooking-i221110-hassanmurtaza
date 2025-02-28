from flask import Flask, jsonify, request
import pika
import requests
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)

# Sync call to Event Service
@app.route('/bookings', methods=['POST'])
def create_booking():
    event_id = request.json['event_id']
    response = requests.get(f'http://localhost:5001/events/{event_id}/availability')
    if response.status_code != 200:
        return jsonify({"error": "Event not available"}), 400
    
    # Publish to RabbitMQ (Async)
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='notifications')
    channel.basic_publish(exchange='', routing_key='notifications', body='{"booking_id": 123, "status": "CONFIRMED"}')
    connection.close()
    
    return jsonify({"message": "Booking confirmed"}), 201

if __name__ == '__main__':
    app.run(port=5002)