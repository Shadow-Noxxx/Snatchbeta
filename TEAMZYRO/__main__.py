import importlib
import logging
import asyncio

from TEAMZYRO import application, ZYRO, LOGGER, send_start_message
from TEAMZYRO.modules import ALL_MODULES


async def main() -> None:
    # Load all bot modules
    for module_name in ALL_MODULES:
        importlib.import_module("TEAMZYRO.modules." + module_name)
    LOGGER("TEAMZYRO.modules").info("🎯 All features loaded successfully!")

    # Start the Pyrogram client (if you're using it alongside PTB)
    ZYRO.start()
    LOGGER("TEAMZYRO").info("✅ ZYRO client started.")

    # Initialize and start the application
    await application.initialize()
    await application.start()
    
    send_start_message()
    LOGGER("TEAMZYRO").info(
        "╔═════ஜ۩۞۩ஜ════╗\n  ☠︎︎ MADE BY TEAMZYRO ☠︎︎\n╚═════ஜ۩۞۩ஜ════╝"
    )
    print("✅ Bot is now running.")

    # Keep the bot running
    await application.updater.start_polling()
    await application.updater.idle()


if __name__ == "__main__":
    asyncio.run(main())
