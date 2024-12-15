class Player:
    def __init__(self, name, id):
        self.name = name
        self.id = id

    strain_cards = []
    strain_taken = 0
    def add_strain_card(self, card):
        self.strain_cards.append(card)
        self.strain_taken += 1
    
    def remove_strain_card(self, card):
        self.strain_cards.remove(card)
    
    def get_strain_cards(self):
        return self.strain_cards