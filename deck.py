from card import Card
import random
class Deck:
    deck = []
    ongoing_cards = []

    def __init__(self, name: str, deck: dict):
        self.stored_deck = deck.cards
        self.name = name
        self.size = deck.size
        self.theme = deck.theme
        self.deck = self.create_deck()
        self.shuffle_deck()

    def create_deck(self):
        deck = []
        for card_name, card in self.stored_deck.items():
            card_type = "None"
            if "Ongoing" in card.attributes:
                card_type = "Ongoing"
            for i in range(card.count):
                c = Card(card_name, card.effect, card_type)
                deck.append(c)
        return deck

    def reset_deck(self):
        self.deck = []
        self.deck = self.create_deck()
        self.shuffle_deck()

    def shuffle_deck(self):
        random.shuffle(self.deck)

    def draw_card(self):
        drawn_card = self.deck.pop()

        if drawn_card.type == "Ongoing":
            self.ongoing_cards.append(drawn_card)

        self.deck.insert(0, drawn_card)
        return drawn_card

    def draw_and_pick(self, choice = -1):
        if choice == -1:
            dlast = self.deck[len(self.deck)]
            dSlast = self.deck[len(self.deck)-1]
            return [dlast, dSlast]

        if choice == 0:
            c = self.draw_card()
            secondChoice = self.deck.pop()
            self.deck.insert(0, secondChoice)
            return c

        if choice == 1:
            secondChoice = self.deck.pop()
            self.deck.insert(0, secondChoice)
            c = self.draw_card()
            return c

        return -1