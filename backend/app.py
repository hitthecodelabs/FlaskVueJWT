from zenpy import Zenpy
from zenpy.lib.api_objects import Ticket, Comment, User
import os

from flask import Flask, jsonify, request
from flask_cors import CORS

# Assuming environment variables are used to store credentials
credentials = {
    'email' : os.environ.get("ZENDESK_EMAIL"),
    'token' : os.environ.get("ZENDESK_TOKEN"),
    'subdomain' : os.environ.get("ZENDESK_SUBDOMAIN")
}

zenpy_client = Zenpy(**credentials)

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes and all origins

@app.route('/')
def home():
    return jsonify({"message": "Welcome!"})

@app.route('/api/message')
def hello():
    return jsonify({"message": "Hello from Flask!"})

@app.route('/api/zendesk/tickets', methods=['GET'])
def get_tickets():
    try:
        # Fetch tickets with a specific status, you can customize the query
        tickets = zenpy_client.search(type='ticket', status='open')
        return jsonify([ticket.to_dict() for ticket in tickets])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/zendesk/tickets', methods=['POST'])
def create_ticket():
    try:
        subject = request.json.get('subject')
        description = request.json.get('description')
        ticket = zenpy_client.tickets.create(Ticket(subject=subject, description=description))
        return jsonify(ticket.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
