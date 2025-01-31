import poker
import prob
import random

suits = ['H', 'D', 'C', 'S']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

def generate_hand():
    deck = [(rank, suit) for rank in ranks for suit in suits]
    random.shuffle(deck)
    return deck[:5]

hand = generate_hand()

print(hand)
print('You have a',poker.hand_rank_string(hand))