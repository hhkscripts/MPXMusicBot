import asyncio

import uvloop

uvloop.install()

import sys

from pyrogram import Client
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import (
    ChatSendPhotosForbidden,
    ChatWriteForbidden,
    FloodWait,
    MessageIdInvalid,
)
from pyrogram.types import (
    BotCommand,
    BotCommandScopeAllChatAdministrators,
    BotCommandScopeAllGroupChats,
    BotCommandScopeAllPrivateChats,
)

import config

from ..logging import LOGGER


class MPXBot(Client):
    def __init__(self: "MPXBot"):

        self.username = None
        self.id = None
        self.name = None
        self.mention = None

        LOGGER(__name__).info(f"Starting Bot")
        super().__init__(
            "MPXMusic",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            in_memory=True,
        )

    async def edit_message_text(self, *args, **kwargs):
        try:
            return await super().edit_message_text(*args, **kwargs)
        except FloodWait as e:
            time = int(e.value)
            await asyncio.sleep(time)
            if time < 25:
                return await self.edit_message_text(self, *args, **kwargs)
        except MessageIdInvalid:
            pass

    async def send_message(self, *args, **kwargs):
        if kwargs.get("send_direct", False):
            kwargs.pop("send_direct", None)
            return await super().send_message(*args, **kwargs)

        try:
            return await super().send_message(*args, **kwargs)
        except FloodWait as e:
            time = int(e.value)
            await asyncio.sleep(time)
            if time < 25:
                return await self.send_message(self, *args, **kwargs)
        except ChatWriteForbidden:
            chat_id = kwargs.get("chat_id") or args[0]
            if chat_id:
                await self.leave_chat(chat_id)

    async def send_photo(self, *args, **kwargs):
        try:
            return await super().send_photo(*args, **kwargs)
        except FloodWait as e:
            time = int(e.value)
            await asyncio.sleep(time)
            if time < 25:
                return await self.send_photo(self, *args, **kwargs)
        except ChatSendPhotosForbidden:
            chat_id = kwargs.get("chat_id") or args[0]
            if chat_id:
                await self.send_message(
                    chat_id,
                    "I ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴛʜᴇ ʀɪɢʜᴛ ᴛᴏ sᴇɴᴅ ᴘʜᴏᴛᴏs ɪɴ ᴛʜɪs ᴄʜᴀᴛ, ʟᴇᴀᴠɪɴɢ ɴᴏᴡ..",
                )
                await self.leave_chat(chat_id)

    async def start(self):
        await super().start()
        get_me = await self.get_me()

        self.username = get_me.username
        self.id = get_me.id
        self.name = self.me.first_name + " " + (self.me.last_name or "")
        self.mention = self.me.mention

        try:
            await self.send_message(
                config.LOG_GROUP_ID,
                text=f"🚀 <b>{self.mention} ʙᴏᴛ sᴛᴀʀᴛᴇᴅ:</b>\n\n🆔 <b>ɪᴅ</b>: <code>{self.id}</code>\n📛 <b>ɴᴀᴍᴇ</b>: {self.name}\n🔗 <b>ᴜsᴇʀɴᴀᴍᴇ:</b> @{self.username}",
            )
        except:
            LOGGER(__name__).error(
                "Bᴏᴛ ʜᴀs ғᴀɪʟᴇᴅ ᴛᴏ ᴀᴄᴄᴇss ᴛʜᴇ ʟᴏɢ ɢʀᴏᴜᴘ. Mᴀᴋᴇ sᴜʀᴇ ᴛʜᴀᴛ ʏᴏᴜ ʜᴀᴠᴇ ᴀᴅᴅᴇᴅ ʏᴏᴜʀ ʙᴏᴛ ᴛᴏ ʏᴏᴜʀ ʟᴏɢ ᴄʜᴀɴɴᴇʟ ᴀɴᴅ ᴘʀᴏᴍᴏᴛᴇᴅ ᴀs ᴀᴅᴍɪɴ!"
            )
            LOGGER(__name__).error("An error occurred", exc_info=True)
            # sys.exit()
        if config.SET_CMDS == str(True):
            try:
                await self.set_bot_commands(
                    commands=[
                        BotCommand("start", "Iniciar o bot"),
                        BotCommand("help", "Abrir o menu de ajuda"),
                        BotCommand("ping", "Cʜᴇᴄᴋ ɪғ ᴛʜᴇ ʙᴏᴛ ɪs ᴀᴄᴛɪᴠᴇ ᴏʀ ɪɴᴀᴄᴛɪᴠᴇ"),
                    ],
                    scope=BotCommandScopeAllPrivateChats(),
                )
                await self.set_bot_commands(
                    commands=[
                        BotCommand("play", "Iniciar a reprodução da música solicitada"),
                    ],
                    scope=BotCommandScopeAllGroupChats(),
                )
                await self.set_bot_commands(
                    commands=[
                        BotCommand("play", "Iniciar a reprodução da música solicitada"),
                        BotCommand("skip", "Pular para a próxima faixa na fila"),
                        BotCommand("pause", "Pausar a música atual"),
                        BotCommand("resume", "Retomar a música pausada"),
                        BotCommand("end", "Limpar a fila e sair do chat de voz"),
                        BotCommand(
                            "shuffle", "Embaralhar aleatoriamente a playlist na fila."
                        ),
                        BotCommand(
                            "playmode",
                            "Permite alterar o modo de reprodução padrão para o seu chat",
                        ),
                        BotCommand(
                            "settings",
                            "Abrir as configurações do bot de música para o seu chat.",
                        ),
                    ],
                    scope=BotCommandScopeAllChatAdministrators(),
                )
            except:
                pass
        else:
            pass
        try:
            a = await self.get_chat_member(config.LOG_GROUP_ID, self.id)
            if a.status != ChatMemberStatus.ADMINISTRATOR:
                LOGGER(__name__).error("Please promote bot as admin in logger group")
                sys.exit()
        except Exception:
            pass
        if get_me.last_name:
            self.name = get_me.first_name + " " + get_me.last_name
        else:
            self.name = get_me.first_name
        LOGGER(__name__).info(f"MusicBot started as {self.name}")

    async def stop(self):
        LOGGER(__name__).info("Bot is shutting down")
        await self.send_message(
            config.LOG_GROUP_ID,
            text=f"🛑 <b>{self.mention} ʙᴏᴛ sᴛᴀʀᴛᴇᴅ:</b>\n\n🆔 <b>ɪᴅ</b>: <code>{self.id}</code>\n📛 <b>ɴᴀᴍᴇ</b>: {self.name}\n🔗 <b>ᴜsᴇʀɴᴀᴍᴇ:</b> @{self.username}",
        )
        await super().stop()
