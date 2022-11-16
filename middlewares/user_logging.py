import datetime
import logging
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware, Bot
from aiogram.types import Message
from aiogram.dispatcher.dispatcher import Dispatcher

from models.users import User


class UserLoggingMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        pass

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        db_session = data['bot'].__getattribute__('db')
        async with db_session() as session:
            user: User = await session.get(User, event.from_user.id)
            now = datetime.datetime.now()
            if not user:
                user = User(id=event.from_user.id, full_name=event.from_user.full_name,
                            username=event.from_user.username, created=now, last_action=now)
                session.add(user)
            else:
                user.last_action = now
            await session.commit()
        data['user'] = user
        data['db_session'] = db_session
        result = await handler(event, data)
        return result
