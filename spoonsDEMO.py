import random
import time
from collections import Counter


#  CARD CLASS 
class Card:
    """Represents a single playing card."""
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        """
        Args:
            rank (str): The rank of the card
            suit (str): The suit of the card
        """

    def __repr__(self):
        return f"{self.rank}{self.suit}"

    def get_rank(self):
        return self.rank


# PLAYER CLASS 
class Player:
    def __init__(self, name, is_human=False):
        self.name = name
        self.is_human = is_human
        self.hand = []
        self.target_rank = None

    def receive_card(self, card):
        self.hand.append(card)

    def remove_card(self, card):
        self.hand.remove(card)

    def show_hand(self):
        return [str(c) for c in self.hand]

    def has_three_or_more(self):
        ranks = [c.get_rank() for c in self.hand]
        counts = Counter(ranks).values()
        return any(c >= 3 for c in counts)

    # HUMAN chooses card
    def choose_card_human(self):
        print(f"\nYour hand: {self.show_hand()}")
        while True:
            chosen = input("Choose a card to pass: ").strip()
            for c in self.hand:
                if str(c) == chosen:
                    return c
            print("Invalid. Choose a card exactly as shown in your hand.")

    # BOT chooses card
    def choose_bot_target(self):
        ranks = [c.get_rank() for c in self.hand]
        counts = Counter(ranks)
        top_count = max(counts.values())
        candidates = [r for r, c in counts.items() if c == top_count]
        self.target_rank = random.choice(candidates)

    def choose_card_bot(self):
        if not self.target_rank:
            self.choose_bot_target()
        non_targets = [c for c in self.hand if c.get_rank() != self.target_rank]
        if non_targets:
            return random.choice(non_targets)
        return random.choice(self.hand)

    def choose_card_to_pass(self):
        return self.choose_card_human() if self.is_human else self.choose_card_bot()

    # REACTION TIME LOGIC
    def reaction_time(self):
        if self.is_human:
            print("\nSET FOUND! Type 'g' fast:")
            t0 = time.time()
            text = input(">>> ").strip().lower()
            t1 = time.time()
            if text != "g":
                return float("inf")
            return max(0.25, t1 - t0)
        # BOT slower for human advantage
        base = random.uniform(0.8, 1.5)  # slower than before
        if self.has_three_or_more():
            base *= random.uniform(0.9, 1.1)
        return base


#  GAME CLASS 
class Game:
    def __init__(self, players):
        self.players = players
        self.deck = []
        self.reset_deck()

    # DECK (small fixed deck)
    def reset_deck(self):
        ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9"]
        suits = ["H", "D"]  # small deck
        self.deck = [Card(r, s) for r in ranks for s in suits]
        random.shuffle(self.deck)

    def draw(self):
        if not self.deck:
            self.reset_deck()
        return self.deck.pop()

    # DEAL INITIAL HANDS
    def deal_initial(self):
        for _ in range(3):  # 3-card hands for faster rounds
            for p in self.players:
                p.receive_card(self.draw())

    # PASS LEFT
    def pass_left(self):
        chosen_cards = [p.choose_card_to_pass() for p in self.players]
        for i, p in enumerate(self.players):
            p.remove_card(chosen_cards[i])
        n = len(self.players)
        for i, p in enumerate(self.players):
            p.receive_card(chosen_cards[(i - 1) % n])

    # CHECK SET
    def check_winner(self):
        return [p for p in self.players if p.has_three_or_more()]

    # SPOON SCRAMBLE
    def spoon_scramble(self, human):
        print("\nTHREE OF A KIND OR BETTER DETECTED!")
        winners = self.check_winner()
        print("Set found by:", [p.name for p in winners])

        spoon_count = len(self.players) - 1
        reactions = {p: p.reaction_time() for p in self.players}
        ordered = sorted(reactions.items(), key=lambda x: x[1])

        print("\nReaction times (fast to slow):")
        for p, rt in ordered:
            if rt == float("inf"):
                print(f" - {p.name}: did not grab")
            else:
                print(f" - {p.name}: {rt:.2f} sec")

        grabbers = [p for p, _ in ordered[:spoon_count]]
        eliminated = ordered[-1][0]

        print(f"\nSpoons taken by: {[p.name for p in grabbers]}")
        print(f"{eliminated.name} is eliminated.")

        self.players.remove(eliminated)
        return eliminated

    # PLAY ONE ROUND
    def play_round(self):
        print("\n--- NEW ROUND ---")
        dealer = random.choice(self.players)
        card = self.draw()
        dealer.receive_card(card)
        print(f"Dealer {dealer.name} drew {card}")

        for _ in range(2):  # two cycles of passing
            self.pass_left()
            if self.check_winner():
                return True
        return False

    # PLAY FULL GAME
    def play_game(self, human_player):
        self.deal_initial()
        while len(self.players) > 1:
            set_triggered = self.play_round()
            if set_triggered:
                self.spoon_scramble(human_player)
                self.reset_deck()
                for p in self.players:
                    p.hand = []
                self.deal_initial()
        print(f"\nWINNER: {self.players[0].name}")


#  RUN GAME 
if __name__ == "__main__":
    name = input("Enter your name: ").strip() or "You"
    human = Player(name, is_human=True)
    bots = [Player("Bot1"), Player("Bot2"), Player("Bot3")]

    game = Game([human] + bots)
    game.play_game(human)
