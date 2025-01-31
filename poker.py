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
    return max(value(card) for card in cards if value(card) not in but)

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

# print('Should be: 8: ', hand_rank(royal_flush_1))
# print('Should be: 7: ', hand_rank(four_1))
# print('Should be: 6: ', hand_rank(full_house_1))
# print('Should be: 5: ', hand_rank(flush_1))
# print('Should be: 4: ', hand_rank(straight_2))
# print('Should be: 3: ', hand_rank(three_1))
# print('Should be: 2: ', hand_rank(two_pair_1))
# print('Should be: 1: ', hand_rank(pair_1))
# print('Should be: 0: ', hand_rank(high_card_1))