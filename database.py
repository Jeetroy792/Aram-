# 𝖥𝗂𝗅𝖾: 𝖽𝖺𝗍𝖺𝖻𝖺𝗌𝖾.𝗉𝗒
# 𝖣𝖾𝗌𝗂𝗀𝗇𝖾𝖽 𝖿𝗈𝗋: 𝖬𝖺𝗌𝗍𝖾𝗋 𝖩𝖾𝖾𝗍 [𝖤𝗅𝗂𝗍𝖾 𝖤𝗇𝖼𝗈𝖽𝖾ר 𝖷𝟫]

import motor.motor_asyncio
from config import Config
import time

class Database:
    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.users
        self.settings = self.db.settings

    def new_user(self, id):
        """নতুন ইউজারের জন্য একটি ডিফল্ট প্রোফাইল তৈরি করা"""
        return dict(
            id=id,
            join_date=time.time(),
            is_premium=False,
            expiry_date=None,
            thumb=None,
            watermark=None,
            last_verify=0,
            current_token=None,
            total_encoded=0
        )

    async def add_user(self, id):
        """ইউজারকে ডাটাবেসে যুক্ত করা"""
        user = self.new_user(id)
        await self.col.insert_one(user)

    async def is_user_exist(self, id):
        """ইউজার আছে কিনা চেক করা"""
        user = await self.col.find_one({'id': int(id)})
        return True if user else False

    async def get_user(self, id):
        """ইউজারের সম্পূর্ণ তথ্য বের করা"""
        return await self.col.find_one({'id': int(id)})

    async def total_users_count(self):
        """মোট ইউজারের সংখ্যা বের করা"""
        count = await self.col.count_documents({})
        return count

    async def get_all_users(self):
        """সব ইউজারের লিস্ট বের করা (ব্রডকাস্টের জন্য)"""
        return self.col.find({})

    async def delete_user(self, user_id):
        """ইউজার ডিলিট করা"""
        await self.col.delete_many({'id': int(user_id)})

    # --- 𝖳𝖧𝖴𝖬𝖡𝖭𝖠𝖨𝖫 & 𝖶𝖠𝖳𝖤𝖱𝖬𝖠𝖱𝖪 𝖫𝖮𝖦𝖨𝖢 ---
    async def set_thumb(self, id, file_id):
        await self.col.update_one({'id': int(id)}, {'$set': {'thumb': file_id}})

    async def get_thumb(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user.get("thumb", None)

    async def set_watermark(self, id, text):
        await self.col.update_one({'id': int(id)}, {'$set': {'watermark': text}})

    # --- 𝖯𝖱𝖤𝖬𝖨𝖴𝖬 & 𝖵𝖤𝖱𝖨𝖥𝖨𝖢𝖠𝖳𝖨𝖮𝖭 𝖲𝖸𝖲𝖳𝖤𝖬 ---
    async def update_verify_status(self, id, verify=False):
        """ইউজারের ভেরিফিকেশন টাইম আপডেট করা"""
        if verify:
            await self.col.update_one({'id': int(id)}, {'$set': {'last_verify': time.time()}})

    async def set_user_token(self, id, token):
        await self.col.update_one({'id': int(id)}, {'$set': {'current_token': token}})

    async def get_user_token(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user.get("current_token", None)

    async def make_premium(self, id, days):
        """ইউজারকে প্রিমিয়াম করার লজিক"""
        expiry = time.time() + (days * 86400)
        await self.col.update_one({'id': int(id)}, {'$set': {'is_premium': True, 'expiry_date': expiry}})
        return expiry

    async def increment_encoded_count(self, id):
        """ইউজার কয়টি ফাইল এনকোড করেছে তা ট্র্যাক করা"""
        await self.col.update_one({'id': int(id)}, {'$inc': {'total_encoded': 1}})

    async def get_total_encoded_count(self):
        """বট দিয়ে আজ পর্যন্ত মোট কতটি এনকোডিং হয়েছে তার সামারি"""
        pipeline = [{"$group": {"_id": None, "total": {"$sum": "$total_encoded"}}}]
        cursor = self.col.aggregate(pipeline)
        result = await cursor.to_list(length=1)
        return result[0]['total'] if result else 0

# 𝖨𝗇𝗂𝗍𝗂𝖺𝗅𝗂𝗓𝗂𝗇𝗀 𝖣𝖺𝗍𝖺𝖻𝖺𝗌𝖾 𝖢𝗈𝗇𝗇𝖾𝖼𝗍𝗂𝗈𝗇
db = Database(Config.DB_URI, "EliteEncoderBot")
      
