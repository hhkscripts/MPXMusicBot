import re
from math import ceil
from typing import Union

from pyrogram import filters, types, Client
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    CallbackQuery,
)

from MPXMusic import HELPABLE, app
from MPXMusic.utils.database import get_lang, is_commanddelete_on
from MPXMusic.utils.decorators.language import language_start
from MPXMusic.utils.inline.help import private_help_panel
from config import BANNED_USERS, START_IMG_URL, PREFIXES
from strings import get_command, get_string

HELP_COMMAND = get_command("HELP_COMMAND")

COLUMN_SIZE = 4  # number of  button height
NUM_COLUMNS = 3  # number of button width

AVISHA = [
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

class EqInlineKeyboardButton(InlineKeyboardButton):
    def __eq__(self, other: InlineKeyboardButton):
        return self.text == other.text

    def __lt__(self, other: InlineKeyboardButton):
        return self.text < other.text

    def __gt__(self, other: InlineKeyboardButton):
        return self.text > other.text


def paginate_modules(page_n, module_dict, chat=None, close: bool = False):
    if chat:
        modules = sorted(
            [
                EqInlineKeyboardButton(
                    x.__MODULE__,
                    callback_data="help_module({},{},{},{})".format(
                        chat, x.__MODULE__.lower(), page_n, int(close)
                    ),
                )
                for x in module_dict.values()
            ]
        )
    else:
        modules = sorted(
            [
                EqInlineKeyboardButton(
                    x.__MODULE__,
                    callback_data="help_module({},{},{})".format(
                        x.__MODULE__.lower(), page_n, int(close)
                    ),
                )
                for x in module_dict.values()
            ]
        )

    pairs = [modules[i: i + NUM_COLUMNS] for i in range(0, len(modules), NUM_COLUMNS)]
    max_num_pages = ceil(len(pairs) / COLUMN_SIZE) if len(pairs) > 0 else 1
    modulo_page = page_n % max_num_pages

    navigation_buttons = [
        EqInlineKeyboardButton(
            "❮",
            callback_data="help_prev({},{})".format(
                modulo_page - 1 if modulo_page > 0 else max_num_pages - 1,
                int(close),
            ),
        ),
        EqInlineKeyboardButton(
            "close" if close else "Bᴀᴄᴋ",
            callback_data="close" if close else "settingsback_helper",
        ),
        EqInlineKeyboardButton(
            "❯",
            callback_data="help_next({},{})".format(modulo_page + 1, int(close)),
        ),
    ]

    if len(pairs) > COLUMN_SIZE:
        pairs = pairs[modulo_page * COLUMN_SIZE: COLUMN_SIZE * (modulo_page + 1)] + [
            navigation_buttons
        ]
    else:
        pairs.append(
            [
                EqInlineKeyboardButton(
                    "close" if close else "Bᴀᴄᴋ",
                    callback_data="close" if close else "settingsback_helper",
                )
            ]
        )

    return pairs


@app.on_message(filters.command(HELP_COMMAND, PREFIXES) & filters.private & ~BANNED_USERS)
@app.on_callback_query(filters.regex("settings_back_helper") & ~BANNED_USERS)
async def helper_private(
        _client: Client, update: Union[types.Message, types.CallbackQuery]
):
    is_callback = isinstance(update, types.CallbackQuery)
    if is_callback:
        try:
            await update.answer()
        except:
            pass
        chat_id = update.message.chat.id
        language = await get_lang(chat_id)
        _ = get_string(language)
        keyboard = InlineKeyboardMarkup(paginate_modules(0, HELPABLE, "help"))
        await update.edit_message_text(_["help_1"], reply_markup=keyboard)
    else:
        chat_id = update.chat.id
        if await is_commanddelete_on(update.chat.id):
            try:
                await update.delete()
            except:
                pass
        language = await get_lang(chat_id)
        _ = get_string(language)
        keyboard = InlineKeyboardMarkup(
            paginate_modules(0, HELPABLE, "help", close=True)
        )
        if START_IMG_URL:
            await update.reply_photo(
                random.choice(AVISHA),
                caption=_["help_1"],
                reply_markup=keyboard,
            )

        else:
            await update.reply_text(
                text=_["help_1"],
                reply_markup=keyboard,
            )


@app.on_message(filters.command(HELP_COMMAND) & filters.group & ~BANNED_USERS)
@language_start
async def help_com_group(client, message: Message, _):
    keyboard = private_help_panel(_)
    await message.reply_text(_["help_2"], reply_markup=InlineKeyboardMarkup(keyboard))


async def help_parser(name, keyboard=None):
    if not keyboard:
        keyboard = InlineKeyboardMarkup(paginate_modules(0, HELPABLE, "help"))
    return keyboard


@app.on_callback_query(filters.regex(r"help_(.*?)"))
async def help_button(client: Client, query: CallbackQuery):
    chat_match = re.match(r"help_module\((.+?),(.+?),(.+?),(\d+)\)", query.data)
    mod_match = re.match(r"help_module\((.+?),(.+?),(\d+)\)", query.data)
    prev_match = re.match(r"help_prev\((.+?),(\d+)\)", query.data)
    next_match = re.match(r"help_next\((.+?),(\d+)\)", query.data)
    back_match = re.match(r"help_back\((\d+),(\d+)\)", query.data)

    try:
        language = await get_lang(query.message.chat.id)
        _ = get_string(language)
    except:
        _ = get_string("en")

    top_text = _["help_1"]

    if chat_match:
        chat_id = chat_match.group(1)
        module = chat_match.group(2)
        prev_page_num = int(chat_match.group(3))
        close = int(chat_match.group(4)) == 1
        text = (
                f"<b><u>Aqui está a ajuda para {HELPABLE[module].__MODULE__}:</u></b>\n"
                + HELPABLE[module].__HELP__
        )
        key = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Bᴀᴄᴋ",
                        callback_data=f"help_back({prev_page_num},{int(close)})",
                    ),
                    InlineKeyboardButton(text="Cʟᴏsᴇ", callback_data="close"),
                ],
            ]
        )
        await query.message.edit(
            text=text,
            reply_markup=key,
            disable_web_page_preview=True,
        )

    elif mod_match:
        module = mod_match.group(1)
        prev_page_num = int(mod_match.group(2))
        close = int(mod_match.group(3)) == 1
        text = (
                f"<b><u>Aqui está a ajuda para {HELPABLE[module].__MODULE__}:</u></b>\n"
                + HELPABLE[module].__HELP__
        )
        key = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Bᴀᴄᴋ",
                        callback_data=f"help_back({prev_page_num},{int(close)})",
                    ),
                    InlineKeyboardButton(text="Cʟᴏsᴇ", callback_data="close"),
                ],
            ]
        )
        await query.message.edit(
            text=text,
            reply_markup=key,
            disable_web_page_preview=True,
        )

    elif prev_match:
        curr_page = int(prev_match.group(1))
        close = int(prev_match.group(2)) == 1
        await query.message.edit(
            text=top_text,
            reply_markup=InlineKeyboardMarkup(
                paginate_modules(curr_page, HELPABLE, close=close)
            ),
            disable_web_page_preview=True,
        )

    elif next_match:
        next_page = int(next_match.group(1))
        close = int(next_match.group(2)) == 1
        await query.message.edit(
            text=top_text,
            reply_markup=InlineKeyboardMarkup(
                paginate_modules(next_page, HELPABLE, close=close)
            ),
            disable_web_page_preview=True,
        )

    elif back_match:
        prev_page_num = int(back_match.group(1))
        close = int(back_match.group(2)) == 1
        await query.message.edit(
            text=top_text,
            reply_markup=InlineKeyboardMarkup(
                paginate_modules(prev_page_num, HELPABLE, close=close)
            ),
            disable_web_page_preview=True,
        )

    await client.answer_callback_query(query.id)
