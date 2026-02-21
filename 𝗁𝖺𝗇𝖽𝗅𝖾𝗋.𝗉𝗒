# 𝖥𝗂𝗅𝖾: 𝗁𝖺𝗇𝖽𝗅𝖾𝗋.𝗉𝗒
# 𝖣𝖾𝗌𝗂𝗀𝗇𝖾𝖽 𝖿𝗈𝗋: 𝖬𝖺𝗌𝗍𝖾𝗋 𝖩𝖾𝖾𝗍 [𝖤𝗅𝗂𝗍𝖾 𝖤𝗇𝖼𝗈𝖽𝖾𝗋 𝖷𝟫]

import asyncio
from pyrogram import Client, filters
from pyrogram.types import CallbackQuery
from run import run_task
from ui_style import EliteLook
from database import db
from brain import brain

class MasterHandler:
    
    @Client.on_callback_query(filters.regex(r"^enc_"))
    async def encoding_handler(client, query: CallbackQuery):
        """
        জিৎ, ইউজার যখন কোয়ালিটি বাটন (480p, 720p) এ ক্লিক করবে, 
        তখন এই ফাংশনটি কাজ শুরু করবে।
        """
        user_id = query.from_user.id
        quality = query.data.split("_")[1] # 𝖾.𝗀., 𝟩𝟤𝟶𝗉
        
        # ১. ইউজার কি অলরেডি কোনো কাজ করছে? (Brain Sync)
        if user_id in brain.active_tasks:
            return await query.answer("⚠️ 𝖸𝗈𝗎 𝖺𝗅𝗋𝖾𝖺𝖽𝗒 𝗁𝖺𝗿𝖾 𝖺𝗇 𝖺𝖼𝗍𝗂𝗏𝖾 𝗍𝖺𝗌𝗄!", show_alert=True)
        
        # ২. ফাইলটি খুঁজে বের করা (Reply context থেকে)
        if not query.message.reply_to_message:
            return await query.message.edit("❌ **𝖲𝗈𝗎𝗋𝖼𝖾 𝖥𝗂𝗅𝖾 𝖭𝗈𝗍 𝖥𝗈𝗎𝗇𝖽!**")
            
        await query.message.delete()
        
        # ৩. রান ফাইলকে টাস্ক হ্যান্ডওভার করা
        asyncio.create_task(run_task(client, query.message.reply_to_message, quality))

    @Client.on_callback_query(filters.regex("settings"))
    async def settings_callback(client, query):
        """ইউজার সেটিংস দেখার বাটন লজিক"""
        user_data = await db.get_user(query.from_user.id)
        thumb_status = "✅ 𝖲𝖾𝗍" if user_data.get("thumb") else "❌ 𝖭𝗈𝗍 𝖲𝖾𝗍"
        wm_status = user_data.get("watermark", "❌ 𝖣𝗂𝗌𝖺𝖻𝗅𝖾𝖽")
        
        text = (
            "⚙️ **𝖸𝗈𝗎𝗋 𝖢𝗎𝗌𝗍𝗈𝗆 𝖲𝖾𝗍𝗍𝗂𝗇𝗀𝗌**\n\n"
            f"🖼 **𝖳𝗁𝗎𝗆𝖻𝗇𝖺𝗂𝗅:** `{thumb_status}`\n"
            f"🏷 **𝖶𝖺𝗍𝖾𝗋𝗆𝖺𝗋𝗄:** `{wm_status}`\n"
            f"💎 **𝖯𝗅𝖺𝗇:** `{'𝖯𝗋𝖾𝗆𝗂𝗎𝗆' if user_data.get('is_premium') else '𝖥𝗋𝖾𝖾'}`\n"
            "━━━━━━━━━━━━━━━━━━━━"
        )
        await query.message.edit_text(text, reply_markup=EliteLook.main_menu())

    @Client.on_callback_query(filters.regex("donate"))
    async def donate_callback(client, query):
        """ডোনেশন বাটন লজিক"""
        await query.message.edit_text(
            "🤴 **𝖲𝗎𝗉𝗉𝗈𝗋𝗍 𝖳𝗁𝖾 𝖣𝖾𝗏𝖾𝗅𝗈𝗉𝖾𝗋**\n\n"
            "𝖨𝖿 𝗒𝗈𝗎 𝗅𝗂𝗄𝖾 𝗆𝗒 𝗐𝗈𝗋𝗄, 𝗒𝗈𝗎 𝖼𝖺𝗇 𝖽𝗈𝗇𝖺𝗍𝖾 𝗍𝗈 𝗄𝖾𝖾𝗉 𝗍𝗁𝗂𝗌 𝗌𝖾𝗋𝗏𝖾𝗋 𝖺𝗅𝗂𝗏𝖾.\n\n"
            "💰 **𝖴𝖯𝖨:** `yourupi@bank`\n"
            "💳 **𝖯𝖺𝗒𝗉𝖺𝗅:** `paypal.me/yourid`",
            reply_markup=EliteLook.main_menu()
        )

    @Client.on_callback_query(filters.regex("close"))
    async def close_callback(client, query):
        """মেসেজ ডিলিট করার লজিক"""
        await query.message.delete()

