from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
from prob import *
from util import *
from hand_compar import *
import secrets  # For generating a secret key

app = Flask(__name__)
CORS(app)
app.secret_key = secrets.token_hex(16)  # Secure session key

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/draw', methods=['GET'])
def draw_hand():
    hand = generate_hand()
    session['hand'] = hand  # Store the hand in session
    formatted_hand = format_poker_hand(hand)

    print("\n--- Hand Drawn ---")
    print("Hand:", hand)

    return jsonify({'hand_message': f"Poker hand: {formatted_hand}"})

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    checkbox_states = data.get('states', [])  # Get checkbox states

    # Retrieve the hand from session
    hand = session.get('hand', generate_hand())  # Fallback if session is lost

    # Filter hand based on kept cards
    kept_hand = [card for i, card in enumerate(hand) if not checkbox_states[i]]

    print("\n--- Debugging Information ---")
    print("Full Hand:", hand)
    print("Checkbox States:", checkbox_states)
    print("Kept Hand:", kept_hand)

    if not kept_hand:  
        print("Kept hand is empty! Returning zeros.")
        return jsonify({'error': 'No valid hand to evaluate'})

    # Calculate probabilities
    probabilities = {
        'Straight': straight_probability(hand, checkbox_states),
        'Flush': flush_probability(hand, checkbox_states),
        'Four of a Kind': four_probability(hand, checkbox_states),
        'Straight Flush': straight_flush_probability(hand, checkbox_states),
        'Three of a Kind': three_probability(hand, checkbox_states),
        'Pair': pair_probability(hand, checkbox_states),
        'Full House': full_house_probability(hand, checkbox_states),
        'Two Pair': two_pair_probability(hand, checkbox_states),
    }

    # Print probabilities in console for debugging
    print("Calculated Probabilities:")
    for hand_type, prob in probabilities.items():
        print(f"{hand_type}: {prob}%")

    return jsonify(probabilities)  # Send probabilities to frontend

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)