import time
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from TEAMZYRO import application, sudo_users

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user.id not in sudo_users:
        await update.message.reply_text("❌ This command is only for Sudo users.")
        return
    start_time = time.time()
    message = await update.message.reply_text("🏓 Pong!")
    end_time = time.time()
    elapsed_time = round((end_time - start_time) * 1000, 3)
    await message.edit_text(f"🏓 Pong! `{elapsed_time} ms`", parse_mode="Markdown")

application.add_handler(CommandHandler("ping", ping))
