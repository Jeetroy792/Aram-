import os
import sys
import time
import asyncio
import logging
from flask import Flask
from threading import Thread
from pyrogram import Client, filters, idle
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import FloodWait

# 𝖨𝗆𝗉𝗈𝗋𝗍𝗂𝗇𝗀 𝖠𝗅𝗅 𝖲𝗒𝗇𝖼𝖾𝖽 𝖬𝗈𝖽𝗎𝗅𝖾𝗌
from config import Config
from database import db
from logic import MegaLogic
from worker import task_queue, process_tasks
from shortner import shortner_handler, ShortnerLogic
from premium_manager import PremiumManager
from ui_style import EliteLook 

# --- 𝖫𝖮𝖦𝖦𝖨𝖭𝖦 𝖲𝖤𝖳𝖴𝖯 ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- 𝖥𝖫𝖠𝖲𝖪 𝖲𝖤𝖱𝖵𝖤𝖱 𝖥𝖮𝖱 𝖪𝖮𝖸𝖤𝖡 𝟤𝟦/𝟩 ---
web = Flask(__name__)
@web.route('/')
def health_check(): 
    return "𝖤𝗅𝗂𝗍𝖾 𝖤𝗇𝗀𝗂𝗇𝖾 𝖷𝟫 𝗂𝗌 𝖠𝖼𝗍𝗂𝗏𝖾 🚀"

def run_web():
    web.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

# --- 𝖡𝖮𝖳 𝖨𝖭𝖨𝖳𝖨𝖠𝖫𝖨𝖹𝖠𝖳𝖨𝖮𝖭 ---
app = Client(
    "MegaEncoderBot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
    workers=100,
    plugins=dict(root="plugins")
)

# --- 𝖬𝖠𝖨𝖭 𝖢𝖮𝖬𝖬𝖠𝖭𝖣 𝖧𝖠𝖭𝖣𝖫𝖤𝖱𝖲 ---

@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    user_id = message.from_user.id
    if len(message.command) > 1 and message.command[1].startswith("verify"):
        return await ShortnerLogic.verify_user(client, message)
    
    await db.add_user(user_id)
    text = EliteLook.start_text(message.from_user.first_name)
    buttons = EliteLook.main_menu() 
    await message.reply_text(text, reply_markup=buttons)

@app.on_message(filters.command("help") & filters.private)
async def help_cmd(client, message):
    help_text = (
        "📖 **𝖤𝗅𝗂𝗍𝖾 𝖢𝗈𝗆𝗆𝖺𝗇𝖽 𝖢𝖾𝗇𝗍𝖾𝗋**\n\n"
        "🏷 **𝖳𝗁𝗎𝗆𝖻𝗇𝖺𝗂𝗅:** `/setthumb`, `/getthumb`, `/delthumb`\n"
        "📝 **𝖶𝖺𝗍𝖾𝗋𝗆𝖺𝗋𝒌:** `/setwatermark`, `/getwatermark`\n"
        "🛠 **𝖤𝖽𝗂𝗍𝗂𝗇𝗀:** `/cut`, `/crop`, `/merge`, `/compress`\n"
        "🎬 **𝖤𝗇𝖼𝗈𝖽𝖾:** `/144p` 𝗍𝗈 `/2160p`, `/all`\n"
        "🎼 **𝖠𝗎𝖽𝗂𝗈/𝖲𝗎𝖻:** `/extract_audio`, `/sub`, `/hsub`\n\n"
        "💎 **𝖠𝖽𝗆𝗂𝗇:** `/addpaid`, `/shortlink1`, `/preset`, `/update`"
    )
    await message.reply_text(help_text, reply_markup=EliteLook.main_menu())

# --- 𝖢𝖠𝖫𝖫𝖡𝖠𝖢𝖪 𝖰𝖴𝖤𝖱𝖸 𝖧𝖠𝖭𝖣𝖫𝖤𝖱 (𝖥𝗈𝗋 𝖡𝗎𝗍𝗍𝗈𝗇𝗌) ---

@app.on_callback_query()
async def callback_handlers(client, query: CallbackQuery):
    data = query.data
    if data == "start_data":
        await query.message.edit_text(EliteLook.start_text(query.from_user.first_name), reply_markup=EliteLook.main_menu())
    elif data == "help_data":
        await query.message.edit_text("📖 **𝖧𝖾𝗅𝗉 𝖬𝖾𝗇𝗎**\n𝖲𝖾𝗇𝖽 𝗆𝖾 𝖺𝗇𝗒 𝗏𝗂𝖽𝖾𝗈 𝗍𝗈 𝖼𝗈𝗆𝗉𝗋𝖾𝗌𝗌.", reply_markup=EliteLook.main_menu())
    elif "encode_" in data:
        quality = data.split("_")[1]
        await query.message.edit_text(f"🚀 **𝖤𝗇𝖼𝗈𝖽𝗂𝗇𝗀 𝗌𝖾𝗍 𝗍𝗈:** `{quality}`\n𝖠𝖽𝖽𝗂𝗇𝗀 𝗍𝗈 𝗍𝖺𝗌𝗄 𝗊𝗎𝖾𝗎𝖾...")
        # এখানে টাস্ক কিউতে যোগ করার লজিক

# --- 𝖬𝖤𝖣𝖨𝖠 𝖯𝖱𝖮𝖢𝖤𝖲𝖲𝖨𝖭𝖦 ---

@app.on_message((filters.video | filters.document) & filters.private)
async def handle_media(client, message):
    if not await shortner_handler(client, message):
        return
    
    # মিডিয়া এনালাইসিস এবং বাটন শো করা
    analysis = await MegaLogic.analyze_file(message)
    await message.reply_text(
        f"📥 **𝖥𝗂𝗅𝖾 𝖠𝗇𝖺𝗅𝗒𝗓𝖾𝖽!**\n\n"
        f"🎬 **𝖥𝗂𝗅𝖾:** `{analysis['name']}`\n"
        f"📦 **𝖲𝗂𝗓𝖾:** `{analysis['size']}`\n\n"
        "𝖢𝗁𝗈𝗈𝗌𝖾 𝗒𝗈𝗎𝗋 **𝖤𝗅𝗂𝗍𝖾 𝖰𝗎𝖺𝗅𝗂𝗍𝗒** 𝖻𝖾𝗅𝗈𝗐:",
        reply_markup=EliteLook.encoding_buttons()
    )

# --- 𝖠𝖣𝖬𝖨𝖭 𝖢𝖮𝖬𝖬𝖠𝖭𝖣𝖲 ---

@app.on_message(filters.command("stats") & filters.user(Config.ADMINS))
async def stats(client, message):
    users = await db.total_users_count()
    await message.reply_text(f"📊 **𝖡𝗈𝗍 𝖲𝗍𝖺𝗍𝗂𝗌𝗍𝗂𝖼𝗌:**\n\n👤 **𝖳𝗈𝗍𝖺𝗅 𝖴𝗌𝖾𝗋𝗌:** `{users}`")

@app.on_message(filters.command("restart") & filters.user(Config.ADMINS))
async def restart_bot(client, message):
    await message.reply_text("🔄 **𝖤𝗇𝗀𝗂𝗇𝖾 𝖱𝖾𝗌𝗍𝖺𝗋𝗍𝗂𝗇𝗀...**")
    os.execl(sys.executable, sys.executable, *sys.argv)

# --- 𝖤𝖷𝖤𝖢𝖴𝖳𝖨𝖮𝖭 𝖤𝖭𝖦𝖨𝖭𝖤 ---

async def start_services():
    for _ in range(getattr(Config, "MAX_CONCURRENT_TASKS", 2)):
        asyncio.create_task(process_tasks())
    
    await app.start()
    logger.info("🚀 𝖤𝗅𝗂𝗍𝖾 𝖤𝗇𝖼𝗈𝖽𝖾𝗋 𝖷𝟫 𝗂𝗌 𝖮𝗇𝗅𝗂𝗇𝖾!")
    await idle()
    await app.stop()

if __name__ == "__main__":
    Thread(target=run_web).start()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_services())

#---------------image-------------------------


@app.on_message(filters.photo & filters.user(Config.ADMINS))
async def get_file_id(client, message):
    # তুমি যখন বটকে কোনো ছবি পাঠাবে, সে ওই ছবির file_id দিয়ে দেবে
    await message.reply_text(f"**Your Image File ID:**\n`{message.photo.file_id}`")


