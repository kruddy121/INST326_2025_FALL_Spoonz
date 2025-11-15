from collections import Counter

def evaluate_hand_strength(hand): #michael 
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

def pass_cards_left(hands, cards_to_pass): #juanita
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

def spoon_event(hands, letters): #tylor
    """
    Runs the spoon event when a player gets four-of-a-kind.

    hands: dict {player_name: [card1, card2, card3, card4]}
    letters: dict {player_name: current_letter_count}

    Returns a dict with:
        - trigger: player who had four-of-a-kind
        - spoons: list of players who got spoons
        - no_spoon: the player who missed a spoon
        - updated_letters: dict of updated letter counts
    """

    # Find the player who triggered with 4 of a kind
    trigger_player = None
    for player, cards in hands.items():
        if 4 in Counter(cards).values():
            trigger_player = player
            break

    if trigger_player is None:
        raise ValueError("No four-of-a-kind found — spoon event cannot run.")

    # Determine spoon count
    active_players = list(hands.keys())
    total_spoons = len(active_players) - 1

    # Trigger player automatically gets one
    spoon_receivers = {trigger_player}

    # Evaluate hand strength (max matching cards)
    match_strength = {}

    for player, cards in hands.items():
        if player == trigger_player:
            continue
        counts = Counter(cards).values()
        match_strength[player] = max(counts)

    # Rank players by strongest matches (3 > 2 > 1)
    # Tie-breaking random
    ranked = sorted(
        match_strength.keys(),
        key=lambda p: (match_strength[p], random.random()),
        reverse=True
    )
    
    # Assign spoons until we run out
    for p in ranked:
        if len(spoon_receivers) < total_spoons:
            spoon_receivers.add(p)

    # Identify the player who did NOT get a spoon
    no_spoon = (set(active_players) - spoon_receivers).pop()

    # Give them a letter
    letters[no_spoon] += 1

    return {
        "trigger": trigger_player,
        "spoons": list(spoon_receivers),
        "no_spoon": no_spoon,
        "updated_letters": letters
    }
def update_score_and_eliminate(scores, players_missed): #ayushi
    """Updates the letter totals of players and eliminates any player who 
    reaches all five letters.
    
    Parameters: 
        scores (dict): maps the player names to how many letters they currently 
        have. (ex. {"Danny": 3, "Ava": 5})
        
        players_missed (str): name of the player who missed the spoon each round.
        
    Returns:
        tuple: (updated_scores, eliminated_players)
        
            updated_scores (dict): the remaining players with their updated
            letter counts.
            
            eliminated_players (list): the list of players who were removed each
            round.
    """
    
    scores[players_missed] += 1
    eliminated_players = []
    
    for player, letters in list(scores.items()):
        if letters >= 5:
            eliminated_players.append(player)
            del scores[player]
            
    return scores, eliminated_players



# test
if __name__ == "__main__":
    test_scores = {"P1": 0, "P2": 3, "P3": 4}
    updated, eliminated = update_score_and_eliminate(test_scores, "P3")
    
    print("Updated:", updated)
    print("Eliminated:", eliminated)
