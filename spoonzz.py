import random
import time
from collections import Counter


# ============================================================
# CARD CLASS
# ============================================================
class Card:
   def __init__(self, rank, suit):
       self.rank = rank
       self.suit = suit


   def __repr__(self):
       return f"{self.rank}{self.suit}"


   def get_rank(self):
       return self.rank


# ============================================================
# PLAYER CLASS
# ============================================================
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


   def has_four_kind(self):
       ranks = [c.get_rank() for c in self.hand]
       return 4 in Counter(ranks).values()


   # -----------------------
   # HUMAN chooses card
   # -----------------------
   def choose_card_human(self):
       print(f"\nYour hand: {self.show_hand()}")
       while True:
           chosen = input("Choose a card to pass (e.g. '10H'): ").strip()
           for c in self.hand:
               if str(c) == chosen:
                   return c
           print("❌ Invalid — choose EXACTLY a card in your hand.")


   # -----------------------
   # BOT chooses card
   # -----------------------
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


   # -----------------------
   # PASS LOGIC (human/bot)
   # -----------------------
   def choose_card_to_pass(self):
       if self.is_human:
           return self.choose_card_human()
       else:
           return self.choose_card_bot()


   # -----------------------
   # REACTION TIME LOGIC
   # -----------------------
   def reaction_time(self, human_has_4=False):
       if self.is_human:
           print("\n🚨🚨🚨 GRAB NOW!!! Type 'grab' FAST:")
           t0 = time.time()
           text = input(">>> ").strip().lower()
           t1 = time.time()
           if text != "grab":
               return float("inf")
           return t1 - t0


       # bots
       base = random.uniform(0.2, 1.1)
       if self.has_four_kind():
           base *= 0.8
       if self.name == "Bot1":
           base *= 0.95
       return base


# ============================================================
# GAME CLASS
# ============================================================
class Game:
   def __init__(self, players):
       self.players = players
       self.deck = []
       self.reset_deck()


   # -------------------------
   # DECK
   # -------------------------
   def reset_deck(self):
       ranks = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]
       suits = ["S","H","D","C"]
       self.deck = [Card(r, s) for r in ranks for s in suits]
       random.shuffle(self.deck)


   def draw(self):
       if not self.deck:
           self.reset_deck()
       return self.deck.pop()


   # -------------------------
   # DEAL
   # -------------------------
   def deal_initial(self):
       for _ in range(4):
           for p in self.players:
               p.receive_card(self.draw())


   # -------------------------
   # PASS CARDS LEFT
   # -------------------------
   def pass_left(self):
       chosen_cards = []


       # Each player chooses
       for p in self.players:
           chosen_cards.append(p.choose_card_to_pass())


       # Remove from hands
       for i, p in enumerate(self.players):
           p.remove_card(chosen_cards[i])


       # Pass left
       n = len(self.players)
       for i, p in enumerate(self.players):
           receive_from = (i - 1) % n
           p.receive_card(chosen_cards[receive_from])


   # -------------------------
   # CHECK FOUR-OF-A-KIND
   # -------------------------
   def check_winner(self):
       return [p for p in self.players if p.has_four_kind()]


   # -------------------------
   # SPOON SCRAMBLE
   # -------------------------
   def spoon_scramble(self, human):
       print("\n🕒 FOUR-OF-A-KIND! Spoon scramble begins!")
       winners = self.check_winner()
       print("Four-of-a-kind held by:", [p.name for p in winners])


       spoon_count = len(self.players) - 1


       # reaction times
       reactions = {}
       for p in self.players:
           reactions[p] = p.reaction_time(human_has_4=human.has_four_kind())


       # sort by fastest
       ordered = sorted(reactions.items(), key=lambda x: x[1])


       print("\n⚡ Reaction times (fast → slow):")
       for p, rt in ordered:
           print(f" - {p.name}: {rt:.3f}s" if rt != float('inf') else f" - {p.name}: ∞")


       # spoon takers
       grabbers = [p for p, _ in ordered[:spoon_count]]
       eliminated = ordered[-1][0]


       print(f"\n🏁 Spoons taken by: {[p.name for p in grabbers]}")
       print(f"❌ {eliminated.name} is eliminated!")


       self.players.remove(eliminated)
       return eliminated


   # -------------------------
   # PLAY ONE ROUND
   # -------------------------
   def play_round(self):
       print("\n--- NEW ROUND ---")
       # dealer draws card
       dealer = random.choice(self.players)
       card = self.draw()
       dealer.receive_card(card)


       print(f"Dealer: {dealer.name} drew {card}")


       # two fast cycles
       for _ in range(2):
           self.pass_left()


           # check four-of-a-kind
           if self.check_winner():
               return True
       return False


   # -------------------------
   # PLAY FULL GAME
   # -------------------------
   def play_game(self, human_player):
       self.deal_initial()


       while len(self.players) > 1:
           four_kind_triggered = self.play_round()


           if four_kind_triggered:
               self.spoon_scramble(human_player)
               self.reset_deck()
               for p in self.players:
                   p.hand = []
               self.deal_initial()


       print(f"\n🏆 WINNER: {self.players[0].name}")


# ============================================================
# RUN GAME
# ============================================================
if __name__ == "__main__":
   name = input("Enter your name: ").strip()
   if not name:
       name = "You"


   human = Player(name, is_human=True)
   bots = [Player("Bot1"), Player("Bot2"), Player("Bot3")]


   game = Game([human] + bots)
   game.play_game(human)