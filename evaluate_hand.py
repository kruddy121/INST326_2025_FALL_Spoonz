from collections import Counter

def evaluate_hand_strength(hand):
    """
    Evaluates a 4-card hand for Spoons and returns its strength category.
    """
    counts = Counter([card[:-1] for card in hand])  # Counts ranks only
    values = sorted(counts.values(), reverse=True)

    if values == [4]:
        category = "four of a kind"
    elif values == [3, 1]:
        category = "three of a kind"
    elif values == [2, 2]:
        category = "two pair"
    elif values == [2, 1, 1]:
        category = "one pair"
    else:
        category = "high card"
    
    return category


