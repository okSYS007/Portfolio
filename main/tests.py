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

RANK_VALUES = {
    '2': 2, '3': 3, '4': 4, '5': 5,
    '6': 6, '7': 7, '8': 8, '9': 9,
    '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14
}

def is_consecutive(ranks):
    ranks = sorted(set(ranks))
    if len(ranks) < 5:
        return False
    for i in range(len(ranks) - 4):
        if ranks[i+4] - ranks[i] == 4:
            return True
    if set([14, 2, 3, 4, 5]).issubset(ranks):
        return True
    return False

def evaluate_hand(hand):
    ranks = sorted([RANK_VALUES[c['rank']] for c in hand], reverse=True)
    suits = [c['suit'] for c in hand]

    is_flush = len(set(suits)) == 1
    is_straight = is_consecutive(ranks)

    counts = {r: ranks.count(r) for r in set(ranks)}
    count_values = sorted(counts.values(), reverse=True)

    if is_flush and is_straight and max(ranks) == 14:
        return (10, ranks, "Royal Flush")
    if is_flush and is_straight:
        return (9, ranks, "Straight Flush")
    if 4 in count_values:
        return (8, ranks, "Four of a Kind")
    if 3 in count_values and 2 in count_values:
        return (7, ranks, "Full House")
    if is_flush:
        return (6, ranks, "Flush")
    if is_straight:
        return (5, ranks, "Straight")
    if 3 in count_values:
        return (4, ranks, "Three of a Kind")
    if count_values.count(2) == 2:
        return (3, ranks, "Two Pair")
    if 2 in count_values:
        return (2, ranks, "One Pair")

    return (1, ranks, "High Card")

def get_best_hand(all_cards):
    best = (-1, [], "")
    best_hand = None
    for combo in combinations(all_cards, 5):
        score = evaluate_hand(combo)
        if score > best:
            best = score
            best_hand = combo
    return best_hand, best

# Общие карты (на столе)
board = [
    {'rank': '2', 'suit': '♠'},
    {'rank': '2', 'suit': '♠'},
    {'rank': '4', 'suit': '♠'},
    {'rank': 'J', 'suit': '♠'},
    {'rank': '10', 'suit': '♠'},
]

# Игроки
players = [
    {
        'name': 'Игрок 1',
        'cards': [
            {'rank': '2', 'suit': '♦'},
            {'rank': '3', 'suit': '♣'},
        ]
    },
    {
        'name': 'Игрок 2',
        'cards': [
            {'rank': '4', 'suit': '♠'},
            {'rank': '5', 'suit': '♠'},
        ]
    }
]

# Проверка рук
results = []
for player in players:
    all_cards = board + player['cards']
    best_hand, (score, _, name) = get_best_hand(all_cards)
    results.append((score, player['name'], name, best_hand))

# Сортировка по силе руки
results.sort(reverse=True)

# Вывод
for score, name, hand_name, hand in results:
    hand_str = ' '.join([c['rank'] + c['suit'] for c in hand])
    print(f"{name}: {hand_name} ({hand_str})")
