from util import *

def is_straight(cards):
    dist = hand_dist(cards)
    for value in range(1,11):
        if all([dist[value + k] == 1 for k in range(5)]):
            return value + 4
    return False

def is_flush(cards):
    dist = hand_dist(cards)
    if all(suit(card)==suit(cards[0]) for card in cards):
        return max([k for k, value in dist.items() if value == 1])
    return False

def is_straight_flush(cards):
    straight = is_straight(cards)
    flush = is_flush(cards)
    if straight and flush:
        return straight
    return False

def is_four(cards):
    hc = card_count(cards, 4)
    k = high_card(cards, hc)
    if hc is not False:
        return [hc,k]
    return False

def is_three(cards):
    hc = card_count(cards, 3)
    k1 = high_card(cards, hc)
    k2 = high_card(cards, {hc,k1})
    if hc is not False:
        return [hc,k1,k2]
    return False

def is_pair(cards):
    hc = card_count(cards, 2)
    k1 = high_card(cards, hc)
    k2 = high_card(cards, {hc,k1})
    k3 = high_card(cards, {hc,k1,k2})
    if hc is not False:
        return [hc,k1,k2,k3]
    return False

def is_two_pair(cards):
    hc1 = card_count(cards,2)
    hc2 = card_count(cards,2,hc1)
    k = high_card(cards, {hc1,hc2})
    if hc1<hc2:
        hc1, hc2 = hc2, hc1
    if (hc2 is not False):
        return [hc1,hc2,k]
    return False

def is_full_house(cards):
    hc = card_count(cards,3)
    k = card_count(cards,2,hc)
    if (hc is not False and k is not False):
        return [hc,k]
    return False

def is_high_card(cards):
    hc = high_card(cards)
    k1 = high_card(cards,hc)
    k2 = high_card(cards,{hc,k1})
    k3 = high_card(cards,{hc,k1,k2})
    k4 = high_card(cards,{hc,k1,k2,k3})
    return [hc,k1,k2,k3,k4]

def hand_rank_list(cards):    
    result = []
    if is_straight_flush(cards) is not False:
        result.append(8)
        result.append(is_straight_flush(cards))
        return result
    if is_four(cards) is not False:
        result.append(7)
        result.extend(is_four(cards))
        return result
    if is_full_house(cards) is not False:
        result.append(6)
        result.extend(is_full_house(cards))
        return result
    if is_flush(cards) is not False:
        result.append(5)
        result.append(is_flush(cards))
        return result
    if is_straight(cards) is not False:
        result.append(4)
        result.append(is_straight(cards))
        return result
    if is_three(cards) is not False:
        result.append(3)
        result.extend(is_three(cards))
        return result
    if is_two_pair(cards) is not False:
        result.append(2)
        result.extend(is_two_pair(cards))
        return result
    if is_pair(cards) is not False:
        result.append(1)
        result.extend(is_pair(cards))
        return result
    result.append(0)
    result.extend(is_high_card(cards))
    return result

def hand_rank_string(cards):
    if is_straight_flush(cards) is not False:
        return "straight flush"
    if is_four(cards) is not False:
        return "four of a kind"
    if is_full_house(cards) is not False:
        return "full house"
    if is_flush(cards) is not False:
        return "flush"
    if is_straight(cards) is not False:
        return "straight"
    if is_three(cards) is not False:
        return "three of a kind"
    if is_two_pair(cards) is not False:
        return "two pair"
    if is_pair(cards) is not False:
        return "pair"
    return "high card" 

c = [('10', 'C'), ('10', 'D'), ('10', 'S')]

print(is_three(c))