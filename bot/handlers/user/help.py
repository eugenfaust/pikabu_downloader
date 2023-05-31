from aiogram import types
from aiogram.types import InputMediaPhoto, URLInputFile


async def bot_help(msg: types.Message):
    text = [
        'Список команд: ',
        '/start - Начать диалог',
        '/help - Получить справку'
    ]
    await msg.answer('\n'.join(text))

