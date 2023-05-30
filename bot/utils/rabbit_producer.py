import json

import sentry_sdk
from aio_pika import connect, Message
from aiogram import Bot


async def send_parse_request(bot: Bot, chat_info: dict) -> bool:
    try:
        connection = await connect(bot.__getattribute__('rabbit_url'))
    except Exception as e:
        sentry_sdk.capture_exception(e)
        return False
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue('link_parser')
        await channel.default_exchange.publish(
            Message(json.dumps(chat_info).encode('utf-8')),
            routing_key=queue.name,
        )
        return True
