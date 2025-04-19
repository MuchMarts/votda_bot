class Player:
    def __init__(self, name, id, stats: list[int] = None, max_hp: int = None):
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
    
    def load_player(self, player_id: int):
        return
    
    

class Stats:
    def __init__(self, m: int, v: int, f: int):
        self.m = m
        self.v = v
        self.f = f