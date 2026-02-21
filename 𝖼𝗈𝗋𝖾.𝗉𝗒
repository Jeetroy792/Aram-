# 𝖥𝗂𝗅𝖾: 𝖼𝗈𝗋𝖾.𝗉𝗒
# 𝖣𝖾𝗌𝗂𝗀𝗇𝖾𝖽 𝖿𝗈𝗋: 𝖬𝖺𝗌𝗍𝖾𝗋 𝖩𝖾𝖾𝗍 [𝖤𝗅𝗂𝗍𝖾 𝖤𝗇𝖼𝗈𝖽𝖾𝗋 𝖷𝟫]

import asyncio
import os
from brain import brain
from config import Config
from premium_handling import PremiumHandler

class EliteCore:
    def __init__(self):
        # জিৎ, এটি একটি 'Queue' যা সিরিয়াল অনুযায়ী ভিডিও প্রসেস করবে
        self.queue = asyncio.Queue()
        self.is_running = False

    async def worker(self, client):
        """বটের মূল কর্মী যে কিউ থেকে টাস্ক নিয়ে কাজ সম্পন্ন করে"""
        while True:
            # কিউ থেকে পরবর্তী কাজ সংগ্রহ করা
            task = await self.queue.get()
            user_id, message, quality, run_func = task
            
            try:
                # ১. প্রায়োরিটি চেক (প্রিমিয়াম ইউজাররা আগে সুযোগ পাবে)
                is_vip = await PremiumHandler.is_vip(user_id)
                
                # ২. টাস্ক এক্সিকিউশন শুরু
                await run_func(client, message, quality)
                
            except Exception as e:
                print(f"Core Error: {e}")
            finally:
                # কাজ শেষ, কিউ খালি করা
                self.queue.task_done()

    async def add_to_queue(self, user_id, message, quality, run_func):
        """নতুন কোনো ভিডিও আসলে তা কিউতে যোগ করার লজিক"""
        # ইউজার কি অলরেডি কিউতে আছে?
        if user_id in brain.active_tasks:
            return False, "⚠️ 𝖸𝗈𝗎 𝖺𝗅𝗋𝖾𝖺𝖽𝗒 𝗁𝖺𝗏𝖾 𝖺 𝗉𝖾𝗇𝖽𝗂𝗇𝗀 𝗍𝖺𝗌𝗄!"
            
        await self.queue.put((user_id, message, quality, run_func))
        return True, f"✅ **𝖠𝖽𝖽𝖾𝖽 𝗍𝗈 𝖰𝗎𝖾𝗎𝖾.** 𝖯𝗈𝗌𝗂𝗍𝗂𝗈𝗇: `{self.queue.qsize()}`"

    def get_system_load(self):
        """সার্ভারের বর্তমান লোড চেক করা (CPU/RAM)"""
        import psutil
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        return cpu, ram

# 𝖨𝗇𝗌𝗍𝖺𝗇𝗍𝗂𝖺𝗍𝗂𝗇𝗀 𝗍𝗁𝖾 𝖢𝗈𝗋𝖾 𝖤𝗇𝗀𝗂𝗇𝖾
core_engine = EliteCore()

