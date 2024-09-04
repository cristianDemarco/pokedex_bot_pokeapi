import re
import sys
import os
import random
import logging

from models.Pokemon import Pokemon
from models.pokemonAPIData import PokemonAPIData
from TEXTS import TEXTS

class PokemonElaborateData: 
    def __init__(self, data : PokemonAPIData) -> None:
        self.pokemon = data.pokemon
        self.species = data.species
        self.variety = data.variety
        self.types = data.types
        self.abilities = data.abilities

    def elaborate(self) -> None:
        name = self.pokemon["name"].capitalize().split("-", 1)[0]
        
        id = str(self.species["id"])

        generation = self.species["generation"]["url"]
        generation = re.search(pattern = r"/generation/(\d+)/",
                               string = generation).group(1)

        photo = self.pokemon["sprites"]["other"]["official-artwork"]["front_default"]
        photo_link = photo.replace("PokeAPI/sprites", "cristianDemarco/PokeAPI_sprites")
        
        warning = ""
        descriptions = self.species["flavor_text_entries"]

        descriptions_set = set(description["flavor_text"] for description in descriptions if description["language"]["name"] == "it")

        if len(descriptions_set) == 0:
            descriptions_set = set(description["flavor_text"] for description in descriptions if description["language"]["name"] == "en")
            warning = TEXTS["IT"]["ITALIAN_DESCRIPTION_NOT_AVAILABLE"]

        try:
            description = warning + " ".join(random.choice(list(descriptions_set)).split())
        except Exception as e:
            description = TEXTS["IT"]["DESCRIPTION_NOT_AVAILABLE"]
            logging.exception(e)
        
        is_legendary = self.species["is_legendary"]
        is_mythical = self.species["is_mythical"]
        number_of_varieties = len(self.species["varieties"])

        variety = self.variety
        if int(self.variety) > number_of_varieties-1:
            variety = 0

        return Pokemon(name=name,
                       id=id,
                       generation=generation,
                       abilities=self.abilities,
                       is_legendary=is_legendary,
                       is_mythical=is_mythical,
                       photo=photo_link,
                       types=self.types,
                       description=description,
                       variety=variety, 
                       number_of_varieties=number_of_varieties)      