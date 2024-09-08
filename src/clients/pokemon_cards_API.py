from cached import cached
from pokemontcgsdk import Card
from models.pokemon_card import PokemonCard
from dataclasses import asdict

class PokemonCardsAPI:

    @cached
    def get_cards(self, name: str) -> str:
        cards = Card.where(q=f'name:{name}', orderBy='-set.releaseDate')
        cards_list = "\n".join(" ".join([card.name, f'[{card.number}/{card.set.total}]']) for card in cards)

        return cards_list
    
    @cached
    def get_card(self, name: str) -> PokemonCard:
        card = Card.where(q=f'name:{name}')[0]
        pokemon_card = PokemonCard(
            name=card.name,
            photo=card.images.large,
            set=card.set.name,
            price=card.cardmarket.prices.averageSellPrice
        )
        return asdict(pokemon_card)
    
    def get_cards_number(self) -> int:
        return len(self.cards)
