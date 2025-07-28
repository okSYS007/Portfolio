from itertools import combinations

# Все значения карт
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

# Масти с символами
suits = {
    '♥': 'hearts',
    '♦': 'diamonds',
    '♣': 'clubs',
    '♠': 'spades'
}

# Генерация всех 52 карт
cards = [f"{rank}{suit}" for suit in suits for rank in ranks]

RANK_VALUES = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6,
    '7': 7, '8': 8, '9': 9, '10': 10,
    'J': 11, 'Q': 12, 'K': 13, 'A': 14
}

def get_best_hand(cards):  # 7 карт
    all_combinations = combinations(cards, 5)
    best_hand = None
    best_rank = -1
    
    for hand in all_combinations:
        rank_value, hand_name = evaluate_hand(hand)
        if rank_value > best_rank:
            best_rank = rank_value
            best_hand = hand

    return best_hand, best_rank, hand_name

def evaluate_hand(hand):
    ranks = sorted([RANK_VALUES[c['rank']] for c in hand], reverse=True)
    suits = [c['suit'] for c in hand]

    is_flush = len(set(suits)) == 1
    is_straight = is_consecutive(ranks)

    # Royal Flush
    if is_flush and is_straight and max(ranks) == 14:
        return (10, "Royal Flush")

    # Straight Flush
    if is_flush and is_straight:
        return (9, "Straight Flush")

    # Four of a Kind, Full House, etc...
    counts = {rank: ranks.count(rank) for rank in set(ranks)}
    count_values = sorted(counts.values(), reverse=True)

    if count_values == [4, 1]:
        return (8, "Four of a Kind")
    if count_values == [3, 2]:
        return (7, "Full House")
    if is_flush:
        return (6, "Flush")
    if is_straight:
        return (5, "Straight")
    if count_values == [3, 1, 1]:
        return (4, "Three of a Kind")
    if count_values == [2, 2, 1]:
        return (3, "Two Pair")
    if count_values == [2, 1, 1, 1]:
        return (2, "One Pair")

    return (1, "High Card")

def is_consecutive(ranks):
    ranks = sorted(set(ranks))
    if len(ranks) < 5:
        return False
    for i in range(len(ranks) - 4):
        if ranks[i+4] - ranks[i] == 4:
            return True
    # Спецслучай: A-2-3-4-5
    if set([14, 2, 3, 4, 5]).issubset(ranks):
        return True
    return False

cards = [
    {'rank': 'A', 'suit': '♠'},
    {'rank': 'K', 'suit': '♠'},
    {'rank': 'Q', 'suit': '♠'},
    {'rank': 'J', 'suit': '♠'},
    {'rank': '10', 'suit': '♠'},
    {'rank': '3', 'suit': '♦'},
    {'rank': '5', 'suit': '♣'},
]

hand, value, name = get_best_hand(cards)
print("Лучшая рука:", [str(c['rank']) + c['suit'] for c in hand])
print("Комбинация:", name)
