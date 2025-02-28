from flask import Flask, jsonify, request
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
client = MongoClient(os.getenv('MONGO_URI'))
db = client['event_db']
events = db.events

@app.route('/events', methods=['GET'])
def get_events():
    return jsonify(list(events.find())), 200

if __name__ == '__main__':
    app.run(port=5001)