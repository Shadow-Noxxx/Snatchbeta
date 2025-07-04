import time
from pyrogram import Client, filters
from pyrogram.types import Message

# Only allow sudo users to use /ping
SUDO_USERS = 7819315360 , 6138142369  # Replace with your actual SUDO user IDs

@Client.on_message(filters.command("ping") & filters.user(SUDO_USERS))
async def ping_command(client: Client, message: Message):
    start_time = time.time()
    reply = await message.reply_text("🏓 Pong...")
    end_time = time.time()
    latency = round((end_time - start_time) * 1000, 3)
    await reply.edit_text(f"🏓 Pong! `{latency}ms`")
