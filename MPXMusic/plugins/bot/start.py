import asyncio
import time
import random

from pyrogram import filters, Client
from pyrogram.enums import ChatType, ParseMode
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from youtubesearchpython.__future__ import VideosSearch

import config
from MPXMusic import HELPABLE, app, Platform
from MPXMusic.misc import SUDOERS, _boot_
from MPXMusic.plugins.play.playlist import del_plist_msg
from MPXMusic.plugins.sudo.sudoers import sudoers_list
from MPXMusic.utils.database import (
    add_served_chat,
    add_served_user,
    blacklisted_chats,
    get_assistant,
    get_lang,
    get_userss,
    is_on_off,
    is_served_private_chat,
)
from MPXMusic.utils.decorators.language import language_start
from MPXMusic.utils.formatters import get_readable_time
from MPXMusic.utils.functions import MARKDOWN, WELCOMEHELP
from MPXMusic.utils.inline import private_panel, start_pannel
from config import BANNED_USERS, START_IMG_URL
from config.config import OWNER_ID, PREFIXES
from strings import command, get_command, get_string
from .help import paginate_modules

loop = asyncio.get_running_loop()

START_COMMAND = get_command("START_COMMAND")

IMAGE = [
    "https://graph.org/file/f76fd86d1936d45a63c64.jpg",
    "https://graph.org/file/69ba894371860cd22d92e.jpg",
    "https://graph.org/file/67fde88d8c3aa8327d363.jpg",
    "https://graph.org/file/3a400f1f32fc381913061.jpg",
    "https://graph.org/file/a0893f3a1e6777f6de821.jpg",
    "https://graph.org/file/5a285fc0124657c7b7a0b.jpg",
    "https://graph.org/file/25e215c4602b241b66829.jpg",
    "https://graph.org/file/a13e9733afdad69720d67.jpg",
    "https://graph.org/file/692e89f8fe20554e7a139.jpg",
    "https://graph.org/file/db277a7810a3f65d92f22.jpg",
    "https://graph.org/file/a00f89c5aa75735896e0f.jpg",
    "https://graph.org/file/f86b71018196c5cfe7344.jpg",
    "https://graph.org/file/a3db9af88f25bb1b99325.jpg",
    "https://graph.org/file/5b344a55f3d5199b63fa5.jpg",
    "https://graph.org/file/84de4b440300297a8ecb3.jpg",
    "https://graph.org/file/84e84ff778b045879d24f.jpg",
    "https://graph.org/file/a4a8f0e5c0e6b18249ffc.jpg",
    "https://graph.org/file/ed92cada78099c9c3a4f7.jpg",
    "https://graph.org/file/d6360613d0fa7a9d2f90b.jpg",
    "https://graph.org/file/37248e7bdff70c662a702.jpg",
    "https://graph.org/file/0bfe29d15e918917d1305.jpg",
    "https://graph.org/file/16b1a2828cc507f8048bd.jpg",
    "https://graph.org/file/e6b01f23f2871e128dad8.jpg",
    "https://graph.org/file/cacbdddee77784d9ed2b7.jpg",
    "https://graph.org/file/ddc5d6ec1c33276507b19.jpg",
    "https://graph.org/file/39d7277189360d2c85b62.jpg",
    "https://graph.org/file/5846b9214eaf12c3ed100.jpg",
    "https://graph.org/file/ad4f9beb4d526e6615e18.jpg",
    "https://graph.org/file/3514efaabe774e4f181f2.jpg",  
    "https://graph.org/file/eaa3a2602e43844a488a5.jpg",
    "https://graph.org/file/b129e98b6e5c4db81c15f.jpg",
    "https://graph.org/file/3ccb86d7d62e8ee0a2e8b.jpg",
    "https://graph.org/file/df11d8257613418142063.jpg",
    "https://graph.org/file/9e23720fedc47259b6195.jpg",
    "https://graph.org/file/826485f2d7db6f09db8ed.jpg",
    "https://graph.org/file/ff3ad786da825b5205691.jpg",
    "https://graph.org/file/52713c9fe9253ae668f13.jpg",
    "https://graph.org/file/8f8516c86677a8c91bfb1.jpg",
    "https://graph.org/file/6603c3740378d3f7187da.jpg",
    "https://graph.org/file/66cb6ec40eea5c4670118.jpg",
    "https://graph.org/file/2e3cf4327b169b981055e.jpg",   
]

@app.on_message(filters.command(START_COMMAND, PREFIXES) & filters.private & ~BANNED_USERS)
@language_start
async def start_comm(client: Client, message: Message, _):
    chat_id = message.chat.id
    await add_served_user(message.from_user.id)
    if len(message.text.split()) > 1:
        name = message.text.split(None, 1)[1]
        if name[0:4] == "help":
            keyboard = InlineKeyboardMarkup(paginate_modules(0, HELPABLE, close=True))
            if config.START_IMG_URL:
                return await message.reply_photo(
                    random.choice(IMAGE),
                    caption=_["help_1"],
                    reply_markup=keyboard,
                )
            else:
                return await message.reply_text(
                    text=_["help_1"],
                    reply_markup=keyboard,
                )
        if name[0:4] == "song":
            await message.reply_text(_["song_2"])
            return
        if name == "mkdwn_help":
            await message.reply(
                MARKDOWN,
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True,
            )
        if name == "greetings":
            await message.reply(
                WELCOMEHELP,
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True,
            )
        if name[0:3] == "sta":
            m = await message.reply_text("🔎 Buscando suas estatísticas pessoais!")
            stats = await get_userss(message.from_user.id)
            tot = len(stats)
            if not stats:
                await asyncio.sleep(1)
                return await m.edit(_["ustats_1"])

            def get_stats():
                msg = ""
                limit = 0
                results = {}
                for i in stats:
                    top_list = stats[i]["spot"]
                    results[str(i)] = top_list
                    list_arranged = dict(
                        sorted(
                            results.items(),
                            key=lambda item: item[1],
                            reverse=True,
                        )
                    )
                if not results:
                    return m.edit(_["ustats_1"])
                tota = 0
                videoid = None
                for vidid, count in list_arranged.items():
                    tota += count
                    if limit == 10:
                        continue
                    if limit == 0:
                        videoid = vidid
                    limit += 1
                    details = stats.get(vidid)
                    title = (details["title"][:35]).title()
                    if vidid == "telegram":
                        msg += f"🔗[Arquivos e áudios do Telegram]({config.SUPPORT_GROUP}) ** tocados {count} vezes**\n\n"
                    else:
                        msg += f"🔗 [{title}](https://www.youtube.com/watch?v={vidid}) ** tocados {count} vezes**\n\n"
                msg = _["ustats_2"].format(tot, tota, limit) + msg
                return videoid, msg

            try:
                videoid, msg = await loop.run_in_executor(None, get_stats)
            except Exception as e:
                print(e)
                return
            thumbnail = await Platform.youtube.thumbnail(videoid, True)
            await m.delete()
            await message.reply_photo(photo=thumbnail, caption=msg)
            return
        if name[0:3] == "sud":
            await sudoers_list(client=client, message=message, _=_)
            await asyncio.sleep(1)
            if await is_on_off(config.LOG):
                sender_id = message.from_user.id
                sender_mention = message.from_user.mention
                sender_name = message.from_user.first_name
                return await app.send_message(
                    config.LOG_GROUP_ID,
                    f"👤 {message.from_user.mention} acabou de iniciar o bot para verificar a <code>lista de Sudo</code>\n\n🆔 **ID do usuário:** {sender_id}\n📛 **Nome do usuário:** {sender_name}",
                )
            return
        if name[0:3] == "lyr":
            query = (str(name)).replace("lyrics_", "", 1)
            lyrical = config.lyrical
            lyrics = lyrical.get(query)
            if lyrics:
                await Platform.telegram.send_split_text(message, lyrics)
                return
            else:
                await message.reply_text("Falha ao obter as letras da música.")
                return
        if name[0:3] == "del":
            await del_plist_msg(client=client, message=message, _=_)
            await asyncio.sleep(1)
        if name[0:3] == "inf":
            m = await message.reply_text("🔎 Buscando informações!")
            query = (str(name)).replace("info_", "", 1)
            query = f"https://www.youtube.com/watch?v={query}"
            results = VideosSearch(query, limit=1)
            for result in (await results.next())["result"]:
                title = result["title"]
                duration = result["duration"]
                views = result["viewCount"]["short"]
                thumbnail = result["thumbnails"][0]["url"].split("?")[0]
                channellink = result["channel"]["link"]
                channel = result["channel"]["name"]
                link = result["link"]
                published = result["publishedTime"]
                searched_text = f"""
🔍__**Informações da Faixa de Vídeo**__

❇️**Título:** {title}

⏳**Duração:** {duration} Minutos
👀**Visualizações:** `{views}`
⏰**Publicado em:** {published}
🎥**Nome do Canal:** {channel}
📎**Link do Canal:** [Visite aqui]({channellink})
🔗**Link do Vídeo:** [Clique aqui]({link})
"""

            key = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="🎥 Assistir", url=f"{link}"),
                        InlineKeyboardButton(text="🔄 Fechar", callback_data="close"),
                    ],
                ]
            )
            await m.delete()
            await app.send_photo(
                message.chat.id,
                photo=thumbnail,
                caption=searched_text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=key,
            )
            await asyncio.sleep(1)
            if await is_on_off(config.LOG):
                sender_id = message.from_user.id
                sender_name = message.from_user.first_name
                return await app.send_message(
                    config.LOG_GROUP_ID,
                    f"👤 {message.from_user.mention} acabou de iniciar o bot para verificar as <code> informações do vídeo </code>\n\n🆔 **ID do usuário:** {sender_id}\n📛 **Nome do usuário:** {sender_name}",
                )
    else:
        try:
            await app.resolve_peer(OWNER_ID[0])
            OWNER = OWNER_ID[0]
        except:
            OWNER = None
        out = private_panel(_, app.username, OWNER)
        if config.START_IMG_URL:
            try:
                await message.reply_photo(
                    random.choice(IMAGE),
                    caption=_["start_1"].format(app.mention),
                    reply_markup=InlineKeyboardMarkup(out),
                )
            except:
                await message.reply_text(
                    text=_["start_1"].format(app.mention),
                    reply_markup=InlineKeyboardMarkup(out),
                )
        else:
            await message.reply_text(
                text=_["start_1"].format(app.mention),
                reply_markup=InlineKeyboardMarkup(out),
            )
        if await is_on_off(config.LOG):
            sender_id = message.from_user.id
            sender_name = message.from_user.first_name
            return await app.send_message(
                config.LOG_GROUP_ID,
                f"👤 {message.from_user.mention} iniciou o bot. \n\n🆔 **ID do usuário:** {sender_id}\n📛 **Nome do usuário:** {sender_name}",
            )


@app.on_message(filters.command(START_COMMAND, PREFIXES) & filters.group & ~BANNED_USERS)
@language_start
async def testbot(_client: Client, message: Message, _):
    uptime = int(time.time() - _boot_)
    chat_id = message.chat.id
    await message.reply_text(_["start_7"].format(get_readable_time(uptime)))

    return await add_served_chat(message.chat.id)


@app.on_message(filters.new_chat_members, group=-1)
async def welcome(_client: Client, message: Message):
    chat_id = message.chat.id
    if config.PRIVATE_BOT_MODE == str(True):
        if not await is_served_private_chat(message.chat.id):
            await message.reply_text(
                "**O modo privado deste bot foi ativado, apenas meu dono pode usá-lo. Se você quiser usar este bot no seu chat, peça ao meu dono para autorizar seu chat.**"
            )
            return await app.leave_chat(message.chat.id)
    else:
        await add_served_chat(chat_id)
    for member in message.new_chat_members:
        try:
            language = await get_lang(message.chat.id)
            _ = get_string(language)
            if member.id == app.id:
                chat_type = message.chat.type
                if chat_type != ChatType.SUPERGROUP:
                    await message.reply_text(_["start_5"])
                    return await app.leave_chat(message.chat.id)
                if chat_id in await blacklisted_chats():
                    await message.reply_text(
                        _["start_6"].format(
                            f"https://t.me/{app.username}?start=sudolist"
                        )
                    )
                    return await app.leave_chat(chat_id)
                userbot = await get_assistant(message.chat.id)
                out = start_pannel(_)
                await message.reply_text(
                    _["start_2"].format(
                        app.mention,
                        userbot.username,
                        userbot.id,
                    ),
                    reply_markup=InlineKeyboardMarkup(out),
                )
            if member.id in config.OWNER_ID:
                return await message.reply_text(
                    _["start_3"].format(app.mention, member.mention)
                )
            if member.id in SUDOERS:
                return await message.reply_text(
                    _["start_4"].format(app.mention, member.mention)
                )
            return
        except:

            return


__MODULE__ = "Bot"
__HELP__ = f"""
<b>✦ c significa reprodução em canal.</b>

<b>★ {command("STATS_COMMAND")}</b> - Obtenha as Estatísticas Globais das 10 faixas mais tocadas, 10 principais usuários do bot, 10 principais chats no bot, 10 mais tocadas em um chat, etc.

<b>★ {command("SUDOUSERS_COMMAND")}</b> - Verifique os usuários Sudo do bot.

<b>★ {command("LYRICS_COMMAND")} [Nome da Música]</b> - Pesquise letras para uma música específica na web.

<b>★ {command("SONG_COMMAND")} [Nome da Faixa] ou [Link do YT]</b> - Baixe qualquer faixa do YouTube nos formatos MP3 ou MP4.

<b>★ {command("QUEUE_COMMAND")}</b> - Verifique a lista de músicas na fila.

    <u><b>⚡️Bot Privado:</b></u>

<b>✧ {command("AUTHORIZE_COMMAND")} [ID_DO_CHAT]</b> - Permitir que um chat use o seu bot.

<b>✧ {command("UNAUTHORIZE_COMMAND")} [ID_DO_CHAT]</b> - Bloquear um chat de usar o seu bot.

<b>✧ {command("AUTHORIZED_COMMAND")}</b> - Verificar todos os chats permitidos do seu bot.
"""
