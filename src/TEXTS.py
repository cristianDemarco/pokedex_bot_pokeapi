import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

TEXTS = {
    "SEARCH_POKEMON_KEYWORD" : "pokemon",
    "SEARCH_POKEMON_COMAND" : "/pokemon",
    "IT":{
        "POKEDEX_RETURN_MESSAGE" : f"""
<name> N°<id><b><is_legendary></b><b><is_mythical></b>
<generation>° Generazione
<b>Tipo:</b> <types>
<b>Abilità:</b> <abilities>\n
<b>Descrizione:</b> <description>
""",
        "START_MESSAGE_TEXT" : rf"Benvenuto <username>! Questo è un bot che ti permette di cercare facilmente pokémon attraverso il pokédex. Per iniziare digita <code>/help</code>.",
        "HELP_MESSAGE_TEXT" : """
Per cercare un pokémon bisogna digitare <code>/pokemon</code> seguito dal nome o il numero di pokédex del pokémon che vuoi cercare.

Alcuni esempi:

<pre>/pokemon chimchar</pre>
<pre>/pokemon Darkrai</pre>
<pre>/pokemon 644</pre>

Prova tu stesso!
""",
        "LEGENDARY_POKEMON_MESSAGE" : "  [Leggendario]",
        "MYTHICAL_POKEMON_MESSAGE" : "  [Misterioso]",
        "TEXT_CHANGE_VARIETY_BUTTON" : "Cambia forma",
        "DESCRIPTION_NOT_AVAILABLE" : "<i>La descrizione non è disponibile in italiano.</i>\n",
        "ERROR":{
            "POKEMON_NOT_VALID": "Il pokémon <pokemon_name> non è presente all'interno del pokédex",
            "OPTION_ALREADY_CHOSEN" : "Hai già scelto il prossimo pokémon!"
        }
    }
}

def translate(message, language: str = 'IT', data: dict = {}):
    translation = TEXTS[language][message]
    for key in data:
        translation = translation.replace(f'<{key}>', data[key])
    return translation