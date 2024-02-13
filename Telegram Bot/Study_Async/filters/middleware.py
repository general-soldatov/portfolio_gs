import asyncio
from typing import Any, Callable, Dict, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

class SlowpokenMiddleware(BaseMiddleware):
    def __init__(self, sleep_sec: int) -> None:
        self.sleep_sec = sleep_sec

    async def __call__(
            self, 
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]], 
            event: TelegramObject, 
            data: Dict[str, Any]) -> Any:
        await asyncio.sleep(self.sleep_sec)
        result = await handler(event, data)
        print(f'Handler was delayed by {self.sleep_sec} seconds')
        return result