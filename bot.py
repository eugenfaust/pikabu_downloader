from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.fsm.storage.memory import MemoryStorage

from config import load_config
from handlers import errors
from handlers import user

cfg = load_config()
session = AiohttpSession()
bot_settings = {"session": session, "parse_mode": "HTML"}
bot = Bot(token=cfg.token, **bot_settings)
bot.__setattr__('admin_id', cfg.admin_id)
bot.__setattr__('channel_id', cfg.channel_id)
storage = MemoryStorage()

main_dispatcher = Dispatcher(storage=storage)

# routers
main_dispatcher.include_router(errors.setup())
main_dispatcher.include_router(user.setup())
