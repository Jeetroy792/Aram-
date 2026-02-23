# 𝖥𝗂𝗅𝖾: 𝗍𝗂𝗆𝖾_𝗎𝗍𝗂𝗅𝗌.𝗉𝗒

from datetime import datetime
import pytz

def get_ist_time():
    """ভারতীয় সময় (IST) অনুযায়ী বর্তমান সময় বের করা"""
    IST = pytz.timezone('Asia/Kolkata')
    datetime_ist = datetime.now(IST)
    return datetime_ist.strftime('%Y-%m-%d %I:%M:%S %p')

def format_expiry_date(timestamp):
    """টাইমস্ট্যাম্পকে রিডেবল ইন্ডিয়ান ফরম্যাটে কনভার্ট করা"""
    IST = pytz.timezone('Asia/Kolkata')
    date = datetime.fromtimestamp(timestamp, IST)
    return date.strftime('%d %b %Y, %I:%M %p')

