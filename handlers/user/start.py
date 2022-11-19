import re
import traceback

import aiohttp
from aiogram import types
from aiogram.types import URLInputFile, InputMediaPhoto

import config
from parser.pikabu import PikabuParser


async def gif_handler(msg: types.Message, bot):
    try:
        await msg.answer_document(msg.text)
        await bot.send_document(config.CHANNEL_ID, msg.text)
        if msg.chat.type != 'private':
            try:
                await msg.delete()
            except:
                pass
    except:
        pass


async def pikabu_link_handler(msg: types.Message, bot):
    try:
        # Formatted string used for regex with whitespace. Without this regex can be failed if link in end of string
        link = re.search('https:\/\/pikabu.ru(.*) ', f'{msg.text} ').group().strip()
    except Exception as e:
        await bot.send_message(config.ADMIN_IDS[0], 'Error in link:\n{}\n{}'.format(msg.text, e))
        return
    try:
        pikabu = PikabuParser(link)
        title = await pikabu.parse_title()
        video, file_size, duration = await pikabu.parse_video()
        images = await pikabu.parse_images()
        caption = '<a href="{}">{}</a>'.format(link, title)
        if msg.chat.type != 'private':
            try:
                await msg.delete()
            except:
                pass
        if images:
            if len(images) > 1:
                media_groups = []
                temp_group = []
                counter = 0
                for img in images:
                    temp_group.append(InputMediaPhoto(media=img, caption=caption))
                    counter += 1
                    if counter >= 10:
                        counter = 0
                        media_groups.append(temp_group)
                        temp_group = []
                media_groups.append(temp_group)
                for media in media_groups:
                    await msg.answer_media_group(media)
            else:
                await msg.answer_photo(images[0], caption=caption)
        if not video:
            return
        try:
            if 50_000_000 >= file_size >= 20_000_000:  # 20 MB by link limit, 50 MB upload limit
                input_file = URLInputFile(video)
                sent = await msg.answer_video(input_file, caption=caption,
                                              duration=duration)
            elif file_size >= 50_000_000:
                return
            else:
                sent = await msg.answer_video(video,
                                              caption=caption)
            await bot.send_video(config.CHANNEL_ID, sent.video.file_id,
                                 caption=caption)
        except Exception as e:
            await bot.send_message(config.ADMIN_IDS[0],
                                   'Error in link:\n{}\n{}\nCan\'t upload video'.format(video, e))
    except Exception as e:
        traceback.print_exception(e)
        print(e)
        await bot.send_message(config.ADMIN_IDS[0], e)
