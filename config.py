import re, os

id_pattern = re.compile(r'^.\d+$') 

API_ID = os.environ.get("API_ID", "12936189")

API_HASH = os.environ.get("API_HASH", "7e24008e8ec33a397155b6a9d618497b")

BOT_TOKEN = os.environ.get("BOT_TOKEN", "6396913711:AAFJpA3eMFa1Nzo9aHVGsuPys-mSocXemUY") 

FORCE_SUB = os.environ.get("FORCE_SUB", "-1001640719273") 

DB_NAME = os.environ.get("DB_NAME","Cluster0Rename")     

DB_URL = os.environ.get("DB_URL","mongodb+srv://gill1322:gill1322@cluster0rename.x8jiptm.mongodb.net/?retryWrites=true&w=majority")
 
FLOOD = int(os.environ.get("FLOOD", "10"))

START_PIC = os.environ.get("START_PIC", "")

ADMIN = [int(admin) if id_pattern.search(admin) else admin for admin in os.environ.get('ADMIN', '1166670205').split()]

# Bot_Username = "@LazyPrincessXBOT"
BOT_USERNAME = os.environ.get("BOT_USERNAME", "@FileRenamesRobot")

PORT = os.environ.get('PORT', '8080')

String_Session  = "None"

Lazy_session = {}

Permanent_4gb = "-100XXX"
