import sys
import os
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.Pokemon import Pokemon
from TEXTS import translate, TEXTS
from telegram.ext import ContextTypes
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update

async def send_message(context : ContextTypes.DEFAULT_TYPE, pokemon : Pokemon, chat_id : int, message_id : int, reply_markup : InlineKeyboardMarkup, is_callback : bool):
    message = await context.bot.send_photo(
        chat_id = chat_id,
        caption = translate("POKEDEX_RETURN_MESSAGE", language="IT", data={
            "name": pokemon.name,
            "id" : pokemon.id,
            "generation" : pokemon.generation,
            "abilities" : pokemon.abilities,
            "is_legendary" : TEXTS["IT"]["LEGENDARY_POKEMON_MESSAGE"] if pokemon.is_legendary else "",
            "is_mythical" : TEXTS["IT"]["MYTHICAL_POKEMON_MESSAGE"] if pokemon.is_mythical else "",
            "types" : pokemon.types,
            "description" : pokemon.description
        }),
        photo = pokemon.photo,
        reply_markup=reply_markup,
        reply_to_message_id= message_id if not is_callback else None,
        parse_mode="html"
    )

    return message

def create_keyboard(pokemon, POKEMON_COUNT) -> InlineKeyboardMarkup:
    keyboard = [[]]

    if int(pokemon.id) > 1:
        keyboard[0].append(create_button(pokemon=pokemon,
                                        text = f"< N°{int(pokemon.id) - 1}",
                                        id_changer=-1))

    if pokemon.number_of_varieties > 1:
        keyboard[0].append(create_button(pokemon=pokemon,
                                        text = TEXTS["IT"]["TEXT_CHANGE_VARIETY_BUTTON"],
                                        id_changer=0, variety_changer=1))
    if int(pokemon.id) < POKEMON_COUNT:
        keyboard[0].append(create_button(pokemon=pokemon,
                                        text = f"N°{int(pokemon.id) + 1} >",
                                        id_changer=1))

    return keyboard

def create_button(pokemon, text, id_changer, variety_changer = 0):
    button = InlineKeyboardButton(text = text, callback_data=json.dumps(            
                    {
                        "pokemon" : f"{TEXTS['SEARCH_POKEMON_COMAND']} {int(pokemon.id) + id_changer}",
                        "variety" : f"{int(pokemon.variety) + variety_changer}"
                    }
                )
            )
    
    return button


def get_data_from_message(update : Update, is_callback : bool):
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

    pokemon_name = pokemon_name.replace(TEXTS['SEARCH_POKEMON_COMAND'], "").strip().lower()

    return pokemon_name, chat_id, message_id, variety
