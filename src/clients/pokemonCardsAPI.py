from cached import CacheManager
from pokemontcgsdk import Card

class pokemonCardsAPI:

    def __init__(self):
        self.cache_manager = CacheManager(URL='https://pokeapi.co/api', API_VERSION = 'v2')

    def get_cards(self, name) -> None:
        cards = Card.where(q=f'name:{name}')
        return cards
    
    def get_cards_number(self):
        return len(self.cards)