import logging

from aiogram import types

from keyboards.inline.menu import get_menu
from models.users import User


async def bot_start(msg: types.Message, user: User):
    await msg.answer(f'Привет, {user.full_name}!', reply_markup=get_menu())


async def clb_start(clb: types.CallbackQuery, user: User):
    await clb.answer()
    await clb.message.delete()
    await clb.message.answer(f'Привет, {user.full_name}!', reply_markup=get_menu())