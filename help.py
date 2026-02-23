# 𝖥𝗂𝗅𝖾: 𝗁𝖾𝗅𝗉.𝗉𝗒
# 𝖣𝖾𝗌𝗂𝗀𝗇𝖾𝖽 𝖿𝗈𝗋: 𝖬𝖺𝗌𝗍𝖾𝗋 𝖩𝖾𝖾𝗍 [𝖤𝗅𝗂𝗍𝖾 𝖤𝗇𝖼𝗈𝖽𝖾ר 𝖷𝟫]

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from ui_style import EliteLook

class EliteHelp:
    
    @staticmethod
    def main_help_text():
        return (
            "📖 **𝖤𝗅𝗂𝗍𝖾 𝖤𝗇𝖼𝗈𝖽𝖾𝗋 𝖧𝖾𝗅𝗉 𝖢𝖾𝗇𝗍𝖾𝗋**\n\n"
            "𝖶𝖾𝗅𝖼𝗈𝗆𝖾 𝗍𝗈 𝗍𝗁𝖾 𝗆𝗈𝗌𝗍 𝖺𝖽𝗏𝖺𝗇𝖼𝖾𝖽 𝗏𝗂𝖽𝖾𝗈 𝗉𝗋𝗈𝖼𝖾𝗌𝗌𝗂𝗇𝗀 𝖼𝖾𝗇𝗍𝖾𝗋.\n"
            "𝖲𝖾𝗅𝖾𝖼𝗍 𝖺 𝖼𝖺𝗍𝖾𝗀𝗈𝗋𝗒 𝖻𝖾𝗅𝗈𝗐 𝗍𝗈 𝗌𝖾𝖾 𝗍𝗁𝖾 𝖺𝗏𝖺𝗂𝗅𝖺𝖻𝗅𝖾 𝖼𝗈𝗆𝗆𝖺𝗇𝖽𝗌:\n"
            "━━━━━━━━━━━━━━━━━━━━"
        )

    @staticmethod
    def help_buttons():
        return InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🎬 𝖤𝗇𝖼𝗈𝖽𝗂𝗇𝗀", callback_data="help_encode"),
                InlineKeyboardButton("🛠 𝖤𝖽𝗂𝗍𝗂𝗇𝗀", callback_data="help_edit")
            ],
            [
                InlineKeyboardButton("🖼 𝖳𝗁𝗎𝗆𝖻𝗇𝖺𝗂𝗅", callback_data="help_thumb"),
                InlineKeyboardButton("🏷 𝖬𝖾𝗍𝖺𝖽𝖺𝗍𝖺", callback_data="help_meta")
            ],
            [
                InlineKeyboardButton("💎 𝖯𝗋𝖾𝗆𝗂𝗎𝗆", callback_data="help_premium"),
                InlineKeyboardButton("👤 𝖠𝖽𝗆𝗂𝗇", callback_data="help_admin")
            ],
            [
                InlineKeyboardButton("🔙 𝖡𝖺𝖼𝗄 𝗍𝗈 𝖬𝖾𝗇𝗎", callback_data="start_back")
            ]
        ])

# --- 𝖧𝖠𝖭𝖣𝖫𝖤𝖱𝖲 ---

@Client.on_message(filters.command("help") & filters.private)
async def help_handler(client, message):
    text = EliteHelp.main_help_text()
    buttons = EliteHelp.help_buttons()
    await message.reply_text(text, reply_markup=buttons)

@Client.on_callback_query(filters.regex(r"^help_"))
async def help_callback(client, query):
    data = query.data.split("_")[1]
    
    help_data = {
        "encode": "🎬 **𝖤𝗇𝖼𝗈𝖽𝗂𝗇𝗀 𝖧𝖾𝗅𝗉**\n\n𝖲𝖾𝗇𝖽 𝖺𝗇𝗒 𝗏𝗂𝖽𝖾𝗈 𝖺𝗇𝖽 𝖼𝗁𝗈𝗈𝗌𝖾:\n• `/144p` 𝗍𝗈 `/2160p` (𝟦𝖪)\n• `/all` - 𝖠𝗅𝗅 𝗊𝗎𝖺𝗅𝗂𝗍𝗂𝖾𝗌 𝗈𝗇𝖾 𝖻𝗒 𝗈𝗇𝖾.",
        "edit": "🛠 **𝖤𝖽𝗂𝗍𝗂𝗇𝗀 𝖧𝖾𝗅𝗉**\n\n• `/cut` - 𝖳𝗋𝗂𝗆 𝗏𝗂𝖽𝖾𝗈 (𝖧𝖧:𝖬𝖬:𝖲𝖲)\n• `/merge` - 𝖢𝗈𝗆𝖻𝗂𝗇𝖾 𝗏𝗂𝖽𝖾𝗈𝗌\n• `/crop` - 𝖠𝗌𝗉𝖾𝖼𝗍 𝗋𝖺𝗍𝗂𝗈",
        "thumb": "🖼 **𝖳𝗁𝗎𝗆𝖻𝗇𝖺𝗂𝗅 𝖧𝖾𝗅𝗉**\n\n• `/setthumb` - 𝖱𝖾𝗉𝗅𝗒 𝗍𝗈 𝖺 𝗉𝗁𝗈𝗍𝗈\n• `/getthumb` - 𝖲𝗁𝗈𝗐 𝖼𝗎𝗋𝗋𝖾𝗇𝗍 𝗍𝗁𝗎𝗆𝖻\n• `/delthumb` - 𝖱𝖾𝗆𝗈𝗏𝖾 𝗍𝗁𝗎𝗆𝖻",
        "meta": "🏷 **𝖬𝖾𝗍𝖺𝖽𝖺𝗍𝖺 𝖧𝖾𝗅𝗉**\n\n• `/metadata` - 𝖲𝖾𝗍 𝖼𝗎𝗌𝗍𝗈𝗆 𝗍𝗂𝗍𝗅𝖾/𝖺𝗎𝗍𝗁𝗈𝗋\n• `/extract_audio` - 𝖬𝖯𝟥 𝖤𝗑𝗍𝗋𝖺𝖼𝗍𝗈𝗋",
        "premium": "💎 **𝖯𝗋𝖾𝗆𝗂𝗎𝗆 𝖧𝖾𝗅𝗉**\n\n• 𝖭𝗈 𝖠𝖽𝗌 / 𝖭𝗈 𝖳𝗈𝗄𝖾𝗇\n• 𝟧𝖷 𝖥𝖺𝗌𝗍𝖾𝗋 𝖤𝗇𝖼𝗈𝖽𝗂𝗇𝗀\n• 𝖴𝗅𝗍𝗋𝖺 𝖯𝗋𝗂𝗈𝗋𝗂𝗍𝗒 𝖰𝗎𝖾𝗎𝖾",
        "admin": "👤 **𝖠𝖽𝗆𝗂𝗇 𝖢𝗈𝗇𝗍𝗋𝗈𝗅**\n\n• `/addpaid` - 𝖠𝖽𝖽 𝗉𝗋𝖾𝗆𝗂𝗎𝗆 𝗎𝗌𝖾𝗋\n• `/restart` - 𝖱𝖾𝖻𝗈𝗈𝗍 𝖾𝗇𝗀𝗂𝗇𝖾\n• `/stats` - 𝖡𝗈𝗍 𝗌𝗍𝖺𝗍𝗂𝗌𝗍𝗂𝗀𝗌"
    }
    
    await query.message.edit_text(
        text=help_data.get(data, "𝖨𝗇𝗏𝖺𝗅𝗂𝖽 𝖧𝖾𝗅𝗉 𝖢𝖺𝗍𝖾𝗀𝗈𝗋𝗒"),
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 𝖡𝖺𝖼𝗄", callback_data="help_main")]])
    )

@Client.on_callback_query(filters.regex("help_main"))
async def help_main_callback(client, query):
    await query.message.edit_text(
        text=EliteHelp.main_help_text(),
        reply_markup=EliteHelp.help_buttons()
    )
  
