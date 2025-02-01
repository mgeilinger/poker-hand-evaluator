from poker import *

import random
import math

checkboxStates = [False,False,False,True,True] #Will be taken from js later

# Using the probability mass function let's start with flushes
# math.comb() for binomial coefficient

def pmf (N,K,n,k):
    return round((math.comb(K,k)*math.comb((N-k),(n-k)))/(math.comb(N,n))*100,2)

# Check whether all the Falses in the array are the same suit.

def check_matching_suits(cards, states):
    suit_set = set()  # To store suits corresponding to False values

    for i in range(len(states)):
        if not states[i]:  # If the value is False
            suit_set.add(cards[i][1])  # Add the suit to the set

    return len(suit_set) == 1  # True if all suits are the same, False otherwise

def flush_probability(cards,states):
    if check_matching_suits(cards,states):
        deck = 47
        draws = states.count(True)
        success = 8 + draws
        return pmf(deck,success,draws,draws)
    return 0

# Next do four of a kind

def four_probability(cards,states):

hand = generate_hand()
formatted_hand = format_poker_hand(hand)

# print(formatted_hand)
# print('You have a',hand_rank_string(hand))

s = [True, True, True, True, True]
c = [('K', 'H'), ('K', 'H'), ('4', 'H'), ('8', 'H'), ('8', 'H')]

print(check_matching_suits(c, s))
print(flush_probability(c,s))