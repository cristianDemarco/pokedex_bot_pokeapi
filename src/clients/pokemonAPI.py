from models.pokemonAPIData import PokemonAPIData
from CacheManager import CacheManager

class PokemonAPI:

    def __init__(self):
        self.cache_manager = CacheManager(URL='https://pokeapi.co/api', API_VERSION = 'v2')

    def get_pokemon_count(self) -> int:
        api = self.cache_manager.get('pokemon-species/?limit=0')

        return api["count"]

    def get_pokemon_species(self, pokemon: str) -> dict:
        api = f'pokemon-species/{pokemon}'
        return self.cache_manager(api)
    
    def get_pokemon_variety(self, pokemon_variety: str) -> dict:
        api = f'pokemon/{pokemon_variety}'
        return self.cache_manager(api)
    
    def get_api_data(self, pokemon : str, variety : int = 0) -> PokemonAPIData:
        
        species_data = self.cache_manager_pokemon_species(pokemon=pokemon)

        if variety > len(species_data["varieties"]) - 1:
            variety = 0
                    
        pokemon_variety = species_data["varieties"][variety]["pokemon"]["name"]
        pokemon_data = self.cache_manager_pokemon_variety(pokemon_variety=pokemon_variety)
        
        types = self.cache_manager_list_of_elements(pokemon_data, "types", "type")
        abilities = self.cache_manager_list_of_elements(pokemon_data, "abilities", "ability")

        return PokemonAPIData(pokemon_data, species_data, variety, types, abilities)
    
    def get_list_of_elements(self, data, elements : str, element : str, language : str = "it") -> str:
        # Return a string containing a list of names separated by commas (for example types, abilities)
        elements_list = []

        for value in data[elements]:
            element_api = value[element]["url"]
            element_data = self.cache_manager(element_api)
            for item in element_data["names"]:
                if item["language"]["name"] == language:
                    elements_list.append(item["name"])
                    break

        #Delete duplicates

        elements_list = list(set(elements_list))

        #Lowercase all elements in list except the first one

        elements_list = [elements_list[0]] + [x.lower() for x in elements_list[1:]]

        return ", ".join(elements_list)  