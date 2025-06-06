import importlib
import logging
import asyncio
from TEAMZYRO import *
from TEAMZYRO import application, ZYRO, LOGGER, send_start_message
from TEAMZYRO.modules import ALL_MODULES


async def main() -> None:
    # Load all bot modules
    for module_name in ALL_MODULES:
        importlib.import_module("TEAMZYRO.modules." + module_name)
    LOGGER("TEAMZYRO.modules").info("🎯 All features loaded successfully!")

    # Start the bot
    ZYRO.start()
    LOGGER("TEAMZYRO").info("✅ Bot client started.")

    # Run polling
    await application.start()
    send_start_message()
    LOGGER("TEAMZYRO").info(
        "╔═════ஜ۩۞۩ஜ════╗\n  ☠︎︎ MADE BY TEAMZYRO ☠︎︎\n╚═════ஜ۩۞۩ஜ════╝"
    )
    print("✅ Bot is now running.")
    
    # Keep bot running
    await application.updater.idle()


if __name__ == "__main__":
    asyncio.run(main())
