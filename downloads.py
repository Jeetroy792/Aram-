# 𝖥𝗂𝗅𝖾: 𝖽𝗈𝗐𝗇𝗅𝗈𝖺𝖽𝗌.𝗉𝗒
# 𝖣𝖾𝗌𝗂𝗀𝗇𝖾𝖽 𝖿𝗈𝗋: 𝖬𝖺𝗌𝗍𝖾r 𝖩𝖾𝖾𝗍 [𝖤𝗅𝗂𝗍𝖾 𝖤𝗇𝖼𝗈𝖽𝖾𝗋 𝖷𝟫]

import os
import time
import math
from pyrogram.errors import FloodWait
from utils.ui_style import UIStyle # জিৎ, এটি বাটন ও টেক্সট স্টাইল করবে

async def progress_bar(current, total, ud_type, message, start):
    """ডাউনলোড বা আপলোডের সময় সুন্দর প্রগ্রেস বার দেখানোর ফাংশন"""
    now = time.time()
    diff = now - start
    if round(diff % 10.00) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion

        elapsed_str = display_time(elapsed_time // 1000)
        remaining_str = display_time(time_to_completion // 1000)

        # 🟩🟩🟩⬜⬜ স্টাইলের বার
        tmp = f"{['🟩' * int(math.floor(percentage / 10)) + '⬜' * (10 - int(math.floor(percentage / 10)))]}"
        
        progress = (
            f"📊 **{ud_type} 𝖨𝗇 𝖯𝗋𝗈𝗀𝗋𝖾𝗌𝗌...**\n\n"
            f"{tmp}\n"
            f"🚀 **𝖯𝖾𝗋𝖼𝖾𝗇𝗍𝖺𝗀𝖾:** `{round(percentage, 2)}%`\n"
            f"📂 **𝖲𝗂𝗓𝖾:** `{humanbytes(current)} / {humanbytes(total)}`\n"
            f"⚡ **𝖲𝗉𝖾𝖾𝖽:** `{humanbytes(speed)}/𝗌`\n"
            f"⏳ **𝖤𝖳𝖠:** `{remaining_str}`\n"
        )
        
        try:
            await message.edit(
                text=progress,
                reply_markup=UIStyle.cancel_button() # ক্যানসেল বাটন যোগ করা হয়েছে
            )
        except FloodWait as e:
            await asyncio.sleep(e.value)
        except:
            pass

def humanbytes(size):
    """বাইটকে সুন্দর KB/MB/GB তে রূপান্তর করা"""
    if not size:
        return "0 B"
    for unit in ['', '𝖪𝖡', '𝖬𝖡', '𝖦𝖡', '𝖳𝖡']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024

def display_time(seconds):
    """সেকেন্ডকে রিডেবল টাইম ফরম্যাটে দেখানো"""
    result = ""
    for unit, div in [('𝖽', 86400), ('𝗁', 3600), ('𝗆', 60), ('𝗌', 1)]:
        n, seconds = divmod(seconds, div)
        if n > 0:
            result += f"{n}{unit} "
    return result.strip()

async def download_file(client, message, download_path):
    """টেলিগ্রাম থেকে ফাইল ডাউনলোড করার মেইন ফাংশন"""
    start_time = time.time()
    try:
        file_path = await client.download_media(
            message=message,
            file_name=download_path,
            progress=progress_bar,
            progress_args=("𝖣𝗈𝗐𝗇𝗅𝗈𝖺𝖽𝗂𝗇𝗀", message, start_time)
        )
        return file_path
    except Exception as e:
        print(f"Download Error: {e}")
        return None
      
