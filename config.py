import datetime
import logging
import os

formatter = '[%(asctime)s] %(levelname)8s --- %(message)s (%(filename)s:%(lineno)s)'
logging.basicConfig(

    filename=f'bot-from-{datetime.datetime.now().date()}.log',
    filemode='w',
    format=formatter,
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.DEBUG
)

ManheimLogin = os.getenv("ManheimLogin")
ManheimPass = os.getenv("ManheimPass")
TOKEN = os.getenv("TOKEN")
CopartURL = os.getenv("CopartURL")


admins = [
    os.getenv("ADMIN_ID"),
]

MANHEIM_MAKE = {
    "101000011": "Chevrolet",
    "101000065": "TOYOTA",
    "101000659": "TESLA",
    "101000037": "LEXUS",
    "101000049": "NISSAN",
    "101000025": "HONDA",
    "101000042": "MAZDA",
    "102000829": "SUBARU"
}
SUBARU = {
    "101000063": "Outback"
}
TESLA = {
    "102187155" : "MODEL S"
}
Chevrolet = {
    "102193165": "Bolt ev",
}
NISSAN = {
    "102011280": "Leaf"
}
HONDA ={
    "102000454": "Accord",
    "102000458": "CR-V",
    "102000463": "Odyssey",
    "102000461": "Fit"
}
MAZDA = {
    "102000617": "Mazda 3"
}


TOYOTA = {
    "102000854" : "Camry",
    "102000853"  : "Avalon",
    "102000871"  : "RAV4",
    "102000851"  : "4Runner",
    "102000861"  : "FJ Cruiser",
    "102192816"  : "Tundra 4WD",
    "102000873": "Sequoia",
    "102000862": "Highlander",
    "102000863": "Highlander Hybrid",
}
LEXUS = {
    "101000659" : "GX460"
}

PLAT = {
    "0": "Manheim",
    "1": "Copart",
}
Copart_TOYOTA = {'Supra', 'Sienna', 'Rav4', '86', 'Corolla', 'Avalon', 'Tundra', 'Yaris', 'Prius', 'Sequoia', 'Mirai', 'Highlander', 'Celica', 'C-HR', '4runner', 'Tacoma', 'Camry', 'FJ_Cruiser', 'Venza'}
Copart_HONDA = {'Crosstour',  'CRV', 'Ridgeline',  'FIT',   'Civic', 'Prelude',   'Clarity',  'Rancher', 'Accord', 'Element',  'Passport',  'HR-V', 'Talon', 'Odyssey', 'Pilot', 'Insight'}
Copart_TESLA = {'Model_X', 'Model_S',  'Model_Y', 'Model_3'}
Copart_LEXUS= {'NX', 'RC', 'IS', 'RX350','RX330', 'LX570', 'RX400', 'UX_200','UX_250H', 'SC430', 'LS430',  'CT_200', 'ES_300',  'LX470', 'RX450',   'ES_350',  'LX570',  'ES_350',  'ES300', 'ES330',  'GX460',   'LS460',   'IS', 'ES 300H LU', 'GX'}
Copart_NISSAN= {'Altima', 'Rogue',  'Sentra' 'Versa', 'Pathfinder', 'Leaf'}
Copart_MAZDA = {'3', 'CX-5',  '6', 'CX-7', 'CX-9'}
Copart_SUBARU = {'XV', 'BRZ', 'B9', 'WRX', 'Forester', 'Tribeca', 'Legacy', 'Baja', 'Crosstrek', 'Impreza', 'Outback'}
Copart_Chevrolet = {'Bolt', 'Volt', 'Suburban'}



REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_PASSWORD = os.getenv("REDIS_PASS")

MINUTE = 60
YEAR = 60*60*24*366
