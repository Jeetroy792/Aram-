# 𝖥𝗂𝗅𝖾: 𝗉𝗋𝖾𝗆𝗂𝗎𝗆_𝗁𝖺𝗇𝖽𝗅𝗂𝗇𝗀.𝗉𝗒
# 𝖣𝖾𝗌𝗂𝗀𝗇𝖾𝖽 𝖿𝗈𝗋: 𝖬𝖺𝗌𝗍𝖾𝗋 𝖩𝖾𝖾𝗍 [𝖤𝗅𝗂𝗍𝖾 𝖤𝗇𝖼𝗈𝖽𝖾𝗋 𝖷𝟫]

import time
import asyncio
from database import db
from config import Config

class PremiumHandler:
    
    @staticmethod
    async def is_vip(user_id):
        """ইউজার প্রিমিয়াম কি না এবং তার মেয়াদ আছে কি না তা চেক করে"""
        user_data = await db.get_user(user_id)
        if not user_data:
            return False
            
        if not user_data.get("is_premium", False):
            return False
            
        # মেয়াদ শেষ হয়েছে কি না পরীক্ষা
        expiry = user_data.get("expiry_date", 0)
        if time.time() > expiry:
            # মেয়াদ শেষ, তাই ডাটাবেস আপডেট করা হচ্ছে
            await db.col.update_one(
                {"id": user_id},
                {"$set": {"is_premium": False, "expiry_date": None}}
            )
            return False
            
        return True

    @staticmethod
    async def apply_premium_logic(user_id, ffmpeg_cmd):
        """
        জিৎ, এটি প্রিমিয়াম ইউজারদের জন্য 
        FFmpeg স্পিড বাড়িয়ে দেওয়ার লজিক।
        """
        is_premium = await PremiumHandler.is_vip(user_id)
        
        if is_premium:
            # প্রিমিয়াম ইউজারদের জন্য ফাস্টার এনকোডিং প্রিসেট
            # 'ultrafast' বা 'superfast' ব্যবহার করা হয়েছে
            if "-preset" in ffmpeg_cmd:
                index = ffmpeg_cmd.index("-preset")
                ffmpeg_cmd[index + 1] = "ultrafast"
            return ffmpeg_cmd, "🚀 𝖴𝗅𝗍𝗋𝖺 𝖥𝖺𝗌𝗍 𝖬𝗈𝖽𝖾 (𝖯𝗋𝖾𝗆𝗂𝗎𝗆)"
        else:
            # ফ্রি ইউজারদের জন্য মিডিয়াম স্পিড
            return ffmpeg_cmd, "🐢 𝖲𝗍𝖺𝗇𝖽𝖺𝗋𝖽 𝖲𝗉𝖾𝖾𝖽 (𝖥𝗋𝖾𝖾)"

    @staticmethod
    async def check_task_limit(user_id):
        """ফ্রি ইউজারদের দৈনিক টাস্ক লিমিট চেক করা"""
        is_premium = await PremiumHandler.is_vip(user_id)
        if is_premium:
            return True, "𝖴𝗇𝗅𝗂𝗆𝗂𝗍𝖾𝖽"
            
        user_data = await db.get_user(user_id)
        today_encoded = user_data.get("encoded_today", 0)
        
        if today_encoded >= Config.FREE_LIMIT:
            return False, f"⚠️ 𝖣𝖺𝗂𝗅𝗒 𝖫𝗂𝗆𝗂𝗍 ({Config.FREE_LIMIT}) 𝖤𝗑𝖼𝖾𝖾𝖽𝖾𝖽!"
            
        return True, f"{today_encoded}/{Config.FREE_LIMIT}"

