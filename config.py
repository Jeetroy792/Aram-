import os
from dotenv import load_dotenv

load_dotenv()

class Config(object):
    # --- Bot Core Config ---
    API_ID = int(os.environ.get("API_ID", 24670806))
    API_HASH = os.environ.get("API_HASH", "82134723a32b2cae76b9cfb3b1570745")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "8490377165:AAHqZoFhpM57_e2hSDhhrv5zvhGVmGyRO5c")
    
    # --- Database Config ---
    DB_URI = os.environ.get("DB_URI", "mongodb+srv://Filestore:ram12345678@cluster0.bcz3n2q.mongodb.net/?appName=Cluster0")
    DB_NAME = os.environ.get("DB_NAME", "EliteEncoderBot")
    
    # --- Admin & Logs ---
    # আইডিগুলো সরাসরি সংখ্যা হিসেবে বসানো হয়েছে
    OWNER_ID = int(os.environ.get("OWNER_ID", 8229228616))
    LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", -1003545815372))
    ADMINS = [OWNER_ID, 56789012]
    
    # --- Force Subscribe ---
    FORCE_SUB_CHANNEL = os.environ.get("FORCE_SUB_CHANNEL", "allfreecoursesforfree")
    
    # --- Shortner & Verification ---
    SL1_URL = os.environ.get("SL1_URL", "gplinks.com")
    SL1_API = os.environ.get("SL1_API", "e07aec576df2a9ed36f1b94b8017cc53b792496f")
    START_PIC = os.environ.get("START_PIC", "IMG_1.png")

    # --- Encoding Settings ---
    FREE_LIMIT = int(os.environ.get("FREE_LIMIT", 5))
    DOWNLOAD_DIR = "./downloads"
    ENCODE_DIR = "./encoded"
    
    # --- UI Customization ---
    START_TEXT = (
        "👋 **Hello {user},**\n\n"
        "I am **Elite Encoder X9**, the most powerful video compressor bot.\n"
        "Send me any video to start encoding!"
    )
    
    # --- Server Config ---
    PORT = int(os.environ.get("PORT", 8080))
