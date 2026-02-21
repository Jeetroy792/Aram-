# 𝖥𝗂𝗅𝖾: 𝗎𝗂_𝗌𝗍𝗒𝗅𝖾.𝗉𝗒
# 𝖢𝗈𝖽𝖾𝖽 𝖲𝗉𝖾𝖼𝗂𝖺𝗅𝗅𝗒 𝖿𝗈𝗋 𝖬𝖺𝗌𝗍𝖾𝗋 𝖩𝖾𝖾𝗍

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

class EliteLook:
    @staticmethod
    def start_text(name):
        """
        জিৎ, এটি বটের মেইন স্টার্ট মেসেজ। 
        এখানে ইউনিক ফন্ট এবং ইমোজি ব্যবহার করা হয়েছে।
        """
        return (
            f"👋 **𝖧𝖾𝗒, 𝖨'𝗆 𝖠𝗇 𝖤𝗅𝗂𝗍𝖾 𝖤𝗇𝖼𝗈𝖽𝖾𝗋 𝖡𝗈𝗍 𝖲𝗉𝖾𝖼𝗂𝖺𝗅𝗅𝗒**\n"
            f"**𝖢𝗈𝖽𝖾𝖽 𝖥𝗈𝗋** @{name} **𝖯𝖱𝖮**\n\n"
            "✨ **𝖨 𝖼𝖺𝗇 𝗉𝗋𝗈𝖼𝖾𝗌𝗌 𝗏𝗂𝖽𝖾𝗈𝗌 𝗐𝗂𝗍𝗁 𝖴𝗅𝗍𝗋𝖺-𝖥𝖺𝗌𝗍 𝖲𝗉𝖾𝖾𝖽.**\n"
            "📥 **𝖩𝗎𝗌𝗍 𝗌𝖾𝗇𝖽 𝗆𝖾 𝖺𝗇𝗒 𝗏𝗂𝖽𝖾𝗈 𝗍𝗈 𝗌𝗍𝖺𝗋𝗍 𝖾𝗇𝖼𝗈𝖽𝗂𝗇𝗀.**\n"
            "━━━━━━━━━━━━━━━━━━━━"
        )

    @staticmethod
    def main_menu():
        """
        স্ক্রিনশটের মতো বড় এবং কালারফুল বাটন লজিক।
        """
        buttons = [
            [
                InlineKeyboardButton("🚀 𝖢𝗁𝖺𝗇𝗇𝖾𝗅 🚀", url="https://t.me/your_channel")
            ],
            [
                InlineKeyboardButton("🤴 𝖣𝗈𝗇𝖺𝗍𝖾 𝖠𝗍 𝖸𝗈𝗎𝗋 𝖶𝗂𝗅𝗅 🤴", callback_data="donate")
            ],
            [
                InlineKeyboardButton("🤡 𝖠𝖻𝗈𝗎𝗍 🤡", callback_data="about_bot")
            ],
            [
                InlineKeyboardButton("⚙️ 𝖲𝖾𝗍𝗍𝗂𝗇𝗀𝗌", callback_data="settings"),
                InlineKeyboardButton("📝 𝖧𝖾𝗅𝗉", callback_data="help")
            ],
            [
                InlineKeyboardButton("💎 𝖡𝗎𝗒 𝖯𝗋𝖾𝗆𝗂𝗎𝗆 (𝖭𝗈 𝖠𝖽𝗌) 💎", callback_data="buy_vip")
            ]
        ]
        return InlineKeyboardMarkup(buttons)

    @staticmethod
    def encoding_buttons():
        """
        ভিডিও পাওয়ার পর যে স্টাইলিশ এনকোডিং অপশনগুলো আসবে।
        """
        buttons = [
            [
                InlineKeyboardButton("⚡ 𝟦𝟪𝟶𝗉 (𝖲𝖣)", callback_data="enc_480p"),
                InlineKeyboardButton("🎬 𝟩𝟤𝟶𝗉 (𝖧𝖣)", callback_data="enc_720p")
            ],
            [
                InlineKeyboardButton("🔥 𝟣𝟶𝟪𝟶𝗉 (𝖥𝖧𝖣)", callback_data="enc_1080p"),
                InlineKeyboardButton("💎 𝟤𝟣𝟨𝟶𝗉 (𝟦𝖪)", callback_data="enc_2160p")
            ],
            [
                InlineKeyboardButton("🛠 𝖠𝖽𝗏𝖺𝗇𝖼𝖾𝖽 𝖬𝖾𝖽𝗂𝖺 𝖳𝗈𝗈𝗅𝗌 🛠", callback_data="tools_menu")
            ],
            [
                InlineKeyboardButton("❌ 𝖢𝖺𝗇𝖼𝖾𝗅 𝖯𝗋𝗈𝖼𝖾𝗌𝗌", callback_data="close")
            ]
        ]
        return InlineKeyboardMarkup(buttons)

    @staticmethod
    def progress_bar(current, total):
        """
        একটি প্রফেশনাল প্রগ্রেস বার যা দেখতে দারুণ লাগবে।
        """
        percentage = current * 100 / total
        finished_blocks = int(percentage / 10)
        bar = "▰" * finished_blocks + "▱" * (10 - finished_blocks)
        return f"[{bar}] {round(percentage, 2)}%"
      
