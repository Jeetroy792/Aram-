# 𝖥𝗂𝗅𝖾: 𝖿𝗎𝗇𝖼𝗍𝗂𝗈𝗇𝗌.𝗉𝗒
# 𝖣𝖾𝗌𝗂𝗀𝗇𝖾𝖽 𝖿𝗈𝗋: 𝖬𝖺𝗌𝗍𝖾𝗋 𝖩𝖾𝖾𝗍 [𝖤𝗅𝗂𝗍𝖾 𝖤𝗇𝖼𝗈𝖽𝖾𝗋 𝖷𝟫]

import os
import time
import math
import asyncio
from pyrogram.errors import FloodWait

class EliteFunctions:
    
    @staticmethod
    def humanbytes(size):
        """বাইটস থেকে প্রফেশনাল রিডেবল ফরম্যাটে কনভার্ট করার ফাংশন"""
        if not size:
            return "0 B"
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return f"{size:.2f} {unit}"
            size /= 1024.0

    @staticmethod
    def TimeFormatter(milliseconds: int) -> str:
        """মিলিসেকেন্ড থেকে HH:MM:SS ফরম্যাটে সময় দেখানোর ফাংশন"""
        seconds, milliseconds = divmod(int(milliseconds), 1000)
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)
        tmp = ((str(days) + "d, ") if days else "") + \
              ((str(hours) + "h, ") if hours else "") + \
              ((str(minutes) + "m, ") if minutes else "") + \
              ((str(seconds) + "s, ") if seconds else "")
        return tmp[:-2]

    @staticmethod
    async def progress_for_pyrogram(current, total, ud_type, message, start):
        """
        জিৎ, এটিই সেই প্রফেশনাল প্রগ্রেস বার যা তুমি স্ক্রিনশটে চেয়েছিলে।
        এটি আপলোড এবং ডাউনলোডের সময় রিয়েল-টাইম আপডেট দেবে।
        """
        now = time.time()
        diff = now - start
        if round(diff % 10.00) == 0 or current == total:
            percentage = current * 100 / total
            speed = current / diff
            elapsed_time = round(diff) * 1000
            time_to_completion = round((total - current) / speed) * 1000
            estimated_total_time = elapsed_time + time_to_completion

            elapsed_time_str = EliteFunctions.TimeFormatter(elapsed_time)
            estimated_total_time_str = EliteFunctions.TimeFormatter(estimated_total_time)

            progress = "[{0}{1}] \n**𝖯𝗋𝗈𝗀𝗋𝖾𝗌𝗌:** `{2}%` \n".format(
                ''.join(["▰" for i in range(math.floor(percentage / 10))]),
                ''.join(["▱" for i in range(10 - math.floor(percentage / 10))]),
                round(percentage, 2))

            tmp = progress + \
                  f"**𝖲𝗉𝖾𝖾𝖽:** `{EliteFunctions.humanbytes(speed)}/s` \n" + \
                  f"**𝖤𝖳𝖠:** `{estimated_total_time_str if estimated_total_time_str != '' else '0s'}` \n"

            try:
                await message.edit(
                    text=f"{ud_type}\n{tmp}"
                )
            except FloodWait as e:
                await asyncio.sleep(e.value)
            except Exception:
                pass

    @staticmethod
    async def take_screenshot(video_file, output_directory):
        """ভিডিও থেকে অটোমেটিক থাম্বনেইল জেনারেট করার ফাংশন"""
        out_file = os.path.join(output_directory, str(time.time()) + ".jpg")
        cmd = [
            "ffmpeg",
            "-ss", "00:00:01",
            "-i", video_file,
            "-vframes", "1",
            "-q:v", "2",
            out_file
        ]
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        await process.communicate()
        if os.path.lexists(out_file):
            return out_file
        return None

