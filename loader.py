from aiogram.types import FSInputFile
from aiogram import Bot


class SingleBot:
    bot: Bot = None

async def load_file(path, filename, chat_id: int) -> str:
    conf = FSInputFile(path)
    data = await SingleBot.bot.send_document(
        chat_id=chat_id,
        document=conf
    )
    return data.document.file_id

