import random
from collections import Counter


# Card class

class Card:
    RANKS = ["2","3","4","5","6","7","8","9","10","J","Q","K","A"]
    SUITS = ["H","D","C","S"]

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return f"{self.rank}{self.suit}"

    def __repr__(self):
        return str(self)


# Deck class

class Deck:
    def __init__(self):
        self.cards = [Card(rank, suit) for rank in Card.RANKS for suit in Card.SUITS]
        random.shuffle(self.cards)

    def draw(self):
        if not self.cards:
            return None
        return self.cards.pop()

    def add_cards(self, cards):
        self.cards.extend(cards)
        random.shuffle(self.cards)


# Player class
class Player:
    def __init__(self, name, is_human=False):
        self.name = name
        self.is_human = is_human
        self.hand = []

    def draw_card(self, deck):
        card = deck.draw()
        if card:
            self.hand.append(card)
        return card

    def choose_card_to_pass(self):
        ranks = [card.rank for card in self.hand]
        counts = Counter(ranks)
        lowest_count = min(counts[r] for r in counts)
        candidate_ranks = [r for r in counts if counts[r] == lowest_count]
        chosen_rank = random.choice(candidate_ranks)
        for card in self.hand:
            if card.rank == chosen_rank:
                return card

    def remove_card(self, card):
        self.hand.remove(card)

    def evaluate_hand_strength(self):
        counts = Counter([card.rank for card in self.hand])
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


# Game class

class SpoonsGame:
    def __init__(self):
        self.players = []
        self.scores = {}
        self.round_num = 1
        self.discard_pile = []

    def setup_players(self):
        while True:
            try:
                num = int(input("How many total players? (2-6): "))
                if 2 <= num <= 6:
                    break
                print("Enter a number between 2 and 6")
            except ValueError:
                print("Enter a valid number")

        human_name = input("Your name: ").strip()
        if not human_name:
            human_name = "You"

        self.players.append(Player(human_name, is_human=True))
        for i in range(2, num+1):
            self.players.append(Player(f"CPU{i-1}"))

        self.scores = {p.name: 0 for p in self.players}

    def deal_hands(self, deck):
        for player in self.players:
            player.hand = [deck.draw() for _ in range(4)]

    def spoon_event(self):
        trigger = None
        for player in self.players:
            if player.evaluate_hand_strength() == "four of a kind":
                trigger = player
                break

        if not trigger:
            raise ValueError("No one has four of a kind")

        total_spoons = len(self.players) - 1
        spoon_receivers = {trigger.name}

        strength = {}
        for player in self.players:
            if player == trigger:
                continue
            strength[player.name] = max(Counter([c.rank for c in player.hand]).values())

        ranked = sorted(strength.keys(), key=lambda p: (strength[p], random.random()), reverse=True)
        for p in ranked:
            if len(spoon_receivers) < total_spoons:
                spoon_receivers.add(p)

        no_spoon = (set([p.name for p in self.players]) - spoon_receivers).pop()
        return {"trigger": trigger.name, "spoons": list(spoon_receivers), "no_spoon": no_spoon}

    def update_score_and_eliminate(self, missed):
        self.scores[missed] += 1
        eliminated = [p for p, score in list(self.scores.items()) if score >= 5]
        for p in eliminated:
            del self.scores[p]
        return eliminated

    def run(self):
        print("=== SPOONS GAME ===")
        self.setup_players()

        while len(self.scores) > 1:
            print(f"\n=== Round {self.round_num} ===")
            for p, score in self.scores.items():
                print(f"{p}: {score} letters")

            deck = Deck()
            self.deal_hands(deck)
            triggered = False

            while not triggered:
                pass_card = None
                for i, player in enumerate(self.players):
                    if player.name not in self.scores:
                        continue

                    if i == 0:
                        drawn = player.draw_card(deck)
                        if player.is_human:
                            print(f"\nYou drew {drawn}")
                            print("Your hand:", player.hand)
                            choice_input = input("Pass which card? ").upper()
                            while choice_input not in [str(c) for c in player.hand]:
                                choice_input = input("Invalid card. Try again: ").upper()
                            choice = next(c for c in player.hand if str(c) == choice_input)
                        else:
                            choice = player.choose_card_to_pass()
                        player.remove_card(choice)
                        pass_card = choice
                    else:
                        player.hand.append(pass_card)
                        if i == len(self.players) - 1:
                            choice = player.choose_card_to_pass()
                            player.remove_card(choice)
                            self.discard_pile.append(choice)
                            pass_card = None
                        else:
                            choice = player.choose_card_to_pass()
                            player.remove_card(choice)
                            pass_card = choice

                if any(p.evaluate_hand_strength() == "four of a kind" for p in self.players if p.name in self.scores):
                    triggered = True

            print("\n--- SPOON EVENT ---")
            result = self.spoon_event()
            print(f"{result['trigger']} triggered the event")
            print("Got spoons:", ", ".join(result['spoons']))
            print("Missed spoon:", result['no_spoon'])

            eliminated = self.update_score_and_eliminate(result['no_spoon'])
            if eliminated:
                print("Eliminated:", ", ".join(eliminated))

            self.round_num += 1

        winner = list(self.scores.keys())[0]
        print("\n=== GAME OVER ===")
        print("Winner:", winner)


if __name__ == "__main__":
    game = SpoonsGame()
    game.run()
