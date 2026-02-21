# 𝖥𝗂𝗅𝖾: 𝗁𝖾𝗅𝗉𝖾𝗋_𝖺𝗀𝖾𝗇𝗍.𝗉𝗒
# 𝖣𝖾𝗌𝗂𝗀𝗇𝖾𝖽 𝖿𝗈𝗋: 𝖬𝖺𝗌𝗍𝖾𝗋 𝖩𝖾𝖾𝗍 [𝖤𝗅𝗂𝗍𝖾 𝖤𝗇𝖼𝗈𝖽𝖾𝗋 𝖷𝟫]

import os
import shutil
import time
import asyncio
from datetime import datetime
from config import Config

class EliteHelperAgent:
    def __init__(self):
        self.start_time = time.time()

    @staticmethod
    async def clear_garbage():
        """
        জিৎ, এটি বটের 'বডিগার্ড'। 
        সার্ভারে জমে থাকা অপ্রয়োজনীয় টেম্পোরারি ফাইলগুলো এটি অটো ডিলিট করবে।
        """
        while True:
            await asyncio.sleep(3600) # প্রতি ১ ঘণ্টা পরপর চেক করবে
            folders = ['downloads', 'encoded', 'thumbs']
            for folder in folders:
                if os.path.exists(folder):
                    for filename in os.listdir(folder):
                        file_path = os.path.join(folder, filename)
                        try:
                            # ফাইলটি যদি ২ ঘণ্টার বেশি পুরনো হয়, তবেই ডিলিট করবে
                            if os.path.isfile(file_path) or os.path.islink(file_path):
                                if time.time() - os.path.getmtime(file_path) > 7200:
                                    os.unlink(file_path)
                            elif os.path.isdir(file_path):
                                if time.time() - os.path.getmtime(file_path) > 7200:
                                    shutil.rmtree(file_path)
                        except Exception as e:
                            print(f"Agent Cleanup Error: {e}")

    @staticmethod
    def get_readable_time(seconds: int) -> str:
        """সেকেন্ডকে সুন্দর ইন্ডিয়ান টাইম ফরম্যাটে দেখানোর জন্য"""
        count = 0
        up_time = ""
        time_list = []
        time_suffix_list = ["s", "m", "h", "days"]
        while count < 4:
            count += 1
            if count < 3:
                remainder, result = divmod(seconds, 60)
            else:
                remainder, result = divmod(seconds, 24)
            if seconds == 0 and remainder == 0:
                break
            time_list.append(int(result))
            seconds = int(remainder)
        for i in range(len(time_list)):
            time_list[i] = str(time_list[i]) + time_suffix_list[i]
        if len(time_list) == 4:
            up_time += time_list.pop() + ", "
        time_list.reverse()
        up_time += ":".join(time_list)
        return up_time

    @staticmethod
    async def get_file_info(file_path):
        """ভিডিওর সাইজ এবং ফরম্যাট দ্রুত চেক করার জন্য"""
        size = os.path.getsize(file_path)
        name = os.path.basename(file_path)
        extension = name.split('.')[-1]
        return name, size, extension

# 𝖠𝗀𝖾𝗇𝗍 𝖨𝗇𝗂𝗍𝗂𝖺𝗅𝗂𝗓𝖺𝗍𝗂𝗈𝗇
agent = EliteHelperAgent()
  
