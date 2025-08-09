from aiogram.filters.callback_data import CallbackData

class ConfigCallbackFactory(CallbackData, prefix="config"):
    action: str
    config_id: int

