# 𝖥𝗂𝗅𝖾: 𝖿_𝗌𝗎b.𝗉𝗒
# 𝖣𝖾𝗌𝗂𝗀𝗇𝖾𝖽 𝖿𝗈𝗋: 𝖬𝖺𝗌𝗍𝖾𝗋 𝖩𝖾𝖾𝗍 [𝖤𝗅𝗂𝗍𝖾 𝖤𝗇𝖼𝗈𝖽𝖾𝗋 𝖷𝟫]

import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant
from config import Config

async def force_sub_handler(client, message):
    """
    জিৎ, এটি প্রতিটি মিডিয়া বা কমান্ডের আগে ইউজারকে চেক করবে।
    ইউজার চ্যানেলে না থাকলে তাকে সুন্দর একটি বাটন সহ মেসেজ দেবে।
    """
    # অ্যাডমিন বা ওনারের জন্য ফোর্স সাব চেক করার দরকার নেই
    if message.from_user.id in Config.ADMINS:
        return True

    # যদি চ্যানেলের আইডি কনফিগার করা না থাকে, তবে সরাসরি কাজ করবে
    if not Config.FORCE_SUB_CHANNEL:
        return True

    try:
        user = await client.get_chat_member(Config.FORCE_SUB_CHANNEL, message.from_user.id)
        if user.status == "kicked":
            await message.reply_text("❌ **𝖲𝗈𝗋𝗋𝗒, 𝗒𝗈𝗎 𝖺𝗋𝖾 𝖻𝖺𝗇𝗇𝖾𝖽 𝖿𝗋𝗈𝗆 𝗎𝗌𝗂𝗇𝗀 𝗍𝗁𝗂𝗌 𝖻𝗈𝗍.**")
            return False
        return True

    except UserNotParticipant:
        # ইউজার চ্যানেলে নেই, তাই তাকে জয়েন করার জন্য স্টাইলিশ বাটন দাও
        invite_link = await client.export_chat_invite_link(Config.FORCE_SUB_CHANNEL)
        
        buttons = [
            [
                InlineKeyboardButton("📢 𝖩𝗈𝗂𝗇 𝖮𝗎𝗋 𝖢𝗁𝖺𝗇𝗇𝖾𝗅 📢", url=invite_link)
            ]
        ]
        
        # জিৎ, এখানে সেই 'Nick Bypass' স্টাইলের বাটন লজিক আছে
        if message.command and message.command[0] != "start":
            buttons.append([InlineKeyboardButton("🔄 𝖳𝗋𝗒 𝖠𝗀𝖺𝗂𝗇", url=f"https://t.me/{(await client.get_me()).username}?start=true")])

        text = (
            "⚠️ **𝖠𝖼𝖼𝖾𝗌𝗌 𝖣𝖾𝗇𝗂𝖾𝖽!**\n\n"
            "𝗒𝗈𝗎 𝗆𝗎𝗌𝗍 𝗃𝗈𝗂𝗇 𝗈𝗎𝗋 𝗎𝗉𝖽𝖺𝗍𝖾 𝖼𝗁𝖺𝗇𝗇𝖾𝗅 𝗍𝗈 𝗎𝗌𝖾 𝗍𝗁𝗂𝗌 𝖻𝗈𝗍.\n"
            "𝖽𝗎𝖾 𝗍𝗈 𝗁𝗂𝗀𝗁 𝗌𝖾𝗋𝗏𝖾𝗋 𝗅𝗈𝖺𝖽, 𝗈𝗇𝗅𝗒 𝖼𝗁𝖺𝗇𝗇𝖾𝗅 𝗌𝗎𝖻𝗌𝖼𝗋𝗂𝖻𝖾𝗋𝗌 𝖼𝖺𝗇 𝗎𝗌𝖾 𝗆𝖾!"
        )
        
        await message.reply_text(
            text=text,
            reply_markup=InlineKeyboardMarkup(buttons),
            quote=True
        )
        return False
    except Exception as e:
        print(f"Error in F-Sub: {e}")
        return True # এরর হলে যাতে বট কাজ বন্ধ না করে
