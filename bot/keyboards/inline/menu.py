from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_menu() -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text='Hello', callback_data='hello'))
    builder.add(types.InlineKeyboardButton(text='Bye', callback_data='bye'))
    builder.add(types.InlineKeyboardButton(text='hi', callback_data='hi'))
    builder.row()
    return builder.as_markup()