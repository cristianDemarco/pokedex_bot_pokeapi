from dataclasses import dataclass


@dataclass
class PokemonAPIData:
    pokemon: dict
    species: dict
    variety: int
    types: str
    abilities: str
