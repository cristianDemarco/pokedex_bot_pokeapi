import json

from models.pokemon import Pokemon
from models.pokemon_card import PokemonCard
from TEXTS import translate, TEXTS
from telegram.ext import ContextTypes
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update

async def send_pokemon_message(context: ContextTypes.DEFAULT_TYPE, pokemon: Pokemon, chat_id: int, message_id: int, reply_markup: InlineKeyboardMarkup, is_callback: bool):
    message = await context.bot.send_photo(
        chat_id=chat_id,
        caption=translate("POKEDEX_RETURN_MESSAGE", language="IT", data={
            "name": pokemon.name,
            "id": pokemon.id,
            "generation": pokemon.generation,
            "abilities": pokemon.abilities,
            "is_legendary": TEXTS["IT"]["LEGENDARY_POKEMON_MESSAGE"] if pokemon.is_legendary else "",
            "is_mythical": TEXTS["IT"]["MYTHICAL_POKEMON_MESSAGE"] if pokemon.is_mythical else "",
            "types": pokemon.types,
            "description": pokemon.description
        }),
        photo=pokemon.photo,
        reply_markup=reply_markup,
        reply_to_message_id=message_id if not is_callback else None,
        parse_mode="html"
    )

    return message

def create_keyboard(pokemon: Pokemon, POKEMON_COUNT: int) -> InlineKeyboardMarkup:
    keyboard = [[]]

    there_is_pokemon_before = int(pokemon.id) > 1

    if there_is_pokemon_before:
        keyboard.append(create_button(pokemon=pokemon,
                                         text=f"< N°{int(pokemon.id) - 1}",
                                         id_changer=-1))

    there_is_a_variety = pokemon.number_of_varieties > 1

    if there_is_a_variety:
        keyboard.append(create_button(pokemon=pokemon,
                                         text=TEXTS["IT"]["TEXT_CHANGE_VARIETY_BUTTON"],
                                         id_changer=0, variety_changer=1))

    there_is_pokemon_after = int(pokemon.id) < POKEMON_COUNT

    if there_is_pokemon_after:
        keyboard.append(create_button(pokemon=pokemon,
                                         text=f"N°{int(pokemon.id) + 1} >",
                                         id_changer=1))

    return [keyboard]

def create_button(pokemon: Pokemon, text: str, id_changer: int, variety_changer: int = 0) -> InlineKeyboardButton:
    button = InlineKeyboardButton(
        text=text,
        callback_data=json.dumps({
            "pokemon": f"{TEXTS['SEARCH_POKEMON_COMAND']} {int(pokemon.id) + id_changer}",
            "variety": f"{int(pokemon.variety) + variety_changer}"
        })
    )
    return button

def get_data_from_message(update: Update, is_callback: bool, comand: str):
    if not is_callback:
        pokemon_name = update.message.text
        chat_id = update.effective_chat.id
        message_id = update.message.message_id
        variety = 0
    else:
        query_data = json.loads(update.callback_query.data)
        pokemon_name = query_data["pokemon"]
        chat_id = update.callback_query.message.chat.id
        message_id = update.callback_query.message.message_id
        variety = int(query_data["variety"])

    pokemon_name = pokemon_name.strip().lower().replace(comand, "").strip()

    if comand == TEXTS['SEARCH_CARDS_COMAND']:
        return pokemon_name

    return pokemon_name, chat_id, message_id, variety
