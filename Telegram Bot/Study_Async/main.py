import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from config_reader import config
from handlers import questions, different_types, usernames
from keyboards import simple_row
from filters.middleware import SlowpokenMiddleware
from aiogram.fsm.storage.memory import MemoryStorage
from handlers.happyness import UserInternalIdMiddleware, WeekendCallbackMiddleware, router


#запуск бота
async def main():
    logging.basicConfig(
        level=logging.INFO, 
        stream=sys.stdout,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        )
    
    TOKEN = config.bot_token.get_secret_value()
    bot = Bot(token=TOKEN)
    #запуск диспетчера (режим обслуживания - True)
    dp = Dispatcher(storage=MemoryStorage(), maintenance_mode=False)
    #обработка через middleware
    dp.update.outer_middleware(UserInternalIdMiddleware())
    dp.callback_query.outer_middleware(WeekendCallbackMiddleware())
    questions.regular_router.message.middleware(SlowpokenMiddleware(sleep_sec=1))
    usernames.router.message.middleware(SlowpokenMiddleware(sleep_sec=2))
    #роутер ТО & роутер команд
    dp.include_routers(questions.regular_router, questions.maintenance_router)
    dp.include_router(router)
    dp.include_router(simple_row.router)
    #роутер текстовых сообщений
    dp.include_routers(usernames.router, different_types.router)

    #запускаем бота и пропуск всех входящих
    #await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())


