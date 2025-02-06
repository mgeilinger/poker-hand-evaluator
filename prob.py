from util import *
from hand_compar import *

import random
import math
from collections import Counter

checkboxStates = [False,False,False,True,True] #Will be taken from js later

# Using the probability mass function let's start with flushes
# math.comb() for binomial coefficient

def pmf(N, K, n, k):
    probability = (math.comb(K, k) * math.comb(N - K, n - k)) / math.comb(N, n)
    return probability

def straight_flush_probability(cards, states):
    deck = 47
    draws = states.count(True)
    if draws == 0:
        return 0
    kept_hand = create_hand_after_discard(cards, states)
    if is_flush(kept_hand) is not False:
        success_draws = len(straight_is_missing(cards, states))
        N = math.comb(deck, draws)
        probability = success_draws/N
        return round(probability*100,2)
    return 0

def flush_probability(cards,states):
    deck = 47
    draws = states.count(True)
    if draws == 0:
        return 0
    success_states = 8 + draws
    if check_matching_suits(cards,states):
        return round(100*pmf(deck,success_states,draws,draws),2)
    return 0

def straight_probability(cards, states):
    deck = 47
    draws = states.count(True)
    if draws == 0:
        return 0
    s_f_combination = 0
    kept_hand = create_hand_after_discard(cards, states)
    success_draws = len(straight_is_missing(cards, states))
    if is_flush(kept_hand) is not False:
        s_f_combination += success_draws
    combinations = success_draws*pow(4, draws) - s_f_combination # Subtract the straight flush
    N = math.comb(deck, draws)
    probability = combinations/N
    return round(probability*100,2)

def four_probability(cards, states):
    if is_four(cards) is not False: # Don't calculate if you already have a four of a kind
        return 0
    deck = 47
    draws = states.count(True)
    if draws == 0: # Don't calculate if you're not discarding anything
        return 0
    new_prob = 0
    if (draws==4):
        # If you're drawing four cards, the probability of drawing a new four of a kind is given as:
        new_prob += 8*pmf(deck,4,draws,4)
        # As there are 13 ranks - 5 cards in hand that can't be used, then you need 4 cards and have only 4 cards in the deck
    old_prob = 0
    kept_ranks = kept_card_ranks(cards, states)
    winners = can_you_make_n_of_a_kind(kept_ranks,4,draws)
    for winner in winners:
        N = deck
        K = 4 - len(winner)
        n = draws
        k = 4 - len(winner)
        # print('winner is',winner)
        # print('N is', N)
        # print('K is', K)
        # print('n is', n)
        # print('k is', k)
        old_prob += pmf(N,K,n,k)
    # print(old_prob)
    # print(new_prob)
    probability = new_prob + old_prob
    return round(100*probability,2)

# def pair_probability(cards, states):
#     # If your hand already has a pair or better, you won't care about getting a pair
#     # So I want this to return 0
#     hand_after_discard = create_hand_after_discard(cards, states)
#     if is_four(cards) is not False or is_three(cards) is not False or is_two_pair(cards) is not False or is_pair (cards) is not False:
#         return 0
#     deck = 47
#     draws = states.count(True)
#     kept_ranks = kept_card_ranks(cards, states)
#     old_success_states = 0
#     needed = 1 # Only need one success to make a pair
#     if draws == 0:
#         return 0
#     # Probability of making a pair from the cards you already have:
#     for rank in kept_ranks:
#         old_success_states += 4
#         old_success_states -= count_rank_occurrences(cards,rank)
#     probability_old_pair = pmf (deck,old_success_states,draws,needed)
#     # Probability of drawing a new pair from the deck:
#     if draws<2:
#         return round(probability_old_pair,2)
#     probability_new_pair = 0
#     for rank in ranks:
#         in_deck = 4
#         if rank in kept_ranks:
#             in_deck -= 1
#         N = math.comb(deck,draws)
#         K = math.comb(in_deck,2)*draws*(draws-1)*math.comb(12,draws-2)
#         probability_of_rank = pmf(N,K,1,1)
#         probability_new_pair += probability_of_rank
#         # print('Probability is:',probability_of_rank,'for',rank)
#         # print('N:',N)
#         # print('K:',K)
#     # print('Probability of drawing an old pair:',probability_old_pair)
#     # print('Probability of drawing a new pair:',probability_new_pair)
#     probability = probability_old_pair + probability_new_pair
#     return round(probability,2)

hand = generate_hand()
formatted_hand = format_poker_hand(hand)

s = [False, False, False, False, True]
c = [('2', 'H'), ('3', 'H'), ('4', 'H'), ('5', 'H'), ('K', 'C')]

print('The probability of drawing a straight is:',straight_probability(c,s),'%')
print('The probability of drawing a flush is:',flush_probability(c,s),'%')
print('The probability of drawing a four of a kind is:',four_probability(c,s),'%')
print('The probability of drawing a straight flush is:',straight_flush_probability(c,s),'%')