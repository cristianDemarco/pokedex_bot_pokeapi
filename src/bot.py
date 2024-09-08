import logging
import sys
import os

from telegram import __version__ as TG_VER
from telegram import Update
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from TOKEN import TOKEN
from TEXTS import TEXTS
from handlers.card_handler import CardHandler
from handlers.pokemon_handler import PokemonHandler

# set higher logging level for httpx to avoid all GET and POST requests being logged
# logging.getLogger("httpx").setLevel(logging.DEBUG)
# logger = logging.getLogger(__name__)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

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


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    card_handler = CardHandler()
    pokemon_handler = PokemonHandler()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(
        CommandHandler(TEXTS["SEARCH_POKEMON_KEYWORD"], pokemon_handler.send_pokemon)
    )
    application.add_handler(CommandHandler(["cards"], card_handler.send_card))
    application.add_handler(CommandHandler(["card"], card_handler.send_card))
    application.add_handler(CallbackQueryHandler(pokemon_handler.button_handler))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":

    # for pokemon_name in range(1,1250):
    #   pokemonAPI.get_api_data(pokemon_name, 0)

    main()
