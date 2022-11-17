import re

import aiohttp
from aiogram import types

import config


async def gif_handler(msg: types.Message, bot):
    try:
        await msg.answer_document(msg.text)
        if msg.chat.type != 'private':
            try:
                await msg.delete()
            except:
                pass
    except:
        pass


async def pikabu_link_handler(msg: types.Message, bot):

    try:
        link = re.search('https:\/\/pikabu.ru(.*)', msg.text).group().strip()
    except Exception as e:
        await bot.send_message(config.ADMIN_IDS[0], 'Error in link:\n{}\n{}'.format(msg.text, e))
        return
    headers = {
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}
    res = None
    s = aiohttp.ClientSession()
    try:
        response = await s.get(link, headers=headers)
        html = await response.text()
        res = re.search('<div class="player" data-type="video-file" data-size-type="story" data-source="(.*)" data-vid="',
                    html).group(1)
    except Exception as e:
        await bot.send_message(config.ADMIN_IDS[0], 'Error in link:\n{}\n{}\nDidn\'t found video link'.format(msg.text, e))
    finally:
        await s.close()
    if res:
        await msg.answer_video(res + '.mp4', caption='<a href="{}">Pikabu пост</a>'.format(link))
        if msg.chat.type != 'private':
            try:
                await msg.delete()
            except:
                pass