from aiogram import Bot, Dispatcher
from aiogram.dispatcher.webhook.aiohttp_server import (
    SimpleRequestHandler,
    setup_application,
)
from aiohttp import web

import config
from bot import main_dispatcher, ai_bot
from models.base import start_db, shutdown_db


async def on_startup(dispatcher: Dispatcher, bot: Bot):
    await start_db()
    await bot.set_webhook(f"{config.BASE_URL}{config.MAIN_BOT_PATH}")


async def on_shutdown(dispatcher: Dispatcher, bot: Bot):
    await shutdown_db()


if __name__ == "__main__":
    main_dispatcher.startup.register(on_startup)
    main_dispatcher.shutdown.register(on_shutdown)
    app = web.Application()
    SimpleRequestHandler(dispatcher=main_dispatcher, bot=ai_bot).register(app, path=config.MAIN_BOT_PATH)
    setup_application(app, main_dispatcher, bot=ai_bot)
    web.run_app(app, host=config.WEB_SERVER_HOST, port=config.WEB_SERVER_PORT)
