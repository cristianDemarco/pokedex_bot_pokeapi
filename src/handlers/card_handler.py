from clients.pokemon_cards_API import PokemonCardsAPI

from telegram import Update
from telegram.ext import ContextTypes

from TEXTS import TEXTS
from src.send_pokemon_functions import (
    get_data_from_message,
    translate,
)

from src.send_card_functions import send_pokemon_card


class CardHandler:
    def __init__(self) -> None:
        self.pokemon_cards_API = PokemonCardsAPI()

    async def send_cards(self, update: Update, is_callback: bool = False) -> None:
        pokemon_name = get_data_from_message(
            update=update, is_callback=is_callback, comand=TEXTS["SEARCH_CARDS_COMAND"]
        )
        message = translate(
            message="SEARCH_CARDS_TEXT",
            language="IT",
            data={"pokemon": f"{pokemon_name}"},
        )
        await update.message.reply_html(
            "".join([message, self.pokemon_cards_API.get_cards(pokemon_name)])
        )

    async def send_card(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        is_callback: bool = False,
    ) -> None:
        pokemon_name, chat_id, message_id, variety = get_data_from_message(
            update=update, is_callback=is_callback, comand=TEXTS["SEARCH_CARD_COMAND"]
        )
        pokemon_cards_API = PokemonCardsAPI()
        card = pokemon_cards_API.get_card(pokemon_name)
        await send_pokemon_card(
            context=context,
            pokemon_card=card,
            chat_id=chat_id,
            message_id=message_id,
            is_callback=is_callback,
            reply_markup=None,
        )
