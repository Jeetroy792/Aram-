# 𝖥𝗂𝗅𝖾: 𝖼𝗈𝗆𝗆𝖺𝗇𝖽𝗌.𝗉𝗒
# 𝖣𝖾𝗌𝗂𝗀𝗇𝖾𝖽 𝖿𝗈𝗋: 𝖬𝖺𝗌𝗍𝖾𝗋 𝖩𝖾𝖾𝗍 [𝖤𝗅𝗂𝗍𝖾 𝖤𝗇𝖼𝗈𝖽𝖾𝗋 𝖷𝟫]

import os
import time
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import db
from config import Config
from ui_style import EliteLook

class CommandHandler:
    
    @Client.on_message(filters.command("setthumb") & filters.private)
    async def set_thumbnail(client, message):
        """জিৎ, এটি ইউজারের কাস্টম থাম্বনেইল সেভ করার কমান্ড"""
        if not message.reply_to_message or not message.reply_to_message.photo:
            return await message.reply_text("❌ **𝖯𝗅𝖾𝖺𝗌𝖾 𝗋𝖾𝗉𝗅𝗒 𝗍𝗈 𝖺 𝗉𝗁𝗈𝗍𝗈 𝗍𝗈 𝗌𝖾𝗍 𝗂𝗍 𝖺𝗌 𝗍𝗁𝗎𝗆𝖻𝗇𝖺𝗂𝗅.**")
        
        status = await message.reply_text("📥 **𝖲𝖺𝗏𝗂𝗇𝗀 𝖳𝗁𝗎𝗆𝖻𝗇𝖺𝗂𝗅...**")
        photo_id = message.reply_to_message.photo.file_id
        await db.set_thumb(message.from_user.id, photo_id)
        await status.edit("✅ **𝖢𝗎𝗌𝗍𝗈𝗆 𝖳𝗁𝗎𝗆𝖻𝗇𝖺𝗂𝗅 𝖲𝖺𝗏𝖾𝖽 𝖲𝗎𝖼𝖼𝖾𝗌𝗌𝖿𝗎𝗅𝗅𝗒!**")

    @Client.on_message(filters.command("delthumb") & filters.private)
    async def delete_thumbnail(client, message):
        """থাম্বনেইল রিমুভ করার কমান্ড"""
        await db.set_thumb(message.from_user.id, None)
        await message.reply_text("🗑️ **𝖢𝗎𝗌𝗍𝗈𝗆 𝖳𝗁𝗎𝗆𝖻𝗇𝖺𝗂𝗅 𝖱𝖾𝗆𝗈𝗏𝖾𝖽!**")

    @Client.on_message(filters.command("setwatermark") & filters.private)
    async def set_wm(client, message):
        """ওয়াটারমার্ক সেট করার লজিক"""
        if len(message.command) < 2:
            return await message.reply_text("📑 **𝖴𝗌𝖺𝗀𝖾:** `/setwatermark 𝖸𝗈𝗎𝗋𝖳𝖾𝗑𝗍`")
        
        wm_text = message.text.split(None, 1)[1]
        await db.set_watermark(message.from_user.id, wm_text)
        await message.reply_text(f"✅ **𝖶𝖺𝗍𝖾𝗋mark 𝖲𝖾𝗍 𝗍𝗈:** `{wm_text}`")

    @Client.on_message(filters.command("stats") & filters.user(Config.ADMINS))
    async def get_stats(client, message):
        """অ্যাডমিনের জন্য বটের স্ট্যাটাস কমান্ড"""
        users_count = await db.total_users_count()
        total_tasks = await db.get_total_encoded_count()
        uptime = time.time() - client.start_time
        
        stats_text = (
            "📊 **𝖤𝗅𝗂𝗍𝖾 𝖤𝗇𝖼𝗈𝖽𝖾𝗋 𝖲𝗍𝖺𝗍𝗌**\n\n"
            f"👤 **𝖳𝗈𝗍𝖺𝗅 𝖴𝗌𝖾𝗋𝗌:** `{users_count}`\n"
            f"🎬 **𝖥𝗂𝗅𝖾𝗌 𝖤𝗇𝖼𝗈𝖽𝖾𝖽:** `{total_tasks}`\n"
            f"⏳ **𝖴𝗉𝗍𝗂𝗆𝖾:** `{int(uptime/3600)}𝗁 {int((uptime%3600)/60)}𝗆`"
        )
        await message.reply_text(stats_text)

    @Client.on_message(filters.command("broadcast") & filters.user(Config.ADMINS))
    async def broadcast_msg(client, message):
        """ইউজারদের কাছে মেসেজ পাঠানোর কমান্ড"""
        if not message.reply_to_message:
            return await message.reply_text("❌ **𝖱𝖾𝗉𝗅𝗒 𝗍𝗈 𝖺 𝗆𝖾𝗌𝗌𝖺𝗀𝖾 𝗍𝗈 𝖻𝗋𝗈𝖺𝖽𝖼𝖺𝗌𝗍.**")
        
        all_users = await db.get_all_users()
        success = 0
        failed = 0
        
        msg = await message.reply_text("📢 **𝖡𝗋𝗈𝖺𝖽𝖼𝖺𝗌𝗍𝗂𝗇𝗀 𝗂𝗇 𝖯𝗋𝗈𝗀𝗋𝖾𝗌𝗌...**")
        
        for user in all_users:
            try:
                await message.reply_to_message.forward(user['id'])
                success += 1
            except:
                failed += 1
        
        await msg.edit(f"✅ **𝖡𝗋𝗈𝖺𝖽𝖼𝖺𝗌𝗍 𝖢𝗈𝗆𝗉𝗅𝖾𝗍𝖾!**\n\n🎯 **𝖲𝗎𝖼𝖼𝖾𝗌𝗌:** `{success}`\n⚠️ **𝖥𝖺𝗂𝗅𝖾𝖽:** `{failed}`")

    @Client.on_message(filters.command("about") & filters.private)
    async def about_handler(client, message):
        """বট সম্পর্কে তথ্য"""
        about_text = (
            "🤖 **𝖠𝖻𝗈𝗎𝗍 𝖤𝗅𝗂𝗍𝖾 𝖤𝗇𝖼𝗈𝖽𝖾𝗋 𝖷𝟫**\n\n"
            "✨ **𝖮𝗐𝗇𝖾𝗋:** [𝖬𝖺𝗌𝗍𝖾𝗋 𝖩𝖾𝖾𝗍](𝗍.𝗆𝖾/𝗒𝗈𝗎𝗋_𝗎𝗌𝖾𝗋𝗇𝖺𝗆𝖾)\n"
            "🚀 **𝖤𝗇𝗀𝗂𝗇𝖾:** `𝖥𝖥𝗆𝗉𝖾𝗀 𝖷-𝖲𝖾𝗋𝗂𝖾𝗌`\n"
            "📜 **𝖫𝖺𝗇𝗀𝗎𝖺𝗀𝖾:** `𝖯𝗒𝗍𝗁𝗈𝗇 𝟥.𝟣𝟢`\n"
            "💎 **𝖲𝗍𝖺𝗍𝗎𝗌:** `𝖯𝗋𝖾𝗆𝗂𝗎𝗆 𝖤𝖽𝗂𝗍𝗂𝗈𝗇`"
        )
        await message.reply_text(about_text, reply_markup=EliteLook.main_menu())

