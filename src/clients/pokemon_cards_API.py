from cached import cached
from pokemontcgsdk import Card
import logging

class PokemonCardsAPI:

    @cached
    def get_cards(self, name) -> None:
        cards = Card.where(q=f'name:{name}')
        sorted_cards = sorted(cards, key=lambda card: card.set.releaseDate)
        cards_list = "\n".join(" ".join([card.name, f'[{card.number}/{card.set.total}]']) for card in sorted_cards)

        return cards_list
    
    def get_cards_number(self):
        return len(self.cards)