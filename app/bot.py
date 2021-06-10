import asyncio
import pickle
import config
import app.service as s
from database import r
from config import TOKEN
from typing import Union
from app.dialogs import msg
from app import parser, copart
from aiogram import Bot, types
from aiogram.types import CallbackQuery, Message
from concurrent.futures import ThreadPoolExecutor
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.middlewares.logging import LoggingMiddleware





loop = asyncio.get_event_loop()
bot = Bot(TOKEN, loop=loop)
storage1 = MemoryStorage()
dp = Dispatcher(bot, storage=storage1)
dp.middleware.setup(LoggingMiddleware())
exucutr = ThreadPoolExecutor(max_workers=1)


class OrderFood(StatesGroup):
    platform = State()

@dp.message_handler(commands=['start'])
async def show_menu(message: types.Message):
    await platform_list(message)

async def platform_list(message: Union[CallbackQuery, Message], **kwargs):
    markup = await s.platform()

    if isinstance(message, Message):
        await message.answer(msg.plat, reply_markup=markup)

    elif isinstance(message, CallbackQuery):
        call = message
        await call.message.edit_text(text=msg.plat, reply_markup=markup)


#
async def make_list(callback: CallbackQuery, platform, **kwargs):
    markup = await s.make(platform)
    await callback.message.edit_text(text=msg.make, reply_markup=markup)



async def model_list(callback: CallbackQuery, platform, make, code, **kwargs):
    markup = await s.model(platform, make, code)
    await callback.message.edit_text(text=msg.model, reply_markup=markup)


async def god_auto_nan(callback: CallbackQuery, platform, make, model, code, **kwargs):
    markup = await s.god_start(platform, make, model, code)
    await callback.message.edit_text(text=msg.entergd, reply_markup=markup)


async def god_auto_fin(callback: CallbackQuery, platform, make, model, code, gn, **kwargs):
    markup = await s.god_fin(platform, make, model, code, gn)
    await callback.message.edit_text(text=msg.inpgod, reply_markup=markup)


@dp.message_handler(state=OrderFood.platform)
async def fin(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        u = await s.get_data_ids(message.from_user.id)
        await state.finish()
        cat = u[0].split(":")[2]
        def mod(cat):
            if int(cat) == 0:
                mod = u[0].split(":")[3]
                read_dict = r.get(mod)
                yourdict = pickle.loads(read_dict)
                make = yourdict[u[0].split(":")[4]]
                return make
            else:
                make = u[0].split(":")[4]
                return make
        make = mod(cat)
        keybord = await s.verifi(platform=u[0].split(":")[2], make=u[0].split(":")[3], level=u[0].split(":")[1],
                                 model=u[0].split(":")[4], code=u[0].split(":")[5], gn=u[0].split(":")[6],
                                 gf=u[0].split(":")[7], cn=message.text)

        await bot.send_message(message.from_user.id, text=f' {msg.edit}\n'
                                                          f' Сайт {config.PLAT[u[0].split(":")[2]]}\n'
                                                          f' Марка: {u[0].split(":")[3]}\n'
                                                          f' Модель: {make}\n'
                                                          f' Год с {u[0].split(":")[6]}\n'
                                                          f' по {u[0].split(":")[7]}\n'
                                                           f' C ценой ниже {message.text} $', reply_markup=keybord)
        print(u)
        s.delete_data(message.from_user.id, u)
    else:
        await bot.send_message(message.from_user.id, text=msg.errcena)
    # await s.delete_data(message.from_user.id, u)


async def cena_auto(callback: CallbackQuery, **kwargs):
    s.update_data(callback.from_user.id, callback.data)
    await callback.message.edit_text(text=msg.cen)
    await OrderFood.platform.set()

@dp.callback_query_handler(s.menu_cd.filter())
async def navigate(call: CallbackQuery, callback_data: dict):
    current_level = callback_data.get("level")
    code = callback_data.get("code")
    gn = callback_data.get("gn")
    gf = callback_data.get("gf")
    cn = callback_data.get("cn")
    platform = callback_data.get("platform")
    make = callback_data.get("make")
    model = callback_data.get("model")


    levels = {
        "0": platform_list,  # Платформа (Copart or Manheim)
        "1": make_list,      # Модели Авто
        "2": model_list,     # Марка Авто
        "3": god_auto_nan,   # С какого года авто
        "4": god_auto_fin,   # По какой год авто
        "5": cena_auto,      # Цена авто

    }


    current_level_function = levels[current_level]
    await current_level_function(
        call,
        platform=platform,
        make=make,
        model=model,
        code=code,
        gn=gn,
        gf=gf,
        cn=cn
    )


@dp.callback_query_handler(s.buy_item.filter())
async def otch(call: CallbackQuery, callback_data: dict):
    await call.message.edit_text(text=msg.otch)
    if int(callback_data.get("platform")) == 0:
        loop = asyncio.get_event_loop()
        end_time = loop.time() + 604800
        while True:
            _instance = parser.Man(callback_data.get("cn"), callback_data.get("gf"), callback_data.get("gn")
                                  , int(callback_data.get("model")), callback_data.get("code"))
            now = asyncio.create_task(coro=_instance.get_registr())
            x = s.liststring(await now)
            mod = callback_data.get("make")
            read_dict = r.get(mod)
            yourdict = pickle.loads(read_dict)
            make = yourdict[callback_data.get("model")]

            if now == [] or now == ['auto=0']:
                await bot.send_message(call.from_user.id, text=f'{msg.otchpod} '
                                                               f'{config.PLAT[callback_data.get("platform")]} '
                                                               f'{callback_data.get("make")} {make}'" c"
                                                               f'{callback_data.get("gn")}{msg.god_po}'
                                                               f'{callback_data.get("gf")}{msg.god_do}'
                                                               f'{callback_data.get("cn")}'"$"
                                                               f'\n {msg.no_res}')
            else:
                await bot.send_message(call.from_user.id, text=f'{msg.otchpod} '
                                                               f'{config.PLAT[callback_data.get("platform")]} '
                                                               f'{callback_data.get("make")} {make}'" c "
                                                               f'{callback_data.get("gn")}{msg.god_po}'
                                                               f'{callback_data.get("gf")}{msg.god_do}'
                                                               f'{callback_data.get("cn")}'"$"
                                                               f'\n{x}')
            if (loop.time() + 1.0) >= end_time:
                break
            await asyncio.sleep(300)
    else:
        loop = asyncio.get_event_loop()
        end_time = loop.time() + 604800
        while True:
            _instance = copart.Copart(callback_data.get("cn"), callback_data.get("gn"), callback_data.get("gf"),
                                    callback_data.get("make"), callback_data.get("model"))
            task1 = asyncio.create_task(coro=_instance.coro())
            now = await task1
            if now == None:
                await bot.send_message(call.from_user.id, text=f'{msg.otchpod} '
                                                               f'{config.PLAT[callback_data.get("platform")]} '
                                                               f' {callback_data.get("make")} {callback_data.get("model")}'" c"
                                                               f' {callback_data.get("gn")} {msg.god_po} '
                                                               f' {callback_data.get("gf")}{msg.god_do}'
                                                               f'{callback_data.get("cn")}'"$"
                                                               f'\n {msg.no_res}')
            else:
                if len(now) > 4096:
                    for x in range(0, len(now), 3800):
                        await bot.send_message(call.from_user.id, text=f'{msg.otchpod} '
                                                               f' {config.PLAT[callback_data.get("platform")]} '
                                                               f' {callback_data.get("make")} {callback_data.get("model")} c '
                                                               f' {callback_data.get("gn")}{msg.god_po}'
                                                               f' {callback_data.get("gf")}{msg.god_do}'
                                                               f'{callback_data.get("cn")}'"$"
                                                               f'\n{now[x:x + 3800]}')
                else:
                    await bot.send_message(call.from_user.id, text=f'{msg.otchpod} '
                                                                   f' {config.PLAT[callback_data.get("platform")]} '
                                                                   f' {callback_data.get("make")} {callback_data.get("model")} c '
                                                                   f' {callback_data.get("gn")}{msg.god_po}'
                                                                   f' {callback_data.get("gf")}{msg.god_do}'
                                                                   f'{callback_data.get("cn")}'"$"
                                                                   f'\n{now}')

            now = ""
            if (loop.time() + 1.0) >= end_time:
                break
            await asyncio.sleep(300)


@dp.message_handler(commands=['help'])
async def help(message: types.Message):
    await message.answer(msg.help)

@dp.message_handler()
async def unknown_message(message: types.Message):
    await message.answer(msg.start)
