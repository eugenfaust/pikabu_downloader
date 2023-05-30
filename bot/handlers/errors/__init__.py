import logging
import traceback
from typing import Any

from aiogram import Router
from aiogram.handlers import ErrorHandler
from sentry_sdk import capture_exception

def setup():
    router = Router()
    router.errors.register(MyHandler)
    return router


class MyHandler(ErrorHandler):
    async def handle(self) -> Any:
        try:
            response = capture_exception(self.event)
            username = self.data['event_from_user'].username
            await self.bot.send_message(self.bot.__getattribute__('admin_id'),
                                        f'<pre><code class="language-python">{traceback.format_exc()}</code></pre>'
                                        f"\n\nFrom: ({f'@{username}' if username else self.data['event_from_user'].full_name}) "
                                        f"<code>{self.data['event_from_user'].id}</code>\n{response}")

        except Exception as e:
            logging.exception(e)
            # Add here logging to file/logging system
            pass
