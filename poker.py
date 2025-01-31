import random

suits = ['H', 'D', 'C', 'S']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

def generate_hand():
    deck = [(rank, suit) for rank in ranks for suit in suits]
    random.shuffle(deck)
    return deck[:5]  # Draw 5 cards

hand = generate_hand()

test_hands = [[('K', 'H'), ('6', 'C'), ('4', 'C'), ('8', 'C'), ('8', 'H')],
[('7', 'S'), ('4', 'H'), ('K', 'C'), ('6', 'S'), ('5', 'S')],
[('Q', 'H'), ('9', 'D'), ('10', 'D'), ('7', 'S'), ('5', 'H')],
[('Q', 'S'), ('K', 'H'), ('Q', 'H'), ('Q', 'C'), ('7', 'C')]]

def suit(card):
    return card[-1]

def value(card):
    if (card[0]=='A'):
        return 14
    if (card[0]=='K'):
        return 13
    if (card[0]=='Q'):
        return 12
    if (card[0]=='J'):
        return 11
    if (card[1]=='0'):
        return 10
    else:
        return int(card[0])

# print('Your poker hand:', hand)