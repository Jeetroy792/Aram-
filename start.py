# 𝖥𝗂𝗅𝖾: 𝗉𝗅𝗎𝗀𝗂𝗇𝗌/𝗌𝗍𝖺𝗋𝗍.𝗉𝗒
from pyrogram import Client, filters
from ui_style import EliteLook
from database import db

@Client.on_message(filters.command("start") & filters.private)
async def start_handler(client, message):
    await db.add_user(message.from_user.id)
    await message.reply_text(
        text=EliteLook.start_text(message.from_user.first_name),
        reply_markup=EliteLook.main_menu()
    )
  
