import os, time, re

id_pattern = re.compile(r'^.\d+$') 


class Config(object):
    # pyro client config
    API_ID    = os.environ.get("API_ID", "21740783")  # ⚠️ Required
    API_HASH  = os.environ.get("API_HASH", "a5dc7fec8302615f5b441ec5e238cd46") # ⚠️ Required
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "6610201435:AAHEv2YoM2ZEtlEdqjilv9mZGjT9Uzzrntw") # ⚠️ Required
    FORCE_SUB = os.environ.get('FORCE_SUB', 'Anime_warrior_tamil') # ⚠️ Required
    AUTH_CHANNEL = int(FORCE_SUB) if FORCE_SUB and id_pattern.search(
    FORCE_SUB) else None
   
    # database config
    DB_URL  = os.environ.get("DB_URL", "mongodb+srv://Speedwolf1:speedwolf24689@cluster0.rgfywsf.mongodb.net/")  # ⚠️ Required
    DB_NAME  = os.environ.get("DB_NAME","Speedwolf1") 

    # Other Configs 
    ADMIN = [6299192020, 6693549185, 6121610691, 7035627523] # ⚠️ Required
    LOG_CHANNEL = os.environ.get('LOG_CHANNEL', None) # ⚠️ Required
    BOT_UPTIME = BOT_UPTIME  = time.time()
    START_PIC = os.environ.get("START_PIC", "https://graph.org/file/15e82d7e665eccc8bd9c5.jpg")

    # wes response configuration     
    WEBHOOK = bool(os.environ.get("WEBHOOK", True))
    PORT = int(os.environ.get("PORT", "8080"))
    WARN = """❌ You Can't Able to use the Bot"""


    caption = """
**File Name**: {0}

**Original File Size:** {1}
**Encoded File Size:** {2}
**Compression Percentage:** {3}

__Downloaded in {4}__
__Encoded in {5}__
__Uploaded in {6}__
"""
