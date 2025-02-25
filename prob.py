from util import *
from hand_compar import *

import random, math
from collections import Counter

checkboxStates = [False,False,False,True,True] #Will be taken from js later

# Using the probability mass function let's start with flushes
# math.comb() for binomial coefficient

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
    new_prob = 0
    old_prob = 0
    if (draws>=3):
        for rank in ranks:
            if rank in kept_ranks:
                continue
            # Check occurences in original hand
            seen = 4 - kept_ranks.count(rank) - discarded_ranks.count(rank)
            N = deck
            n = draws
            k = 3
            new_prob += pmf(N,seen,n,k)
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
    new_prob = 0
    old_prob = 0
    if (draws>=2):
        for rank in ranks:
            if rank in kept_ranks:
                continue
            # Check occurences in original hand
            seen = 4 - kept_ranks.count(rank) - discarded_ranks.count(rank)
            N = deck
            n = draws
            k = 2
            new_prob += pmf(N,seen,n,k)
    for winner in winners:
        N = deck
        # Check occurences of winner in discarded cards and subtract those from K
        discarded_winner = discarded_ranks.count(winner[0])
        K = 4 - len(winner) - discarded_winner
        n = draws
        k = 2 - len(winner)
        old_prob += pmf(N,K,n,k)
    probability = new_prob + old_prob
    return round(100*probability,2)

def full_house_probability(cards, states):
    deck = 47
    draws = states.count(True)
    if draws == 0: # Don't calculate if you're not discarding anything
        return 0
    kept_ranks = kept_card_ranks(cards, states)
    winners = full_house_winners(kept_ranks,[3,2],draws)
    discarded_ranks = discarded_card_ranks(cards, states)
    new_prob = 0
    old_prob = 0
    if (len(set(kept_ranks)) == 1): # Check if all kept ranks are the same
        if (draws == 2):
            new_prob = sum_pmf_undetermined_ranks(cards, states, 2)
        if (draws == 3):
            new_prob = sum_pmf_undetermined_ranks(cards, states, 3) + 2/math.comb(deck,draws)*sum_comb_undetermined_ranks(cards, states, 2)
        if (draws == 4):
            new_prob = math.comb(3,2)/math.comb(deck,draws)*sum_comb_undetermined_ranks(cards, states, 2) + 2/math.comb(deck,draws)*sum_comb_undetermined_ranks(cards, states, 3)
    for winner in winners:
        counts = Counter(winner)
        most_common = counts.most_common(2)
        rank_1 = most_common[0][0]
        K_1 = 4 - discarded_ranks.count(rank_1) - kept_ranks.count(rank_1)
        k_1 = most_common[0][1]
        if len(most_common) > 1:
            rank_2 = most_common[1][0]
            K_2 = 4 - discarded_ranks.count(rank_2) - kept_ranks.count(rank_2)
            k_2 = most_common[1][1]
            prob = (math.comb(K_1,k_1)*math.comb(K_2,k_2))/math.comb(deck,draws)
        else:
            prob = math.comb(K_1,k_1)/math.comb(deck,draws)
        old_prob += prob
    probability = new_prob + old_prob
    return round(100*probability,2)

def two_pair_probability(cards, states):
    kept_hand = create_hand_after_discard(cards, states)
    kept_ranks = kept_card_ranks(cards, states)
    discarded_ranks = discarded_card_ranks(cards, states)
    deck = 47
    draws = states.count(True)
    if is_two_pair(kept_hand) is not False: # Don't calculate if you already have a two pair
        return None
    if draws == 0: # Don't calculate if you're not discarding anything
        return 0
    winners = two_pair_winners(kept_ranks, draws)
    # print('kept ranks:',kept_ranks)
    # print('discarded ranks:',discarded_ranks)
    # print('winners:',winners)
    new_prob = 0
    old_prob = 0
    n4_prob = 0
    if draws >= 2:
        for rank in ranks:
            if is_pair(kept_hand) is not False: # You already have a pair and just need to draw another one
                if rank in kept_ranks:
                    continue
                # Check occurences in original hand
                seen = 4 - kept_ranks.count(rank) - discarded_ranks.count(rank)
                N = deck
                n = draws
                k = 2
                new_prob += pmf(N,seen,n,k)
        if draws > 2 and is_pair(kept_hand) is False:
                temp_winners = can_you_make_n_of_a_kind(kept_ranks,2,draws)
                number_of_winners = len(temp_winners)
                new_prob += number_of_winners * 2/math.comb(deck,draws)*sum_comb_undetermined_ranks(cards, states, 2)
    if draws == 4:
        for i, rank_1 in enumerate(ranks):  # Outer loop
            for rank_2 in ranks[i + 1:]:  # Inner loop
                k_1 = k_2 = 2
                K_1 = 4 - discarded_ranks.count(rank_1) - kept_ranks.count(rank_1)
                K_2 = 4 - discarded_ranks.count(rank_2) - kept_ranks.count(rank_2)
                prob_1_2 = (math.comb(K_1,k_1)*math.comb(K_2,k_2))/math.comb(deck,draws)
                n4_prob += prob_1_2
        new_prob += n4_prob
        # print('n4_prob:',n4_prob)
    for winner in winners:
        counts = Counter(winner)
        most_common = counts.most_common(2)
        rank_1 = most_common[0][0]
        K_1 = 4 - discarded_ranks.count(rank_1) - kept_ranks.count(rank_1)
        k_1 = most_common[0][1]
        if len(most_common) > 1:
            rank_2 = most_common[1][0]
            K_2 = 4 - discarded_ranks.count(rank_2) - kept_ranks.count(rank_2)
            k_2 = most_common[1][1]
            prob = (math.comb(K_1,k_1)*math.comb(K_2,k_2))/math.comb(deck,draws)
        else:
            prob = pmf(deck,K_1,draws,k_1)
        old_prob += prob
    # print('new_prob:',new_prob)
    # print('old_prob:',old_prob)
    probability = new_prob + old_prob
    return round(100*probability,2)

hand = generate_hand()
formatted_hand = format_poker_hand(hand)

s = [False, False, True, True, True]
c = [('5', 'C'), ('7', 'D'), ('J', 'S'), ('9', 'S'), ('Q', 'H')]

print('The probability of drawing a straight is:',straight_probability(c,s),'%')
print('The probability of drawing a flush is:',flush_probability(c,s),'%')
print('The probability of drawing a four of a kind is:',four_probability(c,s),'%')
print('The probability of drawing a straight flush is:',straight_flush_probability(c,s),'%')
print('The probability of drawing a three of a kind is:',three_probability(c,s),'%')
print('The probability of drawing a pair is:',pair_probability(c,s),'%')
print('The probability of drawing a full house is:',full_house_probability(c,s),'%')
print('The probability of drawing a two pair is:',two_pair_probability(c,s),'%')