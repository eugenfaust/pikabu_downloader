from aiogram import Router, F
from .help import bot_help
from .start import pikabu_link_handler


def setup():
    router = Router()
    router.message.register(pikabu_link_handler, F.text.contains('https://pikabu.ru/'))
    return router
