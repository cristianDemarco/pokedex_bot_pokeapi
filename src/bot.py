import logging
import sys
import os
import time
import json
from clients.pokemon_cards_API import PokemonCardsAPI
from data_models_mapper import map_API_data_to_pokemon

import telegram.error
from telegram import __version__ as TG_VER
from telegram import InlineKeyboardMarkup, Update
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from TOKEN import TOKEN
from clients.pokemon_API import PokemonAPI
from TEXTS import TEXTS
from src.send_pokemon_functions import (
    send_pokemon_message,
    create_keyboard,
    get_data_from_message,
    translate,
)
from src.send_card_functions import send_pokemon_card

# set higher logging level for httpx to avoid all GET and POST requests being logged
# logging.getLogger("httpx").setLevel(logging.DEBUG)
# logger = logging.getLogger(__name__)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

pokemonAPI = PokemonAPI()
POKEMON_COUNT = pokemonAPI.get_pokemon_count()

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        text=TEXTS["IT"]["START_MESSAGE_TEXT"].replace(
            "<username>", f"{user.mention_html()}"
        )
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_html(TEXTS["IT"]["HELP_MESSAGE_TEXT"])


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_pokemon(update, context, True)


async def send_pokemon(
    update: Update, context: ContextTypes.DEFAULT_TYPE, is_callback: bool = False
) -> None:
    start_timestamp = time.time()

    pokemon_name, chat_id, message_id, variety = get_data_from_message(
        update, is_callback, TEXTS["SEARCH_POKEMON_COMAND"]
    )

    try:
        data = pokemonAPI.get_api_data(pokemon_name, variety)
    except json.decoder.JSONDecodeError as e:
        await update.message.reply_text(
            text=TEXTS["IT"]["ERROR"]["POKEMON_NOT_VALID"].replace(
                "<pokemon_name>", f"{pokemon_name}"
            )
        )
        return

    pokemon = map_API_data_to_pokemon(data)

    reply_markup = InlineKeyboardMarkup(create_keyboard(pokemon, POKEMON_COUNT))

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


async def send_cards(
    update: Update, context: ContextTypes.DEFAULT_TYPE, is_callback: bool = False
) -> None:
    pokemon_name = get_data_from_message(
        update, is_callback, TEXTS["SEARCH_CARDS_COMAND"]
    )
    pokemon_cards_API = PokemonCardsAPI()
    message = translate(
        message="SEARCH_CARDS_TEXT", language="IT", data={"pokemon": f"{pokemon_name}"}
    )
    await update.message.reply_html(
        "".join([message, pokemon_cards_API.get_cards(pokemon_name)])
    )


async def send_card(
    update: Update, context: ContextTypes.DEFAULT_TYPE, is_callback: bool = False
) -> None:
    pokemon_name, chat_id, message_id, variety = get_data_from_message(
        update, is_callback, TEXTS["SEARCH_CARD_COMAND"]
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


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(
        CommandHandler(TEXTS["SEARCH_POKEMON_KEYWORD"], send_pokemon)
    )
    application.add_handler(CommandHandler(["cards"], send_cards))
    application.add_handler(CommandHandler(["card"], send_card))
    application.add_handler(CallbackQueryHandler(button_handler))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":

    # for pokemon_name in range(1,1250):
    #   pokemonAPI.get_api_data(pokemon_name, 0)

    main()
