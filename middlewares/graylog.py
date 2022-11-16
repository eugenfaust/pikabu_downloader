import logging
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message
import graypy


class GrayLogMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        self.DOMAIN = 'example.graylog.dev'
        self.PORT = 12201
        self.logger = logging.getLogger('aiogram_logger')
        self.logger.setLevel(logging.DEBUG)

        handler = graypy.GELFUDPHandler(self.DOMAIN, self.PORT)
        self.logger.addHandler(handler)
        self.logger.debug('Hello Graylog.')

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        self.logger.debug('Got msg: {}'.format(event))
        result = None
        try:
            result = await handler(event, data)
        except Exception as e:
            self.logger.exception('Error on handler: {}\n'
                                  'Data: {}'.format(event, data))
        return result
