import asyncio

from utils.link_validation import check_pikabu_link
from utils.rabbit_producer import send_parse_request
from aiogram import types, Bot, Dispatcher, flags


async def gif_handler(msg: types.Message, bot: Bot):
    try:
        await msg.answer_document(msg.text)
        await bot.send_document(bot.__getattribute__('channel_id'), msg.text)
        if msg.chat.type != 'private':
            try:
                await msg.delete()
            except:
                pass
    except:
        pass


async def pikabu_link_handler(msg: types.Message, bot: Bot):
    link = check_pikabu_link(msg.text)
    if not link:
        return
    resp = await msg.answer('✅ Загружаем...')
    info = {'uid': msg.from_user.id, 'link': link, 'msg_id': resp.message_id, 'chat_type': msg.chat.type,
            'chat_id': msg.chat.id, 'chat_msg_id': msg.message_id}
    await send_parse_request(bot, info)