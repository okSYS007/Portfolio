from itertools import combinations
from collections import Counter

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
    hand = sorted(hand, key=lambda c: RANK_VALUES[c['rank']], reverse=True)
    ranks = [RANK_VALUES[c['rank']] for c in hand]
    suits = [c['suit'] for c in hand]
    rank_counts = Counter(ranks)

    # Проверка на флеш
    flush_suit = None
    for suit in set(suits):
        suited = [c for c in hand if c['suit'] == suit]
        if len(suited) >= 5:
            flush_suit = suit
            flush_cards = suited
            break

    # Проверка на стрейт
    rank_set = set(ranks)
    straights = []
    for start in range(14, 4, -1):
        straight_range = list(range(start, start - 5, -1))
        if set(straight_range).issubset(rank_set):
            straights = [c for c in hand if RANK_VALUES[c['rank']] in straight_range]
            break
    # Спец. случай: A-2-3-4-5
    if not straights and set([14, 2, 3, 4, 5]).issubset(rank_set):
        straights = [c for c in hand if RANK_VALUES[c['rank']] in [14, 2, 3, 4, 5]]

    # STRAIGHT FLUSH / ROYAL FLUSH
    if flush_suit and straights:
        straight_flush = [c for c in flush_cards if c in straights]
        if len(straight_flush) >= 5:
            ranks_only = [RANK_VALUES[c['rank']] for c in straight_flush]
            if max(ranks_only) == 14:
                return 10, straight_flush[:5], "Royal Flush"
            return 9, straight_flush[:5], "Straight Flush"

    # FOUR OF A KIND
    for rank, count in rank_counts.items():
        if count == 4:
            quad_cards = [c for c in hand if RANK_VALUES[c['rank']] == rank]
            return 8, quad_cards, "Four of a Kind"

    # FULL HOUSE
    trips = []
    pairs = []
    for rank, count in rank_counts.items():
        if count >= 3:
            trips.append(rank)
        elif count >= 2:
            pairs.append(rank)
    if trips:
        trips_rank = max(trips)
        remaining_pairs = pairs + [r for r in trips if r != trips_rank]
        if remaining_pairs:
            trip_cards = [c for c in hand if RANK_VALUES[c['rank']] == trips_rank][:3]
            pair_rank = max(remaining_pairs)
            pair_cards = [c for c in hand if RANK_VALUES[c['rank']] == pair_rank][:2]
            return 7, trip_cards + pair_cards, "Full House"

    # FLUSH
    if flush_suit:
        return 6, flush_cards[:5], "Flush"

    # STRAIGHT
    if straights and len(straights) >= 5:
        return 5, straights[:5], "Straight"

    # THREE OF A KIND
    for rank, count in rank_counts.items():
        if count == 3:
            cards = [c for c in hand if RANK_VALUES[c['rank']] == rank]
            return 4, cards, "Three of a Kind"

    # TWO PAIR
    all_pairs = [rank for rank, count in rank_counts.items() if count == 2]
    if len(all_pairs) >= 2:
        high_pairs = sorted(all_pairs, reverse=True)[:2]
        cards = [c for c in hand if RANK_VALUES[c['rank']] in high_pairs][:4]
        return 3, cards, "Two Pair"

    # ONE PAIR
    if len(all_pairs) == 1:
        pair_rank = all_pairs[0]
        cards = [c for c in hand if RANK_VALUES[c['rank']] == pair_rank][:2]
        return 2, cards, "One Pair"

    # HIGH CARD
    return 1, [hand[0]], "High Card"

def get_best_hand(all_cards):
    best_score = -1
    best_combo = []
    best_name = ""

    for combo in combinations(all_cards, 5):
        score, combo_cards, name = evaluate_hand(combo)
        if score > best_score:
            best_score = score
            best_combo = combo_cards  # теперь только нужные карты
            best_name = name

    return best_combo, (best_score, best_combo, best_name)


# Общие карты (на столе)
board = [
    {'rank': '2', 'suit': '♠'},
    {'rank': '2', 'suit': '♣'},
    {'rank': '4', 'suit': '♠'},
    {'rank': 'J', 'suit': '♦'},
    {'rank': '10', 'suit': '♠'},
]

# Игроки
players = [
    {
        'name': 'Игрок 1',
        'cards': [
            {'rank': '5', 'suit': '♦'},
            {'rank': '3', 'suit': '♣'},
        ]
    },
    {
        'name': 'Игрок 2',
        'cards': [
            {'rank': '4', 'suit': '♦'},
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
