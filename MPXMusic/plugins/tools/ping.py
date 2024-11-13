from datetime import datetime

from pyrogram import filters, Client
from pyrogram.types import Message

from MPXMusic import app
from MPXMusic.core.call import MPX
from MPXMusic.utils import bot_sys_stats
from MPXMusic.utils.decorators.language import language
from MPXMusic.utils.inline import support_group_markup
from config import BANNED_USERS, PING_IMG_URL
from strings import get_command

PING_COMMAND = get_command("PING_COMMAND")


@app.on_message(filters.command(PING_COMMAND) & ~BANNED_USERS)
@language
async def ping_com(_client: Client, message: Message, _):
    response = await message.reply_photo(
        photo=PING_IMG_URL,
        caption=_["ping_1"].format(app.mention),
    )
    start = datetime.now()
    pytgping = await MPX.ping()
    UP, CPU, RAM, DISK = await bot_sys_stats()
    resp = (datetime.now() - start).microseconds / 1000
    await response.edit_text(
        _["ping_2"].format(
            resp,
            app.mention,
            UP,
            RAM,
            CPU,
            DISK,
            pytgping,
        ),
        reply_markup=support_group_markup(_),
    )
