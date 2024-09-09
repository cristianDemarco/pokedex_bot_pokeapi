import logging
import time
import json
from data_models_mapper import map_API_data_to_pokemon

import telegram.error
from telegram import InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from clients.pokemon_API import PokemonAPI
from TEXTS import TEXTS
from src.send_pokemon_functions import (
    send_pokemon_message,
    create_keyboard,
    get_data_from_message,
)


class PokemonHandler:
    def __init__(self) -> None:
        self.pokemon_API = PokemonAPI()
        self.POKEMON_COUNT = self.pokemon_API.get_pokemon_count()

    async def send_pokemon(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        is_callback: bool = False,
    ) -> None:
        start_timestamp = time.time()

        pokemon_name, chat_id, message_id, variety = get_data_from_message(
            update, is_callback, TEXTS["SEARCH_POKEMON_COMAND"]
        )

        try:
            data = self.pokemon_API.get_api_data(pokemon_name, variety)
        except json.decoder.JSONDecodeError as e:
            await update.message.reply_text(
                text=TEXTS["IT"]["ERROR"]["POKEMON_NOT_VALID"].replace(
                    "<pokemon_name>", f"{pokemon_name}"
                )
            )
            return

        pokemon = map_API_data_to_pokemon(data)

        reply_markup = InlineKeyboardMarkup(
            create_keyboard(pokemon, self.POKEMON_COUNT)
        )

        try:
            if is_callback:
                await context.bot.deleteMessage(
                    chat_id=chat_id, message_id=update.callback_query.message.message_id
                )
            await send_pokemon_message(
                context, pokemon, chat_id, message_id, reply_markup, is_callback
            )
        except telegram.error.BadRequest as e:
            logging.exception(e)
            await context.bot.answer_callback_query(
                callback_query_id=update.callback_query.id,
                text=TEXTS["IT"]["ERROR"]["OPTION_ALREADY_CHOSEN"],
            )

        end_timestamp = time.time()
        logging.info(f"Time occured: {end_timestamp - start_timestamp}")

    async def button_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await self.send_pokemon(update, context, True)
