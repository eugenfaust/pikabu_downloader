import logging

import aiohttp
from aiogram import types
import re

import config
from keyboards.inline.menu import get_menu


async def pikabu_link_handler(msg: types.Message, bot):
    s = aiohttp.ClientSession()
    try:
        link = re.search('https:\/\/pikabu.ru(.*)', msg.text).group().strip()
    except Exception as e:
        await bot.send_message(config.ADMIN_IDS[0], 'Error in link:\n{}\n{}'.format(msg.text, e))
        await s.close()
        return
    headers = {
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}
    res = None
    try:
        response = await s.get(link, headers=headers)
        print(link)
        html = await response.text()
        print(html)
        res = re.search('<div class="player" data-type="video-file" data-size-type="story" data-source="(.*)" data-vid="',
                    html).group(1)
    except Exception as e:
        await bot.send_message(config.ADMIN_IDS[0], 'Error in link:\n{}\n{}\nDidn\'t found video link'.format(msg.text, e))
    if res:
        await msg.answer_video(res + '.mp4')
    await s.close()
