import random

suits = ['H', 'D', 'C', 'S']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

two_pair_1=[('K', 'H'), ('K', 'C'), ('4', 'C'), ('8', 'C'), ('8', 'H')]
full_house_1=[('K', 'H'), ('K', 'D'), ('K', 'C'), ('5', 'C'), ('5', 'H')]
pair_1=[('K', 'H'), ('6', 'C'), ('4', 'C'), ('8', 'C'), ('8', 'H')]
straight_1=[('K', 'H'), ('10', 'C'), ('J', 'C'), ('A', 'C'), ('Q', 'H')]
straight_2=[('3', 'H'), ('5', 'C'), ('4', 'D'), ('6', 'D'), ('7', 'H')]
straight_3=[('A', 'H'), ('2', 'C'), ('4', 'C'), ('3', 'C'), ('5', 'H')]
royal_flush_1=[('K', 'H'), ('10', 'H'), ('J', 'H'), ('A', 'H'), ('Q', 'H')]
flush_1=[('Q', 'C'), ('10', 'C'), ('J', 'C'), ('10', 'C'), ('Q', 'C')]

def generate_hand():
    deck = [(rank, suit) for rank in ranks for suit in suits]
    random.shuffle(deck)
    return deck[:5]

hand = generate_hand()

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

def high_card(cards):
    dist = hand_dist(cards)
    result = (hc,k1,k2,k3,k4)
    return result

def is_flush(cards):
    dist = hand_dist(cards)
    if(all(suit(card)==suit(cards[0]) for card in cards)==True):
        return max([k for k, value in dist.items() if value == 1])
    return False

def is_straight(cards):
    dist = hand_dist(cards)
    for value in range(1,11):
        if all([dist[value + k] == 1 for k in range(5)]):
            return value + 4
    return False

def is_flush(cards):
    dist = hand_dist(cards)
    if(all(suit(card)==suit(cards[0]) for card in cards)==True):
        return max([k for k, value in dist.items() if value == 1])
    return False

def is_straight_flush(cards):
    if (is_straight(cards) is not False and is_flush(cards) is not False):
        return True
    return False

def is_four(cards):
    return card_count(cards,4)

def is_three(cards):
    return card_count(cards,3)

def is_pair(cards):
    return card_count(cards,2)

def is__two_pair(cards):
    hc = card_count(cards,2)
    k1 = card_count(cards,2,hc)
    if (k1 is not False):
        return [hc,k1]
    return False

def is_full_house(cards):
    hc = card_count(cards,3)
    k1 = card_count(cards,2,hc)
    if (k1 is not False):
        return [hc,k1]
    return False

# def hand_rank(cards):
#     if

# print(is_straight(pair_1))
# print(is_straight_flush(royal_flush_1))
# print(is_straight_flush(straight_1))
# print(is_straight(straight_1))
# print(is_straight(straight_2))

# print(is_pair(pair_1))
# print(is_pair(straight_1))
# print(is_pair(straight_2))

# print(is_two_pair(two_pair_1))
# print(is_two_pair(pair_1))
# print(is_two_pair(straight_1))

# print(is_full_house(full_house_1))
# print(is_full_house(straight_1))

# print(is_straight(straight_3))

# print('Your poker hand:', hand)