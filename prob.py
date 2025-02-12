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
    if is_flush(cards) is not False: # Don't calculate if you already have a flush
        return None
    deck = 47
    draws = states.count(True)
    if draws == 0:
        return 0
    success_states = 8 + draws
    if check_matching_suits(cards,states):
        return round(100*pmf(deck,success_states,draws,draws),2)
    return 0

def straight_probability(cards, states):
    if is_straight(cards) is not False: # Don't calculate if you already have a straight
        return None
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
    if probability == 0:
        return 0
    return round(probability*100,2)

def four_probability(cards, states):
    kept_hand = create_hand_after_discard(cards, states)
    if is_four(kept_hand) is not False: # Don't calculate if you already have a four of a kind or three of a kind
        return None
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
    discarded_ranks = discarded_card_ranks(cards, states)
    for winner in winners:
        N = deck
        discarded_winner = discarded_ranks.count(winner[0])
        K = 4 - len(winner) - discarded_winner
        n = draws
        k = 4 - len(winner)
        old_prob += pmf(N,K,n,k)
    probability = new_prob + old_prob
    return round(100*probability,2)

def three_probability(cards, states):
    kept_hand = create_hand_after_discard(cards, states)
    if is_three(kept_hand) is not False: # Don't calculate if you already have a four of a kind or three of a kind
        return None
    deck = 47
    draws = states.count(True)
    if draws == 0: # Don't calculate if you're not discarding anything
        return 0
    kept_ranks = kept_card_ranks(cards, states)
    winners = can_you_make_n_of_a_kind(kept_ranks,3,draws)
    discarded_ranks = discarded_card_ranks(cards, states)
    # print('kept ranks:',kept_ranks)
    # print('discarded ranks:',discarded_ranks)
    new_prob = 0
    old_prob = 0
    disc_prob = 0
    if (draws>=3):
        for rank in ranks:
            if rank in kept_ranks:
                continue
            # print('rank is:',rank)
            # Check occurences in original hand
            seen = 4 - kept_ranks.count(rank) - discarded_ranks.count(rank)
            N = deck
            n = draws
            k = 3
            # print('N is:',deck)
            # print('K is:',seen)
            # print('n is:',n)
            # print('k is:',k)
            new_prob += pmf(N,seen,n,k)
            # print('prob is:',pmf(N,seen,n,k))
    for winner in winners:
        N = deck
        # Check occurences of winner in discarded cards and subtract those from K
        discarded_winner = discarded_ranks.count(winner[0])
        K = 4 - len(winner) - discarded_winner
        n = draws
        k = 3 - len(winner)
        old_prob += pmf(N,K,n,k)
    probability = new_prob + old_prob
    return round(100*probability,2)

def pair_probability(cards, states):
    kept_hand = create_hand_after_discard(cards, states)
    if is_pair(kept_hand) is not False: # Don't calculate if you already have a four of a kind or three of a kind or a pair
        return None
    deck = 47
    draws = states.count(True)
    if draws == 0: # Don't calculate if you're not discarding anything
        return 0
    kept_ranks = kept_card_ranks(cards, states)
    winners = can_you_make_n_of_a_kind(kept_ranks,2,draws)
    discarded_ranks = discarded_card_ranks(cards, states)
    # print('kept ranks:',kept_ranks)
    # print('discarded ranks:',discarded_ranks)
    new_prob = 0
    old_prob = 0
    disc_prob = 0
    if (draws>=2):
        for rank in ranks:
            if rank in kept_ranks:
                continue
            # print('rank is:',rank)
            # Check occurences in original hand
            seen = 4 - kept_ranks.count(rank) - discarded_ranks.count(rank)
            N = deck
            n = draws
            k = 2
            # print('N is:',deck)
            # print('K is:',seen)
            # print('n is:',n)
            # print('k is:',k)
            new_prob += pmf(N,seen,n,k)
            # print('prob is:',pmf(N,seen,n,k))
    for winner in winners:
        N = deck
        # Check occurences of winner in discarded cards and subtract those from K
        discarded_winner = discarded_ranks.count(winner[0])
        K = 4 - len(winner) - discarded_winner
        n = draws
        k = 2 - len(winner)
        old_prob += pmf(N,K,n,k)
    # print(new_prob)
    # print(old_prob)
    probability = new_prob + old_prob
    return round(100*probability,2)

def full_house_probability(cards, states):
    deck = 47
    draws = states.count(True)
    if draws == 0: # Don't calculate if you're not discarding anything
        return 0
    kept_ranks = kept_card_ranks(cards, states)
    winners = can_you_make_n_of_a_kind(kept_ranks,2,draws)
    discarded_ranks = discarded_card_ranks(cards, states)
    print('kept ranks:',kept_ranks)
    print('discarded ranks:',discarded_ranks)
    print('winners:',winners)
    new_prob = 0
    old_prob = 0
    disc_prob = 0
    # if (draws>=2):
    #     for rank in ranks:
    #         if rank in kept_ranks:
    #             continue
    #         print('rank is:',rank)
    #         # Check occurences in original hand
    #         seen = 4 - kept_ranks.count(rank) - discarded_ranks.count(rank)
    #         N = deck
    #         n = draws
    #         k = 2
    #         print('N is:',deck)
    #         print('K is:',seen)
    #         print('n is:',n)
    #         print('k is:',k)
    #         new_prob += pmf(N,seen,n,k)
    #         # print('prob is:',pmf(N,seen,n,k))
    for winner in winners:
        N = deck
        # Check occurences of winner in discarded cards and subtract those from K
        discarded_winner = discarded_ranks.count(winner[0])
        K = 4 - len(winner) - discarded_winner
        n = draws
        k = 2 - len(winner)
        old_prob += pmf(N,K,n,k)
    print('new_prob:',new_prob)
    print('old_prob:',old_prob)
    probability = new_prob + old_prob
    return round(100*probability,2)

hand = generate_hand()
formatted_hand = format_poker_hand(hand)

s = [False, False, True, True, True]
c = [('5', 'C'), ('6', 'D'), ('8', 'C'), ('9', 'S'), ('8', 'H')]

# print('The probability of drawing a straight is:',straight_probability(c,s),'%')
# print('The probability of drawing a flush is:',flush_probability(c,s),'%')
# print('The probability of drawing a four of a kind is:',four_probability(c,s),'%')
# print('The probability of drawing a straight flush is:',straight_flush_probability(c,s),'%')
# print('The probability of drawing a three of a kind is:',three_probability(c,s),'%')
# print('The probability of drawing a pair is:',pair_probability(c,s),'%')
# print('The probability of drawing a full house is:',full_house_probability(c,s),'%')