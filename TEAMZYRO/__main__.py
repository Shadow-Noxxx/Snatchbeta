import asyncio
import importlib
import logging

from telegram.ext import ApplicationBuilder

  # Make sure BOT_TOKEN is imported from your config
from TEAMZYRO.modules import ALL_MODULES
from TEAMZYRO import LOGGER, send_start_message  # Adjust as per your structure

# Setup logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
BOT_TOKEN = "8053928530:AAFUnLykr0glC00IHD-_w8m-06y4oFSlCaI"
# Build application
application = ApplicationBuilder().token(BOT_TOKEN).build()

# Expose it for modules to use
import TEAMZYRO
TEAMZYRO.application = application


async def main():
    # Load modules dynamically and let them register their handlers
    for module_name in ALL_MODULES:
        importlib.import_module(f"TEAMZYRO.modules.{module_name}")
        print(f"✅ Loaded module: {module_name}")

    LOGGER("TEAMZYRO.modules").info("✅ All modules loaded successfully.")

    # Start the bot
    await application.initialize()
    await application.start()
    LOGGER("TEAMZYRO").info("🤖 Bot started successfully.")

    send_start_message()

    LOGGER("TEAMZYRO").info(
        "╔═════ஜ۩۞۩ஜ════╗\n  ☠︎︎ MADE BY TEAMZYRO ☠︎︎\n╚═════ஜ۩۞۩ஜ════╝"
    )

    # Run the bot until stopped
    await application.updater.start_polling()
    await application.updater.idle()


if __name__ == "__main__":
    asyncio.run(main())
