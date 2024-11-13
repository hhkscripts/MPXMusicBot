import asyncio
import importlib
import sys

from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall

import config
from MPXMusic import HELPABLE, LOGGER, app, userbot
from MPXMusic.core.call import MPX
from MPXMusic.plugins import ALL_MODULES
from MPXMusic.utils.database import get_banned_users, get_gbanned
from config import BANNED_USERS


async def init():
    if sys.version_info < (3, 9):
        LOGGER("MPXMusic").error(
            "MPXMusic is optimized for Python 3.9 or higher. Exiting..."
        )
        sys.exit(1)

    if len(config.STRING_SESSIONS) == 0:
        LOGGER("MPXMusic").error(
            "No Assistant Clients Vars Defined!.. Exiting Process."
        )
        return
    if not config.SPOTIFY_CLIENT_ID and not config.SPOTIFY_CLIENT_SECRET:
        LOGGER("MPXMusic").warning(
            "No Spotify Vars defined. Your bot won't be able to play spotify queries."
        )
    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)
        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except Exception:
        pass
    await app.start()
    for all_module in ALL_MODULES:
        imported_module = importlib.import_module(all_module)

        if hasattr(imported_module, "__MODULE__") and imported_module.__MODULE__:
            if hasattr(imported_module, "__HELP__") and imported_module.__HELP__:
                HELPABLE[imported_module.__MODULE__.lower()] = imported_module
    LOGGER("MPXMusic.plugins").info("Successfully Imported All Modules ")
    await userbot.start()
    await MPX.start()
    LOGGER("MPXMusic").info("Assistant Started Sucessfully")
    try:
        await MPX.stream_call(
            "http://docs.evostream.com/sample_content/assets/sintel1m720p.mp4"
        )
    except NoActiveGroupCall:
        LOGGER("MPXMusic").error(
            "Please ensure the voice call in your log group is active."
        )
        sys.exit()

    await MPX.decorators()
    LOGGER("MPXMusic").info("MPXMusic Started Successfully")

    await idle()
    await app.stop()
    await userbot.stop()


if __name__ == "__main__":
    asyncio.get_event_loop_policy().get_event_loop().run_until_complete(init())
    LOGGER("MPXMusic").info("Stopping MPXMusic! GoodBye")
