# 𝖥𝗂𝗅𝖾: 𝖻𝗋𝖺𝗂𝗇.𝗉𝗒
# 𝖣𝖾𝗌𝗂𝗀𝗇𝖾𝖽 𝖿𝗈𝗋: 𝖬𝖺𝗌𝗍𝖾𝗋 𝖩𝖾𝖾𝗍 [𝖤𝗅𝗂𝗍𝖾 𝖤𝗇𝖼𝗈𝖽𝖾𝗋 𝖷𝟫]

import asyncio
import time
from datetime import datetime, timedelta
from database import db
from config import Config

class EliteBrain:
    def __init__(self):
        # 𝖠𝖼𝗍𝗂𝗏𝖾 𝖳𝖺𝗌𝗄𝗌 𝖳𝗋𝖺𝖼𝗄𝖾𝗋
        self.active_tasks = {}
        self.queue_list = []
        self.start_time = time.time()

    async def check_user_access(self, user_id):
        """
        জিৎ, এটি ইউজারের এক্সেস লেভেল চেক করবে (Premium vs Free)।
        এটিই সিদ্ধান্ত নেবে ইউজার কি বিজ্ঞাপন দেখবে নাকি সরাসরি এনকোড পাবে।
        """
        user_data = await db.get_user(user_id)
        if not user_data:
            return "new_user"
        
        is_premium = user_data.get("is_premium", False)
        if is_premium:
            # 𝖯𝗋𝖾𝗆𝗂𝗎𝗆 𝗎𝗌𝖾𝗋𝗌 𝗀𝖾𝗍 𝗎𝗇𝗅𝗂𝗆𝗂𝗍𝖾𝖽 𝖺𝖼𝖼𝖾𝗌𝗌
            return "premium"
        
        # 𝖥𝗋𝖾𝖾 𝗎𝗌𝖾𝗋 𝖳𝗈𝗄𝖾𝗇 𝖫𝗈𝗀𝗂𝖼 (𝟤𝟦-𝗁𝗈𝗎𝗋 𝗏𝖺𝗅𝗂𝖽𝗂𝗍𝗒)
        last_token_time = user_data.get("last_token", 0)
        if (time.time() - last_token_time) < 86400:
            return "verified"
        
        return "needs_verify"

    async def get_queue_position(self, user_id):
        """কিউতে ইউজারের পজিশন কত সেটা ক্যালকুলেট করার লজিক"""
        if user_id in self.active_tasks:
            return 0
        try:
            return self.queue_list.index(user_id) + 1
        except ValueError:
            return len(self.queue_list) + 1

    @staticmethod
    def get_readable_time(seconds):
        """সেকেন্ডকে সুন্দর করে ঘণ্টা/মিনিটে রূপান্তর করার ব্রেইন লজিক"""
        count = 0
        periods = [('𝗁', 3600), ('𝗆', 60), ('𝗌', 1)]
        time_string = ""
        for period_name, period_seconds in periods:
            if seconds >= period_seconds:
                period_value, seconds = divmod(seconds, period_seconds)
                time_string += f"{int(period_value)}{period_name} "
        return time_string.strip()

    @staticmethod
    def get_file_size(size_in_bytes):
        """বাইটস থেকে MB/GB তে রূপান্তরের নিখুঁত হিসাব"""
        if size_in_bytes is None: return "0𝖡"
        size_name = ("𝖡", "𝖪𝖡", "𝖬𝖡", "𝖦𝖡", "𝖳𝖡")
        i = int(math.floor(math.log(size_in_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_in_bytes / p, 2)
        return f"{s} {size_name[i]}"

    async def smart_scheduler(self):
        """
        এটি বটের 'মহা-মস্তিষ্ক'। 
        সার্ভারের লোড অনুযায়ী টাস্ক ডিস্ট্রিবিউট করবে।
        """
        while True:
            if len(self.active_tasks) < Config.MAX_CONCURRENT_TASKS and self.queue_list:
                next_user = self.queue_list.pop(0)
                # 𝖳𝗋𝗂𝗀𝗀𝖾𝗋 𝖶𝗈𝗋𝗄𝖾𝗋 𝖿𝗈𝗋 𝗍𝗁𝗂𝗌 𝗎𝗌𝖾𝗋
                print(f"🧠 𝖡𝗋𝖺𝗂𝗇: 𝖲𝖼𝗁𝖾𝖽𝗎𝗅𝗂𝗇𝗀 𝗇𝖾𝗑𝗍 𝗍𝖺𝗌𝗄 𝖿𝗈𝗋 {next_user}")
            await asyncio.sleep(5)

# 𝖨𝗇𝗂𝗍𝗂𝖺𝗅𝗂𝗓𝗂𝗇𝗀 𝗍𝗁𝖾 𝖡𝗋𝖺𝗂𝗇
brain = EliteBrain()

