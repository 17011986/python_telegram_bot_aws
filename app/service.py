import pickle
from database import r
from database import cache
from app.dialogs import msg
from config import PLAT, MANHEIM_MAKE
from aiogram.utils.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


menu_cd = CallbackData("show_menu", "level", "platform", "make", "model", "code", "gn", "gf")
buy_item = CallbackData("buy", "platform", "make", "model", "code", "gn", "gf", "cn")


def make_callback_data(level, platform="0", make="0", model="0", code="0", gn="0", gf="0"):
    return menu_cd.new(level=level, platform=platform, make=make, model=model, code=code, gn=gn,
                       gf=gf)


def make_callback_data_buy(platform="0", make="0", model="0", code="0", gn="0", gf="0", cn="0"):
    return buy_item.new(platform=platform, make=make, model=model, code=code, gn=gn, gf=gf, cn=cn)


def update_data(user_id: str, data: str):
    cache.lpush(f'u{user_id}', data)


def delete_data(user_id: str, data: str):
    cache.lrem(f'u{user_id}', 0, data[0])


def liststring(dict: dict):
    massege = list()
    for k in dict:
        massege.append(f'Price {k.get("cena")} VIN CODE {k.get("vin")}\n')
    str1 = " "

    return (str1.join(massege))


async def get_data_ids(user_id: str) -> list:
    data = cache.lrange(f'u{user_id}', 0, -1)
    return data

async def platform():

    CURRENT_LEVEL = 0
    markup = InlineKeyboardMarkup()

    categories = PLAT
    for platform in categories:
        button_text = PLAT[platform]
        callback_data = make_callback_data(level=CURRENT_LEVEL + 1, platform=platform)

        markup.insert(
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        )
    return markup


async def make(platform):
    CURRENT_LEVEL = 1
    markup = InlineKeyboardMarkup(row_width=2)

    subcategories = MANHEIM_MAKE
    for id, make in subcategories.items():
        button_text = make
        callback_data = make_callback_data(level=CURRENT_LEVEL + 1,
                                           platform=platform, make=f'{make}', code=f'{id}')
        markup.insert(
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        )
    markup.row(
        InlineKeyboardButton(
            text=msg.back,
            callback_data=make_callback_data(level=CURRENT_LEVEL - 1))
    )
    return markup


async def model(platform, make, code, **kwargs):
    CURRENT_LEVEL = 2
    markup = InlineKeyboardMarkup(row_width=2)
    if int(platform) == 0:
        read_dict = r.get(make)
        yourdict = pickle.loads(read_dict)
        items = yourdict
        for item in items:
            button_text = items[item]
            callback_data = make_callback_data(level=CURRENT_LEVEL + 1,
                                               platform=platform, make=make,
                                               model=item,
                                               code=code)
            markup.insert(
                InlineKeyboardButton(
                    text=button_text, callback_data=callback_data)
            )
        markup.row(
            InlineKeyboardButton(
                text=msg.back,
                callback_data=make_callback_data(level=CURRENT_LEVEL - 1,
                                                 platform=platform))
        )

    else:
        read_dict = r.get(f'Copart_{make}')
        yourdict = pickle.loads(read_dict)

        for item in yourdict:
            button_text = item
            callback_data = make_callback_data(level=CURRENT_LEVEL + 1,
                                               platform=platform, make=make,
                                               model=button_text,
                                               code=code)
            markup.insert(
                InlineKeyboardButton(
                    text=button_text, callback_data=callback_data)
            )
        markup.row(
            InlineKeyboardButton(
                text=msg.back,
                callback_data=make_callback_data(level=CURRENT_LEVEL - 1,
                                                 platform=platform))
        )
    return markup


async def god_start(platform, make, model, code):
    CURRENT_LEVEL = 3
    markup = InlineKeyboardMarkup()
    for i in range(2000, 2022):
        button_text = i

        callback_data = make_callback_data(level=CURRENT_LEVEL + 1,
                                           platform=platform,
                                           make=make,
                                           model=model,
                                           code=code,
                                           gn=f'{i}')
        markup.insert(
            InlineKeyboardButton(
                text=f'{i}', callback_data=callback_data)
        )
    markup.row(
        InlineKeyboardButton(
            text=msg.back,
            callback_data=make_callback_data(level=CURRENT_LEVEL - 1,
                                             platform=platform,
                                             make=make,
                                             code=code))
    )

    return markup


async def god_fin(platform, make, model, code, gn):
    CURRENT_LEVEL = 4
    markup = InlineKeyboardMarkup()

    for i in range(int(gn), int(gn) + 3):
        button_text = i
        callback_data = make_callback_data(level=CURRENT_LEVEL + 1,
                                           platform=platform, make=make,
                                           model=model,
                                           code=code,
                                           gn=gn,
                                           gf=f'{i}')
        markup.insert(
            InlineKeyboardButton(
                text=f'{i}', callback_data=callback_data)
        )
    markup.row(
        InlineKeyboardButton(
            text=msg.back,
            callback_data=make_callback_data(level=CURRENT_LEVEL - 1,
                                             platform=platform,
                                             make=make,
                                             model=model,
                                             code=code,
                                             gn=gn))
    )

    return markup




async def verifi(platform, make, level, model, code, gn, gf, cn, **kwargs):
    CURRENT_LEVEL = int(level)
    markup = InlineKeyboardMarkup()
    markup.insert(
        InlineKeyboardButton(
            text=msg.back,

            callback_data=make_callback_data(level=CURRENT_LEVEL - 1,
                                             platform=platform,
                                             make=make,
                                             model=model,
                                             code=code,
                                             gn=gn,
                                             gf=gf)

        ))
    markup.insert(
        InlineKeyboardButton(
            text=msg.buy,

            callback_data=make_callback_data_buy(platform=platform,
                                                 make=make,
                                                 model=model,
                                                 code=code,
                                                 gn=gn,
                                                 gf=gf,
                                                 cn=cn))

    )
    return markup


