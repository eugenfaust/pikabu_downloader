from aiogram import Bot, Dispatcher

from bot import main_dispatcher, ai_bot
import config


if __name__ == "__main__":
    main_dispatcher.run_polling(ai_bot)
