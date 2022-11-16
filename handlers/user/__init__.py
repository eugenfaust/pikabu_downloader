from aiogram import Router, F
from aiogram.filters import Command

from filters import AdminFilter
from .help import bot_help
from .start import bot_start, clb_start


def setup():
    router = Router()
    router.message.register(bot_start, Command(commands='start'))
    router.message.register(bot_help, Command(commands='help'))
    router.callback_query.register(clb_start, F.data == 'hello', AdminFilter())
    return router
