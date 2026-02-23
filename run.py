# 𝖥𝗂𝗅𝖾: 𝗋𝗎𝗇.𝗉𝗒
# 𝖣𝖾𝗌𝗂𝗀𝗇𝖾𝖽 𝖿𝗈𝗋: 𝖬𝖺𝗌𝗍𝖾𝗋 𝖩𝖾𝖾𝗍 [𝖤𝗅𝗂𝗍𝖾 𝖤𝗇𝖼𝗈𝖽𝖾𝗋 𝖷𝟫]

import os
import time
import asyncio
from logic import MegaLogic
from functions import EliteFunctions
from brain import brain
from database import db
from config import Config

class TaskRunner:
    @staticmethod
    async def start_encoding(client, message, quality):
        """
        জিৎ, এটিই সেই মেইন ফাংশন যা এনকোডিং প্রসেসটি 
        ডাউনলোড থেকে আপলোড পর্যন্ত নিখুঁতভাবে পরিচালনা করে।
        """
        user_id = message.from_user.id
        start_time = time.time()
        
        # ১. স্ট্যাটাস আপডেট (Elite UI Style)
        status_msg = await message.reply_text("📥 **𝖣𝗈𝗐𝗇𝗅𝗈𝖺𝖽𝗂𝗇𝗀 𝖥𝗂𝗅𝖾...**")
        
        # ২. ফাইল ডাউনলোড লজিক (Functions Sync)
        download_path = await client.download_media(
            message=message,
            progress=EliteFunctions.progress_for_pyrogram,
            progress_args=("📥 **𝖣𝗈𝗐𝗇𝗅𝗈𝖺𝖽𝗂𝗇𝗀...**", status_msg, start_time)
        )
        
        if not download_path:
            return await status_msg.edit("❌ **𝖣𝗈𝗐𝗇𝗅𝗈𝖺𝖽 𝖥𝖺𝗂𝗅𝖾𝖽!**")

        # ৩. এনকোডিং ফেজ (Logic Sync)
        await status_msg.edit(f"⚙️ **𝖤𝗇𝖼𝗈𝖽𝗂𝗇𝗀 𝗍𝗈 {quality}...** \n🚀 **𝖯𝗅𝖾𝖺𝗌𝖾 𝖶𝖺𝗂𝗍!**")
        encoder = MegaLogic(download_path)
        
        # ভিডিওর ডিটেইল বের করা
        metadata = await encoder.get_video_info()
        output_file = await encoder.encode_video(quality)
        
        if not output_file:
            return await status_msg.edit("❌ **𝖤𝗇𝖼𝗈𝖽𝗂𝗇𝗀 𝖤𝗋𝗋𝗈𝗋!**")

        # ৪. থাম্বনেইল ম্যানেজমেন্ট
        await status_msg.edit("🖼 **𝖦𝖾𝗇𝖾𝗋𝖺𝗍𝗂𝗇𝗀 𝖳𝗁𝗎𝗆𝖻𝗇𝖺𝗂𝗅...**")
        thumb = await db.get_thumb(user_id) or await EliteFunctions.take_screenshot(output_file, "thumbs")

        # ৫. আপলোডিং ফেজ (Final Output)
        await status_msg.edit("📤 **𝖴𝗉𝗅𝗈𝖺𝖽𝗂𝗇𝗀 𝖤𝗇𝖼𝗈𝖽𝖾𝖽 𝖥𝗂𝗅𝖾...**")
        up_start = time.time()
        
        caption = Config.DEF_CAP.format(
            file_name=os.path.basename(output_file),
            file_size=EliteFunctions.humanbytes(os.path.getsize(output_file))
        )

        try:
            await client.send_video(
                chat_id=message.chat.id,
                video=output_file,
                caption=caption,
                thumb=thumb,
                duration=int(metadata.get('format', {}).get('duration', 0)),
                progress=EliteFunctions.progress_for_pyrogram,
                progress_args=("📤 **𝖴𝗉𝗅𝗈𝖺𝖽𝗂𝗇𝗀...**", status_msg, up_start)
            )
        except Exception as e:
            await message.reply_text(f"❌ **𝖴𝗉𝗅𝗈𝖺𝖽 𝖤𝗋𝗋𝗈𝗋:** `{e}`")
        finally:
            # ৬. ক্লিনিং (সার্ভার মেমরি বাঁচানোর জন্য)
            await status_msg.delete()
            if os.path.exists(download_path): os.remove(download_path)
            if os.path.exists(output_file): os.remove(output_file)
            if thumb and "thumbs" in thumb: os.remove(thumb)

# 𝖤𝗑𝖾𝖼𝗎𝗍𝗂𝗈𝗇 𝖧𝖺𝗇𝖽𝗅𝖾𝗋
async def run_task(client, message, quality):
    # ব্রেইনকে জানানো যে একটি নতুন টাস্ক শুরু হচ্ছে
    await brain.active_tasks.update({message.from_user.id: True})
    await TaskRunner.start_encoding(client, message, quality)
    # কাজ শেষ হলে ব্রেইন থেকে রিমুভ করা
    brain.active_tasks.pop(message.from_user.id, None)

