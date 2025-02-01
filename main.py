from flask import Flask, render_template, request, jsonify  # Add render_template here
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Requests

# Define suits and ranks for poker cards
suits = ['H', 'D', 'C', 'S']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

# Function to generate a random poker hand
def generate_hand():
    deck = [(rank, suit) for rank in ranks for suit in suits]
    random.shuffle(deck)
    return deck[:5]

# Function to format the poker hand nicely with symbols
def format_poker_hand(hand):
    suit_symbols = {'H': '♥', 'S': '♠', 'D': '♦', 'C': '♣'}
    return ", ".join(f"{rank}{suit_symbols[suit]}" for rank, suit in hand)

@app.route('/')
def home():
    return render_template('index.html')  # Render the index.html file

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    checkbox_states = data.get('states', [])  # Get checkbox states as a list

    # Generate a random poker hand
    hand = generate_hand()
    formatted_hand = format_poker_hand(hand)

    selected_count = sum(checkbox_states)
    response_message = f"{selected_count} boxes selected. Poker hand: {formatted_hand}"

    return jsonify({'message': response_message})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)  # Allow access from any IP