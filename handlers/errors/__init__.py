import traceback
from typing import Any

from aiogram import Router
from aiogram.handlers import ErrorHandler

import config


def setup():
    router = Router()
    router.errors.register(MyHandler)
    return router


class MyHandler(ErrorHandler):
    async def handle(self) -> Any:
        for admin in config.ADMIN_IDS:
            try:
                username = self.data['event_from_user'].username
                await self.bot.send_message(admin,
                                            f'<pre><code class="language-python">{traceback.format_exc()}</code></pre>'
                                            f"\n\nFrom: ({f'@{username}' if username else self.data['event_from_user'].full_name}) "
                                            f"<code>{self.data['event_from_user'].id}</code>")

            except Exception as e:
                # Add here logging to file/logging system
                pass
