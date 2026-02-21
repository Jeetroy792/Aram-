# 𝖥𝗂𝗅𝖾: 𝖻𝗋𝗈𝖺𝖽𝖼𝖺𝗌𝗍.𝗉𝗒
# 𝖣𝖾𝗌𝗂𝗀𝗇𝖾𝖽 𝖿𝗈𝗋: 𝖬𝖺𝗌𝗍𝖾𝗋 𝖩𝖾𝖾𝗍 [𝖤𝗅𝗂𝗍𝖾 𝖤𝗇𝖼𝗈𝖽𝖾𝗋 𝖷𝟫]

import asyncio
import time
import datetime
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, InputUserDeactivated, UserIsBlocked, PeerIdInvalid
from database import db
from config import Config

class EliteBroadcast:
    def __init__(self):
        self.is_broadcasting = False

    async def send_msg(self, user_id, message):
        """ইউজারকে মেসেজ পাঠানোর মূল লজিক যা এরর হ্যান্ডেল করবে"""
        try:
            await message.copy(chat_id=user_id)
            return 200, None
        except FloodWait as e:
            await asyncio.sleep(e.value)
            return await self.send_msg(user_id, message)
        except InputUserDeactivated:
            await db.delete_user(user_id)
            return 404, "Deleted"
        except UserIsBlocked:
            await db.delete_user(user_id)
            return 404, "Blocked"
        except PeerIdInvalid:
            await db.delete_user(user_id)
            return 404, "Invalid"
        except Exception as e:
            return 500, e

@Client.on_message(filters.command("broadcast") & filters.user(Config.OWNER_ID) & filters.reply)
async def start_broadcast(client, message):
    """
    জিৎ, এই কমান্ডটি তোমার রিপ্লাই করা মেসেজটি সবার কাছে পাঠিয়ে দেবে।
    এটি রিয়েল-টাইম স্ট্যাটাস আপডেট দেবে।
    """
    broadcast_engine = EliteBroadcast()
    all_users = await db.get_all_users()
    users = await all_users.to_list(length=100000) # বিশাল ইউজার বেস হ্যান্ডেল করার ক্ষমতা
    
    total_users = len(users)
    done = 0
    blocked = 0
    deleted = 0
    failed = 0
    success = 0
    
    start_time = time.time()
    status_msg = await message.reply_text(f"📢 **𝖡𝗋𝗈𝖺𝖽𝖼𝖺𝗌𝗍 𝖲𝗍𝖺𝗋𝗍𝖾𝖽...**\n🎯 **𝖳𝖺𝗋𝗀𝖾𝗍:** `{total_users}` 𝗎𝗌𝖾𝗋𝗌")

    for user in users:
        user_id = int(user['id'])
        code, err = await broadcast_engine.send_msg(user_id, message.reply_to_message)
        
        if code == 200:
            success += 1
        elif code == 404:
            if err == "Blocked": blocked += 1
            else: deleted += 1
        else:
            failed += 1
        
        done += 1
        
        # প্রতি ১০ জন পরপর স্ট্যাটাস আপডেট করা (সার্ভার সেফটি)
        if done % 10 == 0:
            try:
                await status_msg.edit(
                    f"📢 **𝖡𝗋𝗈𝖺𝖽𝖼𝖺𝗌𝗍𝗂𝗇𝗀...**\n\n"
                    f"✅ **𝖲𝗎𝖼𝖼𝖾𝗌𝗌:** `{success}`\n"
                    f"🚫 **𝖡𝗅𝗈𝖼𝗄𝖾𝖽:** `{blocked}`\n"
                    f"🗑️ **𝖣𝖾𝗅𝖾𝗍𝖾𝖽:** `{deleted}`\n"
                    f"⚠️ **𝖥𝖺𝗂𝗅𝖾𝖽:** `{failed}`\n\n"
                    f"📊 **𝖯𝗋𝗈𝗀𝗋𝖾𝗌𝗌:** `{done}/{total_users}`"
                )
            except:
                pass

    time_taken = str(datetime.timedelta(seconds=int(time.time() - start_time)))
    await status_msg.edit(
        f"✅ **𝖡𝗋𝗈𝖺𝖽𝖼𝖺𝗌𝗍 𝖢𝗈𝗆𝗉𝗅𝖾𝗍𝖾𝖽!**\n\n"
        f"⏱️ **𝖳𝗂𝗆𝖾 𝖳𝖺𝗄𝖾𝗇:** `{time_taken}`\n"
        f"🎯 **𝖳𝗈𝗍𝖺𝗅 𝖴𝗌𝖾𝗋𝗌:** `{total_users}`\n"
        f"🟢 **𝖲𝗎𝖼𝖼𝖾𝗌𝗌:** `{success}`\n"
        f"🔴 **𝖥𝖺𝗂𝗅𝖾𝖽/𝖡𝗅𝗈𝖼𝗄𝖾𝖽:** `{blocked + deleted + failed}`"
    )

