"""
Spoons Game — INST326 Final Project Edition

Text-based version of the card game Spoons.

Features:
- Object-oriented design (Card, Deck, Player, SpoonsGame)
- Helper functions for hand evaluation, spoon event, and scoring
- Passing pipeline where players go 4 -> 5 -> 4 cards each cycle
- Reaction-based spoon scramble (press 'g' as fast as possible)
- Deck uses only 10, J, Q, K, A, but with two copies of each card
"""

import random
import time
from collections import Counter


def evaluate_hand_strength(hand):
    """
    Determine the strength of a 4-card hand by counting matching ranks.

    Primary Author
    --------------
    Juanita Asenso

    Techniques Claimed
    ------------------
    comprehensions or generator expressions
    """
    ranks = [card.rank for card in hand]
    counts = Counter(ranks)
    values = sorted(counts.values(), reverse=True)

    if values == [4]:
        return "four of a kind"
    if values == [3, 1]:
        return "three of a kind"
    if values == [2, 2]:
        return "two pair"
    if values == [2, 1, 1]:
        return "one pair"
    return "high card"


def spoon_event(players, trigger_name):
    """
    Handle the spoon scramble using real reaction timing.

    Primary Author
    --------------
    Ayushi Bhola

    Techniques Claimed
    ------------------
    use of a key function with sorted()
    """
    total_spoons = len(players) - 1
    reaction_times = {}

    print("\nSPOON SCRAMBLE!")
    print("When 'GO!' appears, press 'g' and hit Enter as fast as you can.")
    input("Press Enter to get ready...")

    time.sleep(random.uniform(0.5, 1.5))
    print("GO!")

    for p in players:
        if p.is_human:
            start = time.perf_counter()
            ans = input("> ").strip().lower()
            end = time.perf_counter()
            t = end - start
            if ans != "g":
                t += 1.0
        else:
            t = random.uniform(0.6, 1.5)

        reaction_times[p.name] = t

    if trigger_name in reaction_times:
        reaction_times[trigger_name] *= 0.9

    ordered = sorted(players, key=lambda p: reaction_times[p.name])

    return {
        "trigger": trigger_name,
        "spoons": [p.name for p in ordered[:total_spoons]],
        "no_spoon": ordered[-1].name,
        "reaction_times": reaction_times
    }


def update_score_and_eliminate(scores, player_missed):
    """
    Update scores and remove eliminated players.

    Primary Author
    --------------
    Juanita Asenso

    Techniques Claimed
    ------------------
    None
    """
    scores[player_missed] += 1
    eliminated = []

    for name, total in list(scores.items()):
        if total >= 5:
            eliminated.append(name)
            del scores[name]

    return scores, eliminated


class Card:
    """
    Represents a playing card.

    Primary Author
    --------------
    Tylor Davis

    Techniques Claimed
    ------------------
    None
    """

    RANKS = ["10", "J", "Q", "K", "A"]
    SUITS = ["H", "D", "C", "S"]

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        """
        String representation of a card.

        Primary Author
        --------------
        Tylor Davis

        Techniques Claimed
        ------------------
        f-strings containing expressions
        """
        return f"{self.rank}{self.suit}"

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return isinstance(other, Card) and self.rank == other.rank and self.suit == other.suit

    def __hash__(self):
        return hash((self.rank, self.suit))


class Deck:
    """
    Deck containing all cards used in the game.

    Primary Author
    --------------
    Michael Miceli

    Techniques Claimed
    ------------------
    None
    """

    def __init__(self):
        self.cards = [
            Card(r, s)
            for _ in range(2)
            for r in Card.RANKS
            for s in Card.SUITS
        ]
        random.shuffle(self.cards)

    def draw(self):
        """
        Draw a card from the deck.

        Primary Author
        --------------
        Michael Miceli

        Techniques Claimed
        ------------------
        None
        """
        return self.cards.pop() if self.cards else None

    def __len__(self):
        """
        Number of remaining cards.

        Primary Author
        --------------
        Michael Miceli

        Techniques Claimed
        ------------------
        magic methods other than __init__()
        """
        return len(self.cards)


class Player:
    """
    Represents a human or CPU player.

    Primary Author
    --------------
    Michael Miceli

    Techniques Claimed
    ------------------
    optional parameters and/or keyword arguments
    """

    def __init__(self, name, is_human=False):
        self.name = name
        self.is_human = is_human
        self.hand = []

    def draw_card(self, deck):
        """
        Draw a card and add to hand.

        Primary Author
        --------------
        Michael Miceli

        Techniques Claimed
        ------------------
        None
        """
        card = deck.draw()
        if card:
            self.hand.append(card)
        return card

    def choose_card_to_pass(self):
        """
        Choose weakest card to pass.

        Primary Author
        --------------
        Tylor Davis

        Techniques Claimed
        ------------------
        set operations on sets
        """
        ranks = [c.rank for c in self.hand]
        counts = Counter(ranks)
        weakest = min(counts.values())
        weak_ranks = {r for r, c in counts.items() if c == weakest}
        chosen_rank = random.choice(list(weak_ranks))

        for c in self.hand:
            if c.rank == chosen_rank:
                return c

    def hand_strength(self):
        """
        Compute hand strength.

        Primary Author
        --------------
        Juanita Asenso

        Techniques Claimed
        ------------------
        None
        """
        return evaluate_hand_strength(self.hand)

    def __str__(self):
        return f"{self.name}: {self.hand}"


class SpoonsGame:
    """
    Main game controller.

    Primary Author
    --------------
    Ayushi Bhola

    Techniques Claimed
    ------------------
    composition of two custom classes
    """

    def __init__(self):
        self.players = []
        self.scores = {}
        self.round_num = 1
        self.discard_pile = []

    def setup_players(self):
        """
        Create players.

        Primary Author
        --------------
        Ayushi Bhola

        Techniques Claimed
        ------------------
        None
        """
        while True:
            try:
                n = int(input("How many total players? (2–5): "))
                if 2 <= n <= 5:
                    break
            except ValueError:
                pass

        name = input("Your name: ").strip() or "You"
        self.players.append(Player(name, is_human=True))
        for i in range(2, n + 1):
            self.players.append(Player(f"CPU{i-1}"))

        self.scores = {p.name: 0 for p in self.players}

    def deal_hands(self, deck):
        """
        Deal initial hands.

        Primary Author
        --------------
        Michael Miceli

        Techniques Claimed
        ------------------
        None
        """
        for p in self.players:
            p.hand = [deck.draw() for _ in range(4)]

    def active_players(self):
        """
        Return non-eliminated players.

        Primary Author
        --------------
        Juanita Asenso

        Techniques Claimed
        ------------------
        None
        """
        return [p for p in self.players if p.name in self.scores]

    def run(self):
        """
        Main game loop.

        Primary Author
        --------------
        Ayushi Bhola

        Techniques Claimed
        ------------------
        None
        """
        print("=== SPOONS GAME ===")
        self.setup_players()

        while len(self.scores) > 1:
            deck = Deck()
            self.deal_hands(deck)

            triggered = False
            trigger_name = None

            while not triggered:
                active = self.active_players()
                pass_card = None

                for i, player in enumerate(active):
                    if i == 0:
                        drawn = player.draw_card(deck)
                        if player.is_human:
                            print("\nYou drew", drawn)
                            print("Your hand:", player.hand)
                            pick = input("Pass which card? ").upper()
                            while pick not in [str(c) for c in player.hand]:
                                pick = input("Invalid card. Try again: ").upper()
                            chosen = next(c for c in player.hand if str(c) == pick)
                        else:
                            chosen = player.choose_card_to_pass()

                        player.hand.remove(chosen)
                        pass_card = chosen
                    else:
                        if pass_card:
                            player.hand.append(pass_card)

                        chosen = player.choose_card_to_pass()
                        player.hand.remove(chosen)

                        if i == len(active) - 1:
                            self.discard_pile.append(chosen)
                            pass_card = None
                        else:
                            pass_card = chosen

                for p in active:
                    if p.hand_strength() == "four of a kind":
                        triggered = True
                        trigger_name = p.name
                        break

            event = spoon_event(self.active_players(), trigger_name)
            self.scores, eliminated = update_score_and_eliminate(self.scores, event["no_spoon"])
            self.round_num += 1

        print("\nWinner:", list(self.scores.keys())[0])


def main():
    """
    Program entry point.

    Primary Author
    --------------
    Michael Miceli

    Techniques Claimed
    ------------------
    None
    """
    SpoonsGame().run()


if __name__ == "__main__":
    main()


