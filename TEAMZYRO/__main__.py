import asyncio
import importlib
import logging
from TEAMZYRO import *
from TEAMZYRO import application, LOGGER, send_start_message
from TEAMZYRO.modules import ALL_MODULES


async def main():
    print("✅ Bot is now running.")

    # Import all modules to register handlers
    for module_name in ALL_MODULES:
        importlib.import_module("TEAMZYRO.modules." + module_name)
    LOGGER("TEAMZYRO.modules").info("𝐀𝐥𝐥 𝐅𝐞𝐚𝐭𝐮𝐫𝐞𝐬 𝐋𝐨𝐚𝐝𝐞𝐝 𝐁𝐚𝐛𝐲🥳...")

    # Start the application
    await application.initialize()
    await application.start()
    await application.updater.start_polling()

    send_start_message()
    LOGGER("TEAMZYRO").info(
        "╔═════ஜ۩۞۩ஜ════╗\n  ☠︎︎MADE BY TEAMZYRO☠︎︎\n╚═════ஜ۩۞۩ஜ════╝"
    )

    await application.updater.idle()


if __name__ == "__main__":
    asyncio.run(main())
