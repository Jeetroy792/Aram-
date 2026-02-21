# 𝖥𝗂𝗅𝖾: verify.𝗉𝗒
# 𝖣𝖾𝗌𝗂𝗀𝗇𝖾𝖽 𝖿𝗈𝗋: 𝖬𝖺𝗌𝗍𝖾𝗋 𝖩𝖾𝖾𝗍 [𝖤𝗅𝗂𝗍𝖾 𝖤𝗇𝖼𝗈𝖽𝖾𝗋 𝖷𝟫]

import time
import aiohttp
from database import db
from config import Config
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

class ShortnerLogic:
    
    @staticmethod
    async def get_shortlink(url, api, link):
        """শর্টলিংক এপিআই ব্যবহার করে ইউআরএল জেনারেট করার ফাংশন"""
        params = {'api': api, 'url': link}
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params, raise_for_status=True) as response:
                    data = await response.json()
                    return data["shortenedUrl"]
        except Exception as e:
            print(f"Error generating shortlink: {e}")
            return link

    @staticmethod
    async def verify_user(client, message):
        """
        জিৎ, এটি ডাইনামিক ভেরিফিকেশন লজিক। 
        ইউজার যখন শর্টলিংক পার করে আসবে, তখন এই ফাংশন তাকে ভেরিফাইড করবে।
        """
        user_id = message.from_user.id
        token = message.command[1].split("-")[1]
        
        # ডাটাবেস থেকে টোকেন চেক করা
        saved_token = await db.get_user_token(user_id)
        
        if token == saved_token:
            await db.update_verify_status(user_id, verify=True)
            await message.reply_text(
                "✅ **𝖵𝖾𝗋𝗂𝖿𝗂𝖼𝖺𝗍𝗂𝗈𝗇 𝖲𝗎𝖼𝖼𝖾𝗌𝗌𝖿𝗎𝗅𝗅!**\n"
                "𝖸𝗈𝗎 𝖼𝖺𝗇 𝗇𝗈𝗐 𝗎𝗌𝖾 𝗆𝖾 𝖿𝗈𝗋 𝗍𝗁𝖾 𝗇𝖾𝗑𝗍 𝟤𝟦 𝗁𝗈𝗎𝗋𝗌.",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🚀 𝖲𝗍𝖺𝗋𝗍 𝖴𝗌𝗂𝗇𝗀", callback_data="help")]])
            )
        else:
            await message.reply_text("❌ **𝖨𝗇𝗏𝖺𝗅𝗂𝖽 𝖳𝗈𝗄𝖾𝗇 𝗈𝗋 𝖤𝗑𝗉𝗂𝗋𝖾𝖽!**")

async def shortner_handler(client, message):
    """
    এটি চেক করবে ইউজারের টোকেন ভ্যালিড আছে কিনা। 
    না থাকলে তাকে শর্টলিংক জেনারেট করে দেবে।
    """
    user_id = message.from_user.id
    user_data = await db.get_user(user_id)
    
    # ১. ইউজার যদি প্রিমিয়াম হয়, তবে ভেরিফিকেশন লাগবে না
    if user_data.get("is_premium"):
        return True

    # ২. টাইম চেক (২৪ ঘণ্টার ভ্যালিডিটি)
    last_verify = user_data.get("last_verify", 0)
    if (time.time() - last_verify) < 86400:
        return True

    # ৩. নতুন টোকেন জেনারেট করা
    token = "".join(random.choices(string.ascii_letters + string.digits, k=10))
    await db.set_user_token(user_id, token)
    
    bot_username = (await client.get_me()).username
    verification_link = f"https://t.me/{bot_username}?start=verify-{token}"
    short_url = await ShortnerLogic.get_shortlink(Config.SL1_URL, Config.SL1_API, verification_link)

    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔐 𝖢𝗅𝗂𝖼𝗄 𝖧𝖾𝗋𝖾 𝗍𝗈 𝖵𝖾𝗋𝗂𝖿𝗒", url=short_url)],
        [InlineKeyboardButton("❓ 𝖧𝗈𝗐 𝗍𝗈 𝖵𝖾𝗋𝗂𝖿𝗒 (𝖳𝗎𝗍𝗈𝗋𝗂𝖺𝗅)", url="https://t.me/your_tutorial")]
    ])

    await message.reply_text(
        "⚠️ **𝖠𝖼𝖼𝖾𝗌𝗌 𝖣𝖾𝗇𝗂𝖾𝖽!**\n\n"
        "𝖸𝗈𝗎 𝗇𝖾𝖾𝖽 𝗍𝗈 𝗏𝖾𝗋𝗂𝖿𝗒 𝗒𝗈𝗎𝗋 𝖺𝖼𝖼𝖾𝗌𝗌 𝗍𝗈 𝗎𝗌𝖾 𝗍𝗁𝗂𝗌 𝖻𝗈𝗍 𝖿𝗈𝗋 𝗍𝗁𝖾 𝗇𝖾𝗑𝗍 𝟤𝟦 𝗁𝗈𝗎𝗋𝗌.",
        reply_markup=buttons
    )
    return False
  
