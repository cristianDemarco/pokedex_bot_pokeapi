from telegram.ext import ContextTypes
from src.models.pokemon_card import PokemonCard
from telegram import InlineKeyboardMarkup
from TEXTS import translate


async def send_pokemon_card(
    context: ContextTypes.DEFAULT_TYPE,
    pokemon_card: PokemonCard,
    chat_id: int,
    message_id: int,
    reply_markup: InlineKeyboardMarkup,
    is_callback: bool,
):
    message = await context.bot.send_photo(
        chat_id=chat_id,
        caption=translate(
            "CARD_RETURN_MESSAGE",
            language="IT",
            data={
                "name": pokemon_card["name"],
                "set": pokemon_card["set"],
                "price": str(pokemon_card["price"]),
            },
        ),
        photo=pokemon_card["photo"],
        reply_markup=reply_markup,
        reply_to_message_id=message_id if not is_callback else None,
        parse_mode="html",
    )

    return message
