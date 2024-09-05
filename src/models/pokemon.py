from dataclasses import dataclass
from typing import List

@dataclass
class Pokemon:
    name : str
    id : str
    photo : str
    description : str
    generation : str
    abilities : str
    is_legendary : bool
    is_mythical : bool
    variety : str
    number_of_varieties : int
    types : List