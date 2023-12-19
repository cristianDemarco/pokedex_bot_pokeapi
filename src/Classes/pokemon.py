from typing import List

class Pokemon:
    
    def __init__(self, name : str, id : str, generation : str, abilities, is_legendary : bool, is_mythical : bool, photo : str, types : List, description : str, variety : int, number_of_varieties : int) -> None:
        self.name = name
        self.id = id
        self.generation = generation
        self.abilities = abilities
        self.is_legendary = is_legendary
        self.is_mythical =  is_mythical
        self.photo = photo
        self.types = types
        self.description = description
        self.variety = variety
        self.number_of_varieties = number_of_varieties