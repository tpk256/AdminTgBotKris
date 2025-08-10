from aiogram.utils.keyboard import InlineKeyboardBuilder, KeyboardBuilder
from aiogram.types import InlineKeyboardButton, KeyboardButton

from fabrics import ConfigCallbackFactory
from db import Config



def get_inline_keyboard_menu():
    builder = InlineKeyboardBuilder()

    data = [
        [("Конфиги", "list_config")],
        [("Создать конфиг", "create_config"), ("Обратиться в помощь", "help")],

    ]

    for row in data:
        builder.row(*(
            InlineKeyboardButton(
                text=text,
                callback_data=callback_data) for text, callback_data in row

            )
        )


    return builder.as_markup()



def get_keyboard_cancel():
    builder = KeyboardBuilder(KeyboardButton)
    builder.add(KeyboardButton(text='Отменить'))

    return builder.as_markup()



def get_inline_keyboard_config(conf: Config):

    builder = InlineKeyboardBuilder()

    builder.button(text="Скачать", callback_data=ConfigCallbackFactory(action="download", config_id=conf.id))
    builder.button(text="Удалить", callback_data=ConfigCallbackFactory(action="pre_delete", config_id=conf.id))
    builder.button(text="Вернуться к конфигам", callback_data="back_to_configs")

    builder.adjust(2)

    return builder.as_markup()



def get_inline_keyboard_configs(confs: list[Config]):
    builder = InlineKeyboardBuilder()

    for conf in confs:
        builder.button(
                text=conf.client_name,
                callback_data=ConfigCallbackFactory(action='get', config_id=conf.id)
        )


    builder.button(
        text="Вернуться к админ панели",
        callback_data="back_to_panel"
    )
    builder.adjust(1)
    return builder.as_markup()



def get_inline_keyboard_delete_choice(id: int):
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Да",
        callback_data=ConfigCallbackFactory(action='accept_delete', config_id=id)
    )
    builder.button(
        text="Нет",
        callback_data=ConfigCallbackFactory(action='cancel_delete', config_id=id)
    )

    builder.adjust(2)
    return builder.as_markup()


keyboard_menu = get_inline_keyboard_menu()

