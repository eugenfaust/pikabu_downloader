import asyncio
import json
import logging
from types import SimpleNamespace

from aiogram.exceptions import TelegramBadRequest
from aiogram.types import InputMediaPhoto, URLInputFile
from aiormq import AMQPConnectionError
from sentry_sdk import capture_exception
import sentry_sdk
from aio_pika import connect
from aio_pika.abc import AbstractIncomingMessage

from config import load_config
from aiogram import Bot
from parser.pikabu import PikabuParser

cfg = load_config()
bot = Bot(cfg.token, parse_mode='HTML')
Bot.set_current(bot)


async def on_message(message: AbstractIncomingMessage) -> None:
    logging.info(" [x] Received message %r" % message)
    request = json.loads(message.body, object_hook=lambda d: SimpleNamespace(**d))
    try:
        pikabu = PikabuParser(request.link)
        if not await pikabu.load_content():
            await message.ack()
            await bot.edit_message_text("❌ Бот временно не работает. Работаем над этой проблемой", request.chat_id,
                                        request.msg_id)
            return
        title = await pikabu.parse_title()
        video, file_size, duration = await pikabu.parse_video()
        images = await pikabu.parse_images()
        caption = '<a href="{}">{}</a>'.format(request.link, title)
        if request.chat_type != 'private':
            try:
                await bot.delete_message(request.chat_id, request.chat_msg_id)
            except:
                pass
        if images:
            if len(images) > 1:
                media_groups = []
                temp_group = []
                counter = 0
                for img in images:
                    temp_group.append(InputMediaPhoto(media=URLInputFile(img), caption=caption))
                    counter += 1
                    if counter >= 10:
                        counter = 0
                        media_groups.append(temp_group)
                        temp_group = []
                media_groups.append(temp_group)
                for media in media_groups:
                    await bot.send_media_group(request.chat_id, media)
            else:
                await bot.send_photo(request.chat_id, URLInputFile(images[0]), caption=caption)
        if not video:
            await message.ack()
            return
        try:
            if 50_000_000 >= file_size >= 20_000_000:  # 20 MB by link limit, 50 MB upload limit
                input_file = URLInputFile(video)
                sent = await bot.send_video(request.chat_id, input_file, caption=caption,
                                            duration=duration)
            elif file_size >= 50_000_000:
                await bot.send_message(cfg.admin_id, 'Video size limit: {}'.format(request.link))
                await message.ack()
                return
            else:
                try:
                    sent = await bot.send_video(request.chat_id, video,
                                                caption=caption)
                except TelegramBadRequest as e:  # Some videos with bad width/height can't be uploaded
                    sent = await bot.send_video(request.chat_id, URLInputFile(video), caption=caption)
            if sent.video:
                await bot.send_video(cfg.channel_id, sent.video.file_id,
                                     caption=caption)
            else:
                await bot.send_document(cfg.channel_id, sent.document.file_id, caption=caption)
        except Exception as e:
            capture_exception(e)
            await bot.send_message(cfg.admin_id,
                                   'Error in link:\n{}\n{}\nCan\'t upload video'.format(video, e))
    except Exception as e:
        capture_exception(e)
        await bot.send_message(cfg.admin_id, 'Pikabu handler error: {}'.format(e))
    await bot.delete_message(request.chat_id, request.msg_id)
    await message.ack()


async def main() -> None:
    sentry_sdk.init(
        dsn=cfg.sentry_dsn,
        traces_sample_rate=1.0,
    )
    while True:
        try:
            connection = await connect(f"amqp://{cfg.rabbit.user}:{cfg.rabbit.password}@{cfg.rabbit.host}/")
            break
        except AMQPConnectionError:
            logging.info("Trying connect to rabbit...")
            await asyncio.sleep(1)
    async with connection:
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=10)
        queue = await channel.declare_queue("link_parser")
        await queue.consume(on_message, no_ack=False)
        logging.info(" [*] Waiting for messages. To exit press CTRL+C")
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
