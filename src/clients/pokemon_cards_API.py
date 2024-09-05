from cached import cached
from pokemontcgsdk import Card
import logging

class PokemonCardsAPI:

    @cached
    def get_cards(self, name) -> None:
        cards = Card.where(q=f'name:{name}')
        cards = "\n".join(card.name for card in cards)
        return cards
    
    def get_cards_number(self):
        return len(self.cards)