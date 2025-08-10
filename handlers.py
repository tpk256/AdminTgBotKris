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
                       get_inline_keyboard_config,
                       get_inline_keyboard_delete_choice
                       )
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
    if not is_auth:
        await message.answer("Access Denied!")
        return
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
        callback_data: ConfigCallbackFactory,
        is_auth: bool
):
    if not is_auth:
        await callback.answer("Access Denied!")
        return
    # TODO дописать конфиги

    match callback_data.action:

        case "get":
            conf = db.get_config(id_=callback_data.config_id)

            await callback.message.edit_text(
                text=create_ans(conf),
                reply_markup=get_inline_keyboard_config(conf)
            )

        case "pre_delete":
            conf = db.get_config(callback_data.config_id)
            await callback.message.edit_text(
                text=f"Вы уверены, что хотите удалить конфиг: {conf.client_name} ?",
                reply_markup=get_inline_keyboard_delete_choice(conf.id)
            )

        case "accept_delete":
            conf = db.get_config(callback_data.config_id)
            db.delete_config(conf)
            await callback.message.answer(f"Вы успешно удалили конфиг: {conf.client_name}.")
            await callback.message.edit_text(
                text=f"Здравствуйте, вы в админ панели vpn сервера.",
                reply_markup=keyboard_menu
            )

        case "cancel_delete":
            await callback.message.edit_text(
                text=f"Здравствуйте, вы в админ панели vpn сервера.",
                reply_markup=keyboard_menu
            )
        case "download":
            conf = db.get_config(id_=callback_data.config_id)
            await callback.message.answer_document(
                document=conf.file_id
            )

        case "switch_off":
            ...
        case "switch_on":
            ...


    await callback.answer()



@dp.callback_query(lambda f: f.data in ["list_config", "back_to_configs"])
async def callback_list_config(
        callback: types.CallbackQuery,
        state: FSMContext,
        is_auth: bool
):
    if not is_auth:
        await callback.answer("Access Denied!")
        return
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



@dp.callback_query(F.data == "help")
async def callback_help(
        callback: types.CallbackQuery,
        state: FSMContext,
        is_auth: bool
):
    if not is_auth:
        await callback.answer("Access Denied!")
        return

    await callback.message.answer(
        text="Я верю, что ты Сыльная незавимая!",
    )
    await callback.answer()




@dp.callback_query(F.data == "create_config")
async def callback_create_config(
        callback: types.CallbackQuery,
        state: FSMContext,
        is_auth: bool
):
    if not is_auth:
        await callback.answer("Access Denied!")
        return

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
        state: FSMContext,
        is_auth: bool
):
    if not is_auth:
        await msg.answer("Access Denied!")
        return

    await db.create_config(msg.text, chat_id=msg.chat.id)

    await msg.answer(
        f"Вы успешно создали конфиг {msg.text}",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.clear()



dp.update.middleware(CheckAdminMiddleware())
dp.callback_query.middleware(CheckAdminMiddleware())






