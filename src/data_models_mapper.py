import random
import logging
from models.pokemon import Pokemon
from models.pokemon_API_data import PokemonAPIData
from TEXTS import TEXTS

def map_API_data_to_pokemon(data : PokemonAPIData) -> Pokemon:
    name = data.pokemon["name"].capitalize().split("-", 1)[0]
    id = str(data.species["id"])
    generation = data.species["generation"]["url"][-2]

    photo = data.pokemon["sprites"]["other"]["official-artwork"]["front_default"]
    photo_link = photo.replace("PokeAPI/sprites", "cristianDemarco/PokeAPI_sprites")

    warning = ""
    descriptions = data.species["flavor_text_entries"]
    descriptions_set = set(description["flavor_text"] for description in descriptions if description["language"]["name"] == "it")

    if len(descriptions_set) == 0:
        descriptions_set = set(description["flavor_text"] for description in descriptions if description["language"]["name"] == "en")
        warning = TEXTS["IT"]["ITALIAN_DESCRIPTION_NOT_AVAILABLE"]

    try:
        description = warning + " ".join(random.choice(list(descriptions_set)).split())
    except Exception as e:
        description = TEXTS["IT"]["DESCRIPTION_NOT_AVAILABLE"]
        logging.exception(e)

    is_legendary = data.species["is_legendary"]
    is_mythical = data.species["is_mythical"]
    number_of_varieties = len(data.species["varieties"])

    variety = data.variety
    if int(data.variety) > number_of_varieties-1:
        variety = 0

    return Pokemon(
        name=name,
        id=id,
        generation=generation,
        abilities=data.abilities,
        is_legendary=is_legendary,
        is_mythical=is_mythical,
        photo=photo_link,
        types=data.types,
        description=description,
        variety=variety, 
        number_of_varieties=number_of_varieties)  




