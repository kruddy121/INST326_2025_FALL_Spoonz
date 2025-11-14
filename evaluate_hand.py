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

def pass_cards_left(hands, cards_to_pass):
    """ 
    passes one card from each player to the player on their left
 the last players passed card goes into a DISCARD pile
    """
    num_players = len(hands)

    if len(cards_to_pass) != num_players:# validate input lengths
        raise ValueError("each player must pass exactly ONE card")

    # remove each passed card from its players hand
    for i in range(num_players):
        if cards_to_pass[i] not in hands[i]:
            raise ValueError(f"player {i} cannot pass a card they dont have")
        hands[i].remove(cards_to_pass[i])

    # pass cards to the left
    for i in range(1, num_players):
        hands[i].append(cards_to_pass[i - 1])

    # the last players card gets discarded
    discarded_card = cards_to_pass[-1]

    return hands, discarded_card
