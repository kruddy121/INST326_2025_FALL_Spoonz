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

    Parameters
    ----------
    hand : list[Card]
        The player's current 4-card hand.

    Returns
    -------
    str
        One of: 'four of a kind', 'three of a kind',
        'two pair', 'one pair', or 'high card'.

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

    The human must press 'g' after the 'GO!' signal as fast as possible.
    CPU players get randomized reaction times to keep it competitive.

    Parameters
    ----------
    players : list[Player]
        All active players still in the game.
    trigger_name : str
        Name of the player who achieved four-of-a-kind.

    Returns
    -------
    dict
        Dictionary with:
        - 'trigger': player who triggered the event
        - 'spoons': list of players who got spoons
        - 'no_spoon': player who missed a spoon
        - 'reaction_times': dict mapping player name -> time in seconds

    Primary Author
    --------------
    Ayushi Bhola

    Techniques Claimed
    ------------------
    use of a key function (which can be a lambda expression) with one of the following commands: list.sort(), sorted(), min(), or max()
    """
    total_spoons = len(players) - 1
    reaction_times = {}

    print("\nSPOON SCRAMBLE!")
    print("When 'GO!' appears, press 'g' and hit Enter as fast as you can.")
    input("Press Enter to get ready...")

    # Small random delay so you can't just spam
    time.sleep(random.uniform(0.5, 1.5))
    print("GO!")

    for p in players:
        if p.is_human:
            start = time.perf_counter()
            ans = input("> ").strip().lower()
            end = time.perf_counter()
            t = end - start

            # Penalty for not pressing g
            if ans != "g":
                t += 1.0
        else:
            # CPU reaction window – tweak to adjust difficulty
            t = random.uniform(0.6, 1.5)

        reaction_times[p.name] = t

    # Small advantage for the player who actually hit four-of-a-kind
    if trigger_name in reaction_times:
        reaction_times[trigger_name] *= 0.9

    # Sort fastest → slowest
    ordered = sorted(players, key=lambda p: reaction_times[p.name])

    spoon_receivers = [p.name for p in ordered[:total_spoons]]
    no_spoon = ordered[-1].name

    return {
        "trigger": trigger_name,
        "spoons": spoon_receivers,
        "no_spoon": no_spoon,
        "reaction_times": reaction_times
    }


def update_score_and_eliminate(scores, player_missed):
    """
    Increase the missed player's letter count and remove them if they reach 5.

    Parameters
    ----------
    scores : dict[str, int]
        Mapping of player name -> letter count.
    player_missed : str
        Player who did not get a spoon during this event.

    Returns
    -------
    tuple[dict[str, int], list[str]]
        Updated scores dictionary and list of eliminated players.

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
    A playing card used in the game.

    Attributes
    ----------
    rank : str
        Card rank: '10', 'J', 'Q', 'K', or 'A'.
    suit : str
        Suit: 'H', 'D', 'C', or 'S'.
    """

    RANKS = ["10", "J", "Q", "K", "A"]
    SUITS = ["H", "D", "C", "S"]

    def __init__(self, rank, suit):
        if rank not in Card.RANKS:
            raise ValueError("Invalid card rank.")
        if suit not in Card.SUITS:
            raise ValueError("Invalid card suit.")
        self.rank = rank
        self.suit = suit

    def __str__(self):
        """
        Return a short string representation of the card (rank + suit).

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
    The deck used in the game.

    Uses only the ranks 10, J, Q, K, A, but has two copies of each
    card in each suit (40 cards total) so there are always cards to draw.

    Methods
    -------
    draw()
        Draw a card from the deck.
    __len__()
        Return number of cards remaining.
    """

    def __init__(self):
        self.cards = []
        for _ in range(2):  # two copies of each card
            for r in Card.RANKS:
                for s in Card.SUITS:
                    self.cards.append(Card(r, s))
        random.shuffle(self.cards)

    def draw(self):
        """
        Draw a single card from the deck.

        Returns
        -------
        Card or None
            The drawn card, or None if the deck is empty.
        """
        return self.cards.pop() if self.cards else None

    def __len__(self):
        """
        Return the number of cards remaining in the deck.

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

    Attributes
    ----------
    name : str
        Player's display name.
    is_human : bool
        True if this player is controlled by the user.
    hand : list[Card]
        The player's current hand.
    """

    def __init__(self, name, is_human=False):
        """
        Create a Player with a name and control type.

        Primary Author
        --------------
        Michael Miceli

        Techniques Claimed
        ------------------
        optional parameters and/or keyword arguments
        """
        self.name = name
        self.is_human = is_human
        self.hand = []

    def draw_card(self, deck):
        """
        Draw a card from the deck and add it to this player's hand.

        Parameters
        ----------
        deck : Deck
            Deck to draw from.

        Returns
        -------
        Card or None
            The drawn card, if there is one.
        """
        card = deck.draw()
        if card:
            self.hand.append(card)
        return card

    def choose_card_to_pass(self):
        """
        Choose a card to pass based on weakest rank frequency.

        CPU strategy:
        - Count how many of each rank are in the hand.
        - Find the least common rank(s).
        - Pass one card of a least-common rank.

        Primary Author
        --------------
        Tylor Davis

        Techniques Claimed
        ------------------
        use of a key function (which can be a lambda expression) with one of the following commands: list.sort(), sorted(), min(), or max()
        """
        ranks = [c.rank for c in self.hand]
        counts = Counter(ranks)
        weakest_count = min(counts.values())
        weak_ranks = [r for r, c in counts.items() if c == weakest_count]
        chosen_rank = random.choice(weak_ranks)

        for c in self.hand:
            if c.rank == chosen_rank:
                return c

    def hand_strength(self):
        """
        Compute this player's hand strength using the shared helper.

        Returns
        -------
        str
            Category label for the hand strength.
        """
        return evaluate_hand_strength(self.hand)

    def __str__(self):
        return f"{self.name}: {self.hand}"


class SpoonsGame:
    """
    Main controller for the Spoons game.

    Responsibilities:
    - Set up players
    - Deal cards
    - Run passing pipeline (4 -> 5 -> 4 cards each cycle)
    - Trigger timed spoon event on four-of-a-kind
    - Track letters and eliminate players
    - Announce the final winner
    """

    def __init__(self):
        self.players = []
        self.scores = {}
        self.round_num = 1
        self.discard_pile = []

    def setup_players(self):
        """
        Ask for number of players (2–5) and create human + CPU players.
        """
        while True:
            try:
                n = int(input("How many total players? (2–5): "))
                if 2 <= n <= 5:
                    break
                print("Enter a number between 2 and 5.")
            except ValueError:
                print("Please enter a valid number.")

        name = input("Your name: ").strip() or "You"
        self.players.append(Player(name, is_human=True))

        for i in range(2, n + 1):
            self.players.append(Player(f"CPU{i-1}"))

        self.scores = {p.name: 0 for p in self.players}

    def deal_hands(self, deck):
        """
        Deal four cards to each player from the deck.

        Parameters
        ----------
        deck : Deck
            The deck to deal from.
        """
        for p in self.players:
            p.hand = [deck.draw() for _ in range(4)]

    def active_players(self):
        """
        Players still in the game (not eliminated).

        Returns
        -------
        list[Player]
        """
        return [p for p in self.players if p.name in self.scores]

    def run(self):
        """
        Run the main game loop until only one player remains.

        Primary Author
        --------------
        Ayushi Bhola

        Techniques Claimed
        ------------------
        composition of two custom classes
        """
        print("=== SPOONS GAME ===")
        self.setup_players()

        while len(self.scores) > 1:
            print(f"\n=== Round {self.round_num} ===")
            for name, letters in self.scores.items():
                print(f"{name}: {letters} letters")

            deck = Deck()
            self.deal_hands(deck)
            triggered = False
            trigger_name = None

            # Passing continues until someone gets four-of-a-kind.
            while not triggered:
                active = self.active_players()
                pass_card = None  # card being passed along the circle

                for i, player in enumerate(active):
                    if i == 0:
                        # First player draws from the deck at the start of each cycle
                        drawn = player.draw_card(deck)
                        if player.is_human:
                            print(f"\nYou drew {drawn}")
                            print("Your hand:", player.hand)
                            pick = input("Pass which card? ").upper()
                            while pick not in [str(c) for c in player.hand]:
                                pick = input("Invalid card. Try again: ").upper()
                            chosen = next(c for c in player.hand if str(c) == pick)
                        else:
                            chosen = player.choose_card_to_pass()

                        # Remove chosen and start the pass pipeline
                        player.hand.remove(chosen)
                        pass_card = chosen

                    else:
                        # Other players first receive the passed card (if any)
                        if pass_card is not None:
                            player.hand.append(pass_card)

                        # Now they have 5 cards; choose one to pass
                        chosen = player.choose_card_to_pass()
                        player.hand.remove(chosen)

                        if i == len(active) - 1:
                            # Last player: their passed card is discarded
                            self.discard_pile.append(chosen)
                            pass_card = None
                        else:
                            # Middle player: pass along to next player
                            pass_card = chosen

                # After a full rotation, everyone should be back to 4 cards.
                # Check for four-of-a-kind now.
                for p in active:
                    if p.hand_strength() == "four of a kind":
                        triggered = True
                        trigger_name = p.name
                        break

            print("\n--- SPOON EVENT ---")
            event = spoon_event(self.active_players(), trigger_name)

            print("\nSPOON EVENT RESULTS")
            print(f"Trigger: {event['trigger']}")
            print("Got spoons:", ", ".join(event["spoons"]))
            print("Missed spoon:", event["no_spoon"])

            print("\nReaction Times (fastest first):")
            for name, t in sorted(event["reaction_times"].items(), key=lambda x: x[1]):
                print(f"  {name}: {t:.3f} seconds")

            self.scores, eliminated = update_score_and_eliminate(
                self.scores, event["no_spoon"]
            )

            if eliminated:
                print("Eliminated:", ", ".join(eliminated))

            self.round_num += 1

        print("\n=== GAME OVER ===")
        print("Winner:", list(self.scores.keys())[0])


def main():
    """
    Entry point for running the Spoons game.
    """
    game = SpoonsGame()
    game.run()


if __name__ == "__main__":
    main()

