import asyncio
import importlib
import logging

from TEAMZYRO import application, load_sudo_users, send_start_message, ZYRO
from TEAMZYRO.modules import ALL_MODULES

LOGGER = logging.getLogger

async def main():
    # Load Sudo Users
    await load_sudo_users()
    print("✅ Sudo users loaded.")

    # Import All Modules
    for module_name in ALL_MODULES:
        importlib.import_module("TEAMZYRO.modules." + module_name)
    LOGGER("TEAMZYRO.modules").info("𝐀𝐥𝐥 𝐅𝐞𝐚𝐭𝐮𝐫𝐞𝐬 𝐋𝐨𝐚𝐝𝐞𝐝 𝐁𝐚𝐛𝐲🥳...")

    # Start custom startup function if needed
    ZYRO.start()  # Only if ZYRO is a thread/process-based system
    send_start_message()

    print("✅ Bot is now running.")
    LOGGER("TEAMZYRO").info(
        "╔═════ஜ۩۞۩ஜ════╗\n  ☠︎︎MADE BY TEAMZYRO☠︎︎\n╚═════ஜ۩۞۩ஜ════╝"
    )

    # Start polling
    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    await application.updater.idle()

if __name__ == "__main__":
    asyncio.run(main())
