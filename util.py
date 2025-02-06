import random

two_pair_1=[('K', 'H'), ('K', 'C'), ('4', 'C'), ('8', 'C'), ('8', 'H')]
high_card_1=[('4', 'H'), ('7', 'C'), ('2', 'C'), ('K', 'C'), ('8', 'H')]
three_1=[('3', 'S'), ('3', 'C'), ('K', 'D'), ('Q', 'D'), ('3', 'H')]
three_2=[('K', 'S'), ('K', 'C'), ('3', 'D'), ('5', 'D'), ('K', 'H')]
four_1=[('3', 'S'), ('3', 'C'), ('2', 'D'), ('3', 'D'), ('3', 'H')]
full_house_1=[('K', 'H'), ('K', 'D'), ('K', 'C'), ('5', 'C'), ('5', 'H')]
pair_1=[('K', 'H'), ('6', 'C'), ('4', 'C'), ('8', 'C'), ('8', 'H')]
straight_1=[('K', 'H'), ('10', 'C'), ('J', 'C'), ('A', 'C'), ('Q', 'H')]
straight_2=[('3', 'H'), ('5', 'C'), ('4', 'D'), ('6', 'D'), ('7', 'H')]
straight_3=[('A', 'H'), ('2', 'C'), ('4', 'C'), ('3', 'C'), ('5', 'H')]
royal_flush_1=[('K', 'H'), ('10', 'H'), ('J', 'H'), ('A', 'H'), ('Q', 'H')]
flush_1=[('Q', 'C'), ('10', 'C'), ('J', 'C'), ('10', 'C'), ('Q', 'C')]

s1 = [False, False, False, False, True]
n1_no_gap = [('6', 'H'), ('7', 'C'), ('8', 'C'), ('9', 'C'), ('A', 'H')]
n1_1_gap = [('5', 'H'), ('6', 'C'), ('7', 'C'), ('9', 'C'), ('A', 'H')]

s2 = [False, False, False, True, True]
n2_no_gap = [('6', 'H'), ('7', 'C'), ('8', 'C'), ('K', 'C'), ('A', 'H')]
n2_1_gap = [('6', 'H'), ('5', 'C'), ('8', 'C'), ('K', 'C'), ('A', 'H')]
n2_2_gap = [('9', 'H'), ('5', 'C'), ('8', 'C'), ('K', 'C'), ('A', 'H')]

s3 = [False, False, True, True, True]
n3_no_gap = [('6', 'H'), ('7', 'C'), ('Q', 'C'), ('K', 'C'), ('A', 'H')]
n3_1_gap = [('6', 'H'), ('8', 'C'), ('Q', 'C'), ('K', 'C'), ('A', 'H')]
n3_2_gap = [('5', 'H'), ('8', 'C'), ('Q', 'C'), ('K', 'C'), ('A', 'H')]
n3_3_gap = [('5', 'H'), ('9', 'C'), ('Q', 'C'), ('K', 'C'), ('A', 'H')]

s4 = [False, True, True, True, True]
n4_no_gap = [('7', 'H'), ('J', 'C'), ('Q', 'C'), ('K', 'C'), ('A', 'H')]

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
    else:
        return int(card[0])

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

def hand_dist(cards):
    dist = {i:0 for i in range(1,15)}
    for card in cards:
        dist[value(card)] += 1
    dist[1] = dist[14]
    return dist

def card_count(cards, num, but=None):
    dist = hand_dist(cards)
    for value in range(2,15):
        if value == but:
            continue
        if (dist[value]==num):
            return value
    return False

def high_card(cards, but=None):
    dist = hand_dist(cards)
    if not isinstance(but, set):
        but = {but}
    valid_cards = [value(card) for card in cards if value(card) not in but]
    if not valid_cards:  # If the list is empty, return a safe default value
        return min(dist.keys())  # Or any fallback value
    return max(valid_cards)

def check_matching_suits(cards, states):
    suit_set = set()  # To store suits corresponding to False values
    for i in range(len(states)):
        if not states[i]:  # If the value is False
            suit_set.add(cards[i][1])  # Add the suit to the set
    return len(suit_set) == 1  # True if all suits are the same, False otherwise

def kept_card_ranks(cards, states):
    return [cards[i][0] for i in range(len(cards)) if not states[i]]

def discarded_card_ranks(cards, states):
    return [cards[i][0] for i in range(len(cards)) if states[i]]

def create_hand_after_discard(cards, states):
    return [cards[i] for i in range(len(cards)) if not states[i]]

def count_rank_occurrences(cards, rank):
    return sum(1 for card in cards if card[0] == rank)

def straight_is_missing(cards, states):
    kept_hand = create_hand_after_discard(cards, states)
    n = states.count(True) # Draws
    dist = hand_dist(kept_hand)

    keys = sorted(dist.keys())
    possible_additions = []
    
    for i in range(len(keys) - 4):  # Need at least 5 numbers in a row
        window = keys[i:i+5]  # Take a sliding window of 5 numbers
        missing = [num for num in window if dist[num] == 0]  # Find missing numbers
        
        if len(missing) == n:  # If exactly n numbers are needed
            possible_additions.append(missing)
    
    return possible_additions

s = [False, False, True, True, True]

c = [('3', 'H'), ('5', 'H'), ('8', 'H'), ('J', 'H'), ('K', 'C')]

# print(straight_is_missing(c, s))