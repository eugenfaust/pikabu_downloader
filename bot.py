from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.fsm.storage.memory import MemoryStorage

import config
from handlers import errors
from handlers import user
from middlewares.user_logging import UserLoggingMiddleware

session = AiohttpSession()
bot_settings = {"session": session, "parse_mode": "HTML"}
ai_bot = Bot(token=config.MAIN_BOT_TOKEN, **bot_settings)
# storage = RedisStorage.from_url(REDIS_DSN, key_builder=DefaultKeyBuilder(with_bot_id=True))
storage = MemoryStorage()

main_dispatcher = Dispatcher(storage=storage)
# middlewares
main_dispatcher.message.middleware(UserLoggingMiddleware())
main_dispatcher.callback_query.middleware(UserLoggingMiddleware())

# routers
main_dispatcher.include_router(errors.setup())
main_dispatcher.include_router(user.setup())
