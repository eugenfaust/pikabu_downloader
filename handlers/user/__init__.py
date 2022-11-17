from aiogram import Router, F
from .help import bot_help
from .start import pikabu_link_handler, gif_handler


def setup():
    router = Router()
    router.message.register(gif_handler, F.text.endswith('.gif'))
    router.message.register(pikabu_link_handler, F.text.contains('https://pikabu.ru/'))
    return router
