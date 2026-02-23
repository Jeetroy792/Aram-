# 𝖥𝗂𝗅𝖾: 𝗉𝗋𝖾𝗆𝗂𝗎𝗆.𝗉𝗒
# 𝖣𝖾𝗌𝗂𝗀𝗇𝖾𝖽 𝖿𝗈𝗋: 𝖬𝖺𝗌𝗍𝖾𝗋 𝖩𝖾𝖾𝗍 [𝖤𝗅𝗂𝗍𝖾 𝖤𝗇𝖼𝗈𝖽𝖾𝗋 𝖷𝟫]

import time
import datetime
from pyrogram import Client, filters
from database import db
from config import Config

class PremiumManager:
    @staticmethod
    async def check_premium_validity(user_id):
        """ইউজারের প্রিমিয়াম পিরিয়ড শেষ হয়েছে কিনা তা চেক করার লজিক"""
        user_data = await db.get_user(user_id)
        if not user_data or not user_data.get("is_premium"):
            return False
        
        expiry_timestamp = user_data.get("expiry_date")
        if expiry_timestamp and time.time() > expiry_timestamp:
            # টাইম শেষ, তাই প্রিমিয়াম স্ট্যাটাস কেড়ে নেওয়া হচ্ছে
            await db.col.update_one(
                {'id': int(user_id)}, 
                {'$set': {'is_premium': False, 'expiry_date': None}}
            )
            return False
        return True

    @staticmethod
    def get_remaining_time(expiry_timestamp):
        """প্রিমিয়াম শেষ হতে কত দিন বা ঘণ্টা বাকি আছে তা বের করা"""
        if not expiry_timestamp:
            return "𝖭/𝖠"
        remaining = expiry_timestamp - time.time()
        if remaining <= 0:
            return "𝖤𝗑𝗉𝗂𝗋𝖾𝖽"
        
        days, remainder = divmod(int(remaining), 86400)
        hours, remainder = divmod(remainder, 3600)
        return f"{days}𝖽 {hours}𝗁 𝗋𝖾𝗆𝖺𝗂𝗇𝗂𝗇𝗀"

# --- 𝖠𝖣𝖬𝖨𝖭 𝖢𝖮𝖬𝖬𝖠𝖭𝖣𝖲 ---

@Client.on_message(filters.command("addpremium") & filters.user(Config.ADMINS))
async def add_premium_user(client, message):
    """জিৎ, এই কমান্ড দিয়ে তুমি কাউকে প্রিমিয়াম মেম্বার বানাতে পারবে"""
    if len(message.command) < 3:
        return await message.reply_text("📑 **𝖴𝗌𝖺𝗀𝖾:** `/addpremium [𝗎𝗌𝖾𝗋_𝗂𝖽] [𝖽𝖺𝗒𝗌]`")
    
    user_id = int(message.command[1])
    days = int(message.command[2])
    
    expiry = await db.make_premium(user_id, days)
    readable_date = datetime.datetime.fromtimestamp(expiry).strftime('%Y-%m-%d')
    
    await message.reply_text(
        f"💎 **𝖯𝗋𝖾𝗆𝗂𝗎𝗆 𝖠𝖽𝖽𝖾𝖽 𝖲𝗎𝼼𝖼𝖾𝗌𝗌𝖿𝗎𝗅𝗅𝗒!**\n\n"
        f"👤 **𝖴𝗌𝖾𝗋:** `{user_id}`\n"
        f"⏳ **𝖣𝗎𝗋𝖺𝗍𝗂𝗈𝗇:** `{days} 𝖣𝖺𝗒𝗌`\n"
        f"📅 **𝖤𝗑𝗉𝗂𝗋𝗒:** `{readable_date}`"
    )
    
    # ইউজারকে নোটিফিকেশন পাঠানো
    try:
        await client.send_message(
            user_id,
            f"🎉 **𝖢𝗈𝗇𝗀𝗋𝖺𝗍𝗎𝗅𝖺𝗍𝗂𝗈𝗇𝗌!**\n\n"
            f"𝖸𝗈𝗎𝗋 **𝖤𝗅𝗂𝗍𝖾 𝖯𝗋𝖾𝗆𝗂𝗎𝗆** 𝗉𝗅𝖺𝗇 𝗁𝖺𝗌 𝖻𝖾𝖾𝗇 𝖺𝖼𝗍𝗂𝗏𝖺𝗍𝖾𝖽 𝖿𝗈𝗋 **{days} 𝖽𝖺𝗒𝗌**.\n"
            f"𝖤𝗇𝗀𝗈𝗒 𝖠𝖽-𝖿𝗋𝖾𝖾, 𝖥𝖺𝗌𝗍 𝖤𝗇𝖼𝗈𝖽𝗂𝗇𝗀!"
        )
    except:
        pass

@Client.on_message(filters.command("myplan") & filters.private)
async def check_my_plan(client, message):
    """ইউজার নিজের প্ল্যান চেক করার কমান্ড"""
    user_data = await db.get_user(message.from_user.id)
    if not user_data or not user_data.get("is_premium"):
        return await message.reply_text("🆓 **𝖸𝗈𝗎 𝖺𝗋𝖾 𝖼𝗎𝗋𝗋𝖾𝗇𝗍𝗅𝗒 𝗎𝗌𝗂𝗇𝗀 𝗍𝗁𝖾 𝖥𝗋𝖾𝖾 𝖯𝗅𝖺𝗇.**\n𝖴𝗉𝗀𝗋𝖺𝖽𝖾 𝗍𝗈 𝖯𝗋𝖾𝗆𝗂𝗎𝗆 𝖿𝗈𝗋 𝖻𝖾𝗍𝗍𝖾𝗋 𝗌𝗉𝖾𝖾𝖽!")
    
    remaining = PremiumManager.get_remaining_time(user_data.get("expiry_date"))
    await message.reply_text(
        f"💎 **𝖸𝗈𝗎𝗋 𝖯𝗋𝖾𝗆𝗂𝗎𝗆 𝖲𝗍𝖺𝗍𝗎𝗌**\n\n"
        f"🌟 **𝖯𝗅𝖺𝗇:** `𝖤𝗅𝗂𝗍𝖾 𝖵𝖨𝖯`\n"
        f"⏳ **𝖳𝗂𝗆𝖾 𝖫𝖾𝖿𝗍:** `{remaining}`\n"
        f"🚀 **𝖲𝗉𝖾𝖾𝖽:** `𝖴𝗅𝗍𝗋𝖺 𝖥𝖺𝗌𝗍`"
  )
  
