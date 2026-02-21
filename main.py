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
from ui_style import EliteLook # 𝖸𝗈𝗎𝗋 𝖫𝖺𝗋𝗀𝖾 𝖡𝗎𝗍𝗍𝗈𝗇 𝖲𝗍𝗒𝗅𝖾

# --- 𝖫𝖮𝖦𝖦𝖨𝖭𝖦 𝖲𝖤𝖳𝖴𝖯 ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- 𝖥𝖫𝖠𝖲𝖪 𝖲𝖤𝖱𝖵𝖤𝖱 𝖥𝖮𝖱 𝖪𝖮𝖸𝖤𝖡 𝟤𝟦/𝟩 ---
web = Flask(__name__)
@web.route('/')
def health_check(): return "𝖤𝗅𝗂𝗍𝖾 𝖤𝗇𝖼𝗈𝖽𝖾𝗋 𝖤𝗇𝗀𝗂𝗇𝖾 𝖷𝟫 𝗂𝗌 𝖠𝖼𝗍𝗂𝗏𝖾 🚀"

def run_web():
    web.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

# --- 𝖡𝖮𝖳 𝖨𝖭𝖨𝖳𝖨𝖠𝖫_𝖨𝖹𝖠𝖳𝖨𝖮𝖭 ---
app = Client(
    "MegaEncoderBot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
    workers=100,
    plugins=dict(root="plugins")
)

# --- 𝖬𝖠𝖨𝖭 𝖢𝖮𝖬𝖬𝖠𝖭𝖣 𝖧𝖠𝖭𝖣𝖫𝖤𝖱𝖲 (𝖯𝖺𝗂 𝗍𝗈 𝖯𝖺𝗂 𝖲𝗒𝗇𝖼) ---

@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    user_id = message.from_user.id
    # 𝖣𝖾𝖾𝗉 𝖫𝗂𝗇𝗄 𝖵𝖾𝗋𝗂𝖿𝗂𝖼𝖺𝗍𝗂𝗈𝗇 (𝖲𝗁𝗈𝗋𝗍𝗅𝗂𝗇𝗄 𝖲𝗒𝗇𝖼)
    if len(message.command) > 1 and message.command[1].startswith("verify"):
        return await ShortnerLogic.verify_user(client, message)
    
    await db.add_user(user_id)
    text = EliteLook.start_text(message.from_user.first_name)
    buttons = EliteLook.main_menu() # 𝖫𝖺𝗋𝗀𝖾 𝖢𝗈𝗅𝗈𝗋𝖿𝗎𝗅 𝖡𝗎𝗍𝗍𝗈𝗇𝗌 𝗅𝗂𝗄𝖾 𝖭𝗂𝖼𝗄 𝖡𝗒𝗉𝖺𝗌𝗌
    await message.reply_text(text, reply_markup=buttons)

@app.on_message(filters.command("help") & filters.private)
async def help_cmd(client, message):
    help_text = (
        "📖 **𝖤𝗅𝗂𝗍𝖾 𝖢𝗈𝗆𝗆𝖺𝗇𝖽 𝖢𝖾𝗇𝗍𝖾𝗋**\n\n"
        "🏷 **𝖳𝗁𝗎𝗆𝖻𝗇𝖺𝗂𝗅:** `/setthumb`, `/getthumb`, `/delthumb`\n"
        "📝 **𝖶𝖺𝗍𝖾𝗋𝗆𝖺𝗋𝗄:** `/setwatermark`, `/getwatermark`\n"
        "🛠 **𝖤𝖽𝗂𝗍𝗂𝗇𝗀:** `/cut`, `/crop`, `/merge`, `/compress`\n"
        "🎬 **𝖤𝗇𝖼𝗈𝖽𝖾:** `/144p` 𝗍𝗈 `/2160p`, `/all`\n"
        "🎼 **𝖠𝗎𝖽𝗂𝗈/𝖲𝗎𝖻:** `/extract_audio`, `/sub`, `/hsub`\n\n"
        "💎 **𝖠𝖽𝗆𝗂𝗇:** `/addpaid`, `/shortlink1`, `/preset`, `/update`"
    )
    await message.reply_text(help_text, reply_markup=EliteLook.main_menu())

# --- 𝖬𝖤𝖣𝖨𝖠 𝖯𝖱𝖮𝖢𝖤𝖲𝖲𝖨𝖭𝖦 (𝖳𝗁𝖾 𝖢𝗈𝗋𝖾 𝖲𝗒𝗇𝖼) ---

@app.on_message((filters.video | filters.document) & filters.private)
async def handle_media(client, message):
    user_id = message.from_user.id
    
    # 𝖲𝗒𝗇𝖼 𝖢𝗁𝖾𝖼𝗄 𝟣: 𝖥𝗈𝗋𝖼𝖾 𝖲𝗎𝖻𝗌𝖼𝗋𝗂𝖻𝖾
    # 𝖲𝗒𝗇𝖼 𝖢𝗁𝖾𝖼𝗄 𝟤: 𝖲𝗁𝗈𝗋𝗍𝗅𝗂𝗇𝗄/𝖳𝗈𝗄𝖾𝗇
    if not await shortner_handler(client, message):
        return

    # 𝖲𝗒𝗇𝖼 𝖢𝗁𝖾𝖼𝗄 𝟥: 𝖬𝖾𝖽𝗂𝖺 𝖠𝗇𝖺𝗅𝗒𝗌𝗂𝗌 𝗏𝗂𝖺 𝖫𝗈𝗀𝗂𝖼.𝗉𝗒
    await message.reply_text(
        "📥 **𝖥𝗂𝗅𝖾 𝖠𝗇𝖺𝗅𝗒𝗯𝖾𝖽!**\n𝖢𝗁𝗈𝗈𝗌𝖾 𝗒𝗈𝗎𝗋 **𝖤𝗅𝗂𝗍𝖾 𝖰𝗎𝖺𝗅𝗂𝗍𝗒** 𝖻𝖾𝗅𝗈𝗐:",
        reply_markup=EliteLook.encoding_buttons()
    )

# --- 𝖠𝖣𝖬𝖨𝖭 𝖢𝖮𝖬𝖬𝖠𝖭𝖣𝖲 (𝖯𝗋𝗈𝖿𝖾𝗌𝗌𝗂𝗈𝗇𝖺𝗅 𝖢𝗈𝗇𝗍𝗋𝗈𝗅) ---

@app.on_message(filters.command("restart") & filters.user(Config.ADMINS))
async def restart_bot(client, message):
    await message.reply_text("🔄 **𝖤𝗇𝗀𝗂𝗇𝖾 𝖱𝖾𝗌𝗍𝖺𝗋𝗍𝗂𝗇𝗀...**")
    os.execl(sys.executable, sys.executable, *sys.argv)

@app.on_message(filters.command("addpaid") & filters.user(Config.ADMINS))
async def add_premium_user(client, message):
    if len(message.command) < 3:
        return await message.reply_text("📑 **𝖴𝗌𝖺𝗀𝖾:** `/addpaid user_id days`")
    user_id = int(message.command[1])
    days = int(message.command[2])
    expiry = await PremiumManager.add_premium(user_id, days)
    await message.reply_text(f"💎 **𝖴𝗌𝖾𝗋 {user_id} 𝗎𝗉𝗀𝗋𝖺𝖽𝖾𝖽 𝗎𝗇𝗍𝗂𝗅 {expiry}!**")

# --- 𝖤𝖷𝖤𝖢𝖴𝖳𝖨𝖮𝖭 𝖤𝖭𝖦𝖨𝖭𝖤 ---

async def start_services():
    # 𝖲𝗍𝖺𝗋𝗍 𝖶𝗈𝗋𝗄𝖾𝗋 𝖫𝗈𝗈𝗉𝗌 𝖿𝗈𝗋 𝖯𝖺𝗋𝖺𝗅𝗅𝖾𝗅 𝖤𝗇𝖼𝗈𝖽𝗂𝗇𝗀
    for _ in range(Config.MAX_CONCURRENT_TASKS):
        asyncio.create_task(process_tasks())
    
    await app.start()
    logger.info("🚀 𝖤𝗅𝗂𝗍𝖾 𝖤𝗇𝖼𝗈𝖽𝖾𝗋 𝖷𝟫 𝗂𝗌 𝖮𝗇𝗅𝗂𝗇𝖾!")
    await idle()
    await app.stop()

if __name__ == "__main__":
    # 𝖲𝗍𝖺𝗋𝗍 𝖥𝗅𝖺𝗌𝗄 𝗂𝗇 𝖡𝖺𝖼𝗄𝗀𝗋𝗈𝗎𝗇𝖽
    Thread(target=run_web).start()
    # 𝖱𝗎𝗇 𝖠𝗌𝗒𝗇𝖼𝗂𝗈 𝖤𝗏𝖾𝗇𝗍 𝖫𝗈𝗈𝗉
    asyncio.get_event_loop().run_until_complete(start_services())
