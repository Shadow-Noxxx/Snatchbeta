import time
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from TEAMZYRO import application, sudo_users  # This will be the set, not collection

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    if user_id not in sudo_users:
        await update.message.reply_text("❌ This command is only for Sudo users.")
        return
    start = time.time()
    sent = await update.message.reply_text("🏓 Pong!")
    end = time.time()
    ms = round((end - start) * 1000, 3)
    await sent.edit_text(f"🏓 Pong! `{ms} ms`", parse_mode="Markdown")

application.add_handler(CommandHandler("ping", ping))
