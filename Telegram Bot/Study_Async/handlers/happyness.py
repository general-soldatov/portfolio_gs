from random import randint
from typing import Any, Callable, Dict, Awaitable
from datetime import datetime
from aiogram import BaseMiddleware, Router, F
from aiogram.types import TelegramObject, Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import Command

class UserInternalIdMiddleware(BaseMiddleware):
    def get_internal_id(self, user_id: int) -> int:
        return randint(100_000_000, 900_000_000) + user_id
    
    async def __call__(
            self, 
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]], 
            event: TelegramObject, 
            data: Dict[str, Any]
            ) -> Any:
        user = data['event_from_user']
        data['internal_id'] = self.get_internal_id(user.id)
        return await handler(event, data)
    
class HappyMonthMiddleware(BaseMiddleware):
    async def __call__(
            self, 
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]], 
            event: TelegramObject, 
            data: Dict[str, Any]
            ) -> Any:
        internal_id: int = data['internal_id']
        current_month: int = datetime.now().month
        is_happy_month: bool = (internal_id % 12) == current_month
        data['is_happy_month'] = is_happy_month
        return await handler(event, data)
    
class WeekendCallbackMiddleware(BaseMiddleware):
    def is_weekend(self) -> bool:
        return datetime.utcnow().weekday() in (5, 6)
    
    async def __call__(
            self, 
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]], 
            event: TelegramObject, 
            data: Dict[str, Any]
            ) -> Any:
        if not isinstance(event, CallbackQuery):
            print('Игнор миддлваря')
            return await handler(event, data)
        if not self.is_weekend():
            return await handler(event, data)
        
        await event.answer(
            "Какая работа? Завод остановлен до понедельника!",
            show_alert=True
        )
        return
    
    
router = Router()
router.message.middleware(HappyMonthMiddleware())
router.message.middleware(WeekendCallbackMiddleware())

@router.message(Command('happymonth'))
async def cmd_happymonth(
    message: Message,
    internal_id: int,
    is_happy_month: bool
):
    phrases = [f"Ваш ID в нашем сервисе: {internal_id}"]
    if is_happy_month:
        phrases.append('Сейчас ваш счастливый месяц!')
    else:
        phrases.append("В этом месяце будьте осторожнее...")
    await message.answer('. '.join(phrases))

@router.message(Command('checkin'))
async def cmd_checkin(message: Message):
    builder = InlineKeyboardBuilder()
    builder.button(text='I`m working', callback_data='checkin')
    await message.answer(
        text="Нажимайте эту кнопку только по будним дням!",
        reply_markup=builder.as_markup()
    )

@router.callback_query(F.data == 'checkin')
async def callback_answer(callback: CallbackQuery):
    #Тут много сложного кода
    await callback.answer(
        text="Спасибо, что подтвердили своё присутствие!",
        show_alert=True
    )