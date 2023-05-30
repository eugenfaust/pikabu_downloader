from aiogram.types.chat_action import ChatAction
from aiogram import Router, F
from aiogram.filters import Command
from .help import bot_help
from .start import pikabu_link_handler, gif_handler


def setup():
    router = Router()
    router.message.register(bot_help, Command("help", "start"))
    router.message.register(gif_handler, F.text.endswith('.gif'))
    router.message.register(pikabu_link_handler, F.text.contains('https://pikabu.ru/'),
                            flags={'throttling_key': "pikabu_link"})
    return router
