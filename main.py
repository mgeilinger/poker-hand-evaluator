# from flask import Flask, render_template, request, jsonify
# from flask_cors import CORS
# from prob import *
# from util import *
# from hand_compar import *

# app = Flask(__name__)
# CORS(app)  # Enable Cross-Origin Requests

# @app.route('/')
# def home():
#     return render_template('index.html')  # Render the index.html file

# @app.route('/submit', methods=['POST'])
# def submit():
#     data = request.json
#     checkbox_states = data.get('states', [])  # Get checkbox states as a list

#     # Process checkbox data
#     selected_count = sum(checkbox_states)
#     response_message = f"{selected_count} cards selected"
    
#     return jsonify({'checkbox_message': response_message})

# @app.route('/draw', methods=['GET'])
# def draw_hand():
#     # Generate a random poker hand
#     hand = generate_hand()
#     formatted_hand = format_poker_hand(hand)

#     return jsonify({'hand_message': f"Poker hand: {formatted_hand}"})

# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=5000)  # Allow access from any IP