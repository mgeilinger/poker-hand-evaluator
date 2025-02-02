from poker import *

import random
import math

checkboxStates = [False,False,False,True,True] #Will be taken from js later

# Using the probability mass function let's start with flushes
# math.comb() for binomial coefficient

def pmf(N, K, n, k):
    probability = (math.comb(K, k) * math.comb(N - K, n - k)) / math.comb(N, n)
    return round(probability * 100, 2)

# Check whether all the Falses in the array are the same suit.

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

def flush_probability(cards,states):
    deck = 47
    draws = states.count(True)
    success_states = 8 + draws
    if draws == 0:
        return 0
    if check_matching_suits(cards,states):
        return pmf(deck,success_states,draws,draws)
    return 0

def pair_probability(cards, states):
    deck = 47
    draws = states.count(True)
    kept_ranks = kept_card_ranks(cards, states)
    success_states = 0
    needed = 1 # Only need one success to make a pair
    hand_after_discard = create_hand_after_discard(cards, states)
    if draws == 0:
        return 0
    if is_pair(hand_after_discard) is not False:
        return 0 # Don't show the probability if you already have a pair (after discarding)
    for rank in kept_ranks:
        success_states += 4
        success_states -= count_rank_occurrences(cards,rank)
    return round(pmf (deck,success_states,draws,needed),2)

# def three_probability(cards, states):
#     deck = 47
#     draws = states.count(True)
#     kept_ranks = kept_card_ranks(cards, states)
#     needed = 2 # Need two successes to make a pair
#     hand_after_discard = create_hand_after_discard(cards, states)
#     total_probability = 0
#     if draws == 0:
#         print('No draws')
#         return 0
#     if is_three(hand_after_discard) is not False:
#         print('Already got three of a kind')
#         return 0 # Don't show the probability if you already have three of a kind (after discarding)
#     for rank in kept_ranks:
#         total_probability += 
#         success_states -= count_rank_occurrences(cards,rank)
#     print('N:',deck)
#     print('K:',success_states)
#     print('n:',draws)
#     print('k:',needed)
#     return round(pmf (deck,success_states,draws,needed),2)

hand = generate_hand()
formatted_hand = format_poker_hand(hand)

# print(formatted_hand)
# print('You have a',hand_rank_string(hand))

s = [False, True, False, False, False]
c = [('K', 'H'), ('K', 'H'), ('4', 'H'), ('8', 'H'), ('9', 'H')]

# print('Hand after discard:',create_hand_after_discard(c,s))
# print(three_probability(c,s))

print('Hand after discard:',create_hand_after_discard(c,s))
print(pair_probability(c,s))