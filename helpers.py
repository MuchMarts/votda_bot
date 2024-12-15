import json

def parse_deck(file_path):
    deck = {}
    with open(file_path, 'r', encoding="utf-8") as file:
        lines = file.readlines()

        deck_name = None
        current_card = None

        for line in lines:
            line = line.strip()

            if line.startswith("Deck Name:"):
                deck_name = line.split(":", 1)[1].strip()
                deck[deck_name] = {"cards": {}}
            elif line.startswith("Card Count:"):
                deck[deck_name]["size"] = int(line.split(":", 1)[1].strip())
            elif line.startswith("Theme:"):
                deck[deck_name]["theme"] = line.split(":", 1)[1].strip().strip('"')
            elif line and not line.startswith("Cards:") and not line.startswith("Effect:"):
                # This line describes a card name and its details
                card_details = line.split("(", 1)
                card_name = card_details[0].strip()
                attributes = card_details[1].strip(")").split(", ")  if len(card_details) > 1 else ""
                deck[deck_name]["cards"][card_name] = {"attributes": attributes}
                current_card = card_name
            elif line.startswith("Effect:") and current_card:
                effect = line.split(":", 1)[1].strip()
                deck[deck_name]["cards"][current_card]["effect"] = effect

    return deck
