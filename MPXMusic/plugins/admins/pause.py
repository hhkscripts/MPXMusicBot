from pyrogram import filters, Client
from pyrogram.types import Message

from MPXMusic import app
from MPXMusic.core.call import MPX
from MPXMusic.utils.database import is_music_playing, music_off
from MPXMusic.utils.decorators import admin_rights_check
from config import BANNED_USERS, PREFIXES
from strings import get_command

PAUSE_COMMAND = get_command("PAUSE_COMMAND")


@app.on_message(filters.command(PAUSE_COMMAND, PREFIXES) & filters.group & ~BANNED_USERS)
@admin_rights_check
async def pause_admin(_client: Client, message: Message, _, chat_id: int):
    if not len(message.command) == 1:
        return await message.reply_text(_["general_2"])
    if not await is_music_playing(chat_id):
        return await message.reply_text(_["admin_1"])
    await music_off(chat_id)
    await MPX.pause_stream(chat_id)
    await message.reply_text(_["admin_2"].format(message.from_user.mention))
