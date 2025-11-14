import random
from collections import Counter

def spoon_event(hands, letters):
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