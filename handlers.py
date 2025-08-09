import asyncio
import logging

from aiogram import F
from aiogram import Dispatcher, types
from aiogram.types import ReplyKeyboardRemove
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext


from middleware import CheckAdminMiddleware
from keyboards import (keyboard_menu,
                       get_inline_keyboard_configs,
                       get_keyboard_cancel,
                       get_inline_keyboard_config)
from fabrics import ConfigCallbackFactory
from fsm import ClientConfigState
from db import Db, Config

logging.basicConfig(level=logging.INFO)


dp = Dispatcher()
db = Db()

@dp.message(Command("start"))
async def cmd_start(
        message: types.Message,
        is_auth: bool
):
    print(is_auth)
    await message.answer("Здравствуйте, вы в админ панели vpn сервера.", reply_markup=keyboard_menu)




def create_ans(conf: Config):
    return f"""
    Информация по клиенту
    ---------------
    ID: {conf.id}
    File ID: {conf.file_id}
    File Name: {conf.file_name}
    ---------------
    Клиент: {conf.client_name}
    Статус: {"Активный" if conf.is_active else "НЕактивный"}
    """


@dp.callback_query(ConfigCallbackFactory.filter())
async def callbacks_client_config(
        callback: types.CallbackQuery,
        callback_data: ConfigCallbackFactory
):
    # TODO дописать конфиги

    match callback_data.action:

        case "get":
            conf = db.get_config(id_=callback_data.config_id)

            await callback.message.edit_text(
                text=create_ans(conf),
                reply_markup=get_inline_keyboard_config(conf)
            )

        case "delete":
            db.delete_config(callback_data.config_id)
            await callback.message.answer("Конфиг успешно удален!")

            await callback.message.edit_text(
                text="Здравствуйте, вы в админ панели vpn сервера.",
                reply_markup=keyboard_menu
            )
        case "download":
            ...

        case "switch_off":
            ...
        case "switch_on":
            ...


    await callback.answer()



@dp.callback_query(lambda f: f.data in ["list_config", "back_to_configs"])
async def callback_list_config(
        callback: types.CallbackQuery,
        state: FSMContext
):
    confs = db.all_configs()
    await callback.message.edit_text(
        text="Все конфиги:",
        reply_markup=get_inline_keyboard_configs(confs)
    )



@dp.callback_query(lambda f: f.data in ["back_to_panel", ])
async def callback_back_to_panel(
        callback: types.CallbackQuery,
):
    await callback.message.edit_text(
        text="Здравствуйте, вы в админ панели vpn сервера.",
        reply_markup=keyboard_menu
    )


@dp.callback_query(F.data == "create_config")
async def callback_create_config(
        callback: types.CallbackQuery,
        state: FSMContext
):
    if db.count_config() == 10:
        await callback.message.answer(
            text="Количество конфигов не может быть больше 10."
        )
        await callback.answer()
        return



    await callback.message.answer(
        text="Введите имя клиента:",
        reply_markup=get_keyboard_cancel()
    )
    await callback.answer()
    await state.set_state(ClientConfigState.choosing_name_client)


@dp.message(
    F.text.in_(["Отменить"]),
    StateFilter(ClientConfigState.choosing_name_client)
)
async def cancel(
        msg: types.Message,
        state: FSMContext
):

    await msg.answer(
        "Вы успешно отменили создание конфига",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.clear()





@dp.message(
    StateFilter(ClientConfigState.choosing_name_client)
)
async def config_create(
        msg: types.Message,
        state: FSMContext
):

    db.create_config(msg.text)

    await msg.answer(
        f"Вы успешно создали конфиг {msg.text}",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.clear()



dp.update.middleware(CheckAdminMiddleware())
dp.callback_query.middleware(CheckAdminMiddleware())






