from telegram import Update
from telegram.ext import ContextTypes
from TEXTS import TEXTS


class BotHandler:
    async def start(update: Update) -> None:
        """Send a message when the command /start is issued."""
        user = update.effective_user
        await update.message.reply_html(
            text=TEXTS["IT"]["START_MESSAGE_TEXT"].replace(
                "<username>", f"{user.mention_html()}"
            )
        )

    async def help_command(update: Update) -> None:
        """Send a message when the command /help is issued."""
        await update.message.reply_html(TEXTS["IT"]["HELP_MESSAGE_TEXT"])
