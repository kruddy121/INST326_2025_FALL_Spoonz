from collections import Counter
import random

# ranks and suits for making the deck
RANKS = ["2","3","4","5","6","7","8","9","10","J","Q","K","A"]
SUITS = ["H","D","C","S"]

# evaluates how strong a hand is
def evaluate_hand_strength(hand):
    counts = Counter([card[:-1] for card in hand])  # count ranks only
    values = sorted(counts.values(), reverse=True)

    if values == [4]:
        return "four of a kind"
    elif values == [3,1]:
        return "three of a kind"
    elif values == [2,2]:
        return "two pair"
    elif values == [2,1,1]:
        return "one pair"
    else:
        return "high card"

# passes one chosen card from each player to the left
# last player’s card goes into a discard pile
# (helper function, not used in the main loop)
def pass_cards_left(hands, cards_to_pass):
    num_players = len(hands)

    if len(cards_to_pass) != num_players:
        raise ValueError("each player must pass exactly one card")

    for i in range(num_players):
        if cards_to_pass[i] not in hands[i]:
            raise ValueError("player cannot pass a card they dont have")
        hands[i].remove(cards_to_pass[i])

    for i in range(1, num_players):
        hands[i].append(cards_to_pass[i-1])

    discarded_card = cards_to_pass[-1]
    return hands, discarded_card

# handles spoon event when someone gets four of a kind
def spoon_event(hands):
    trigger = None
    for player, cards in hands.items():
        ranks = [card[:-1] for card in cards]
        if 4 in Counter(ranks).values():
            trigger = player
            break

    if trigger is None:
        raise ValueError("no one has four of a kind")

    players = list(hands.keys())
    total_spoons = len(players) - 1
    spoon_receivers = {trigger}

    strength = {}
    for player, cards in hands.items():
        if player == trigger:
            continue
        ranks = [card[:-1] for card in cards]
        strength[player] = max(Counter(ranks).values())

    ranked = sorted(
        strength.keys(),
        key=lambda p: (strength[p], random.random()),
        reverse=True
    )

    for p in ranked:
        if len(spoon_receivers) < total_spoons:
            spoon_receivers.add(p)

    no_spoon = (set(players) - spoon_receivers).pop()

    return {
        "trigger": trigger,
        "spoons": list(spoon_receivers),
        "no_spoon": no_spoon
    }

# updates letters and eliminates players at 5 letters
def update_score_and_eliminate(scores, missed):
    scores[missed] += 1
    eliminated = []

    for player, value in list(scores.items()):
        if value >= 5:
            eliminated.append(player)
            del scores[player]

    return scores, eliminated

# makes a shuffled deck
def create_deck():
    deck = [rank + suit for rank in RANKS for suit in SUITS]
    random.shuffle(deck)
    return deck

# deals 4-card starting hands
def deal_hands(players):
    deck = create_deck()
    hands = {}
    for p in players:
        hands[p] = [deck.pop() for _ in range(4)]
    return hands, deck

# chooses which card a computer player will pass or discard
def choose_cpu_pass_card(hand):
    ranks = [card[:-1] for card in hand]
    counts = Counter(ranks)
    lowest_count = min(counts[r] for r in counts)
    candidate_ranks = [r for r in counts if counts[r] == lowest_count]
    chosen_rank = random.choice(candidate_ranks)
    for card in hand:
        if card[:-1] == chosen_rank:
            return card

# main spoons game loop (you vs computer players)
def run_game():
    print("=== SPOONS GAME: YOU VS COMPUTERS ===")

    # number of players (1 human + rest cpu)
    while True:
        try:
            num = int(input("how many total players? (2-6): "))
            if 2 <= num <= 6:
                break
            else:
                print("enter a number between 2 and 6")
        except ValueError:
            print("enter a valid number")

    human_name = input("your name: ").strip()
    if not human_name:
        human_name = "you"

    players = [human_name]
    for i in range(2, num + 1):
        players.append(f"cpu{i-1}")

    scores = {p: 0 for p in players}
    round_num = 1

    while len(scores) > 1:
        print(f"\n=== round {round_num} ===")
        for p in scores:
            print(f"{p}: {scores[p]} letters")

        active = list(scores.keys())
        hands, deck = deal_hands(active)
        discard = []
        triggered = False

        # keep passing until someone gets four of a kind
        while not triggered:
            print("\nhands:")
            for p in active:
                print(f"{p}: {hands[p]}")

            # one card will travel around the table
            pass_card = None

            for i, p in enumerate(active):
                # first player draws from deck
                if i == 0:
                    if not deck:
                        if discard:
                            deck = discard
                            discard = []
                            random.shuffle(deck)
                        else:
                            forced = random.choice(active)
                            rank = hands[forced][0][:-1]
                            hands[forced] = [rank + s for s in SUITS[:4]]
                            triggered = True
                            break

                    drawn = deck.pop()
                    hands[p].append(drawn)  # now 5 cards

                    if p == human_name:
                        print(f"\n{p} drew {drawn}")
                        print("your hand:", hands[p])
                        choice = input("pass which card? ").strip().upper()
                        while choice not in hands[p]:
                            choice = input("invalid card, try again: ").strip().upper()
                    else:
                        choice = choose_cpu_pass_card(hands[p])
                        print(f"\n{p} drew {drawn} and will pass {choice}")

                    hands[p].remove(choice)
                    pass_card = choice  # goes to next player

                else:
                    # receive card from previous player
                    hands[p].append(pass_card)  # now 5 cards

                    # last player discards to pile
                    if i == len(active) - 1:
                        if p == human_name:
                            print(f"\n{p} received {pass_card}")
                            print("your hand:", hands[p])
                            choice = input("discard which card? ").strip().upper()
                            while choice not in hands[p]:
                                choice = input("invalid card, try again: ").strip().upper()
                        else:
                            choice = choose_cpu_pass_card(hands[p])
                            print(f"\n{p} received {pass_card} and will discard {choice}")

                        hands[p].remove(choice)
                        discard.append(choice)
                        pass_card = None
                    else:
                        # middle players pass to the next
                        if p == human_name:
                            print(f"\n{p} received {pass_card}")
                            print("your hand:", hands[p])
                            choice = input("pass which card? ").strip().upper()
                            while choice not in hands[p]:
                                choice = input("invalid card, try again: ").strip().upper()
                        else:
                            choice = choose_cpu_pass_card(hands[p])
                            print(f"\n{p} received {pass_card} and will pass {choice}")

                        hands[p].remove(choice)
                        pass_card = choice  # goes to next player

            if triggered:
                break

            # check for any four of a kind after full table pass
            if any(evaluate_hand_strength(h) == "four of a kind" for h in hands.values()):
                triggered = True

        print("\n--- SPOON EVENT ---")
        result = spoon_event(hands)
        trigger = result["trigger"]
        spoons = result["spoons"]
        missed = result["no_spoon"]

        print(f"{trigger} triggered the event")
        print("got spoons:", ", ".join(spoons))
        print("missed spoon:", missed)

        scores, eliminated = update_score_and_eliminate(scores, missed)

        if eliminated:
            print("eliminated:", ", ".join(eliminated))

        round_num += 1

    winner = list(scores.keys())[0]
    print("\n=== GAME OVER ===")
    print("winner:", winner)


if __name__ == "__main__":
    run_game()
