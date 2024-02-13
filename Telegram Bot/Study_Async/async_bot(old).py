import asyncio
import logging
import re

from aiogram import Bot, Dispatcher, html, types
from aiogram.types import Message, FSInputFile, URLInputFile
from aiogram.filters import Command, CommandObject, CommandStart
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.markdown import hide_link
from aiogram.exceptions import TelegramBadRequest
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from aiogram.enums import ParseMode
from magic_filter import F
from aiogram.utils.formatting import (
    Text, Bold, as_list, as_marked_section, as_key_value, HashTag
)

from contextlib import suppress
from typing import Optional
from datetime import datetime
from random import randint
from config_reader import config
from aiogram.client.session.aiohttp import AiohttpSession

class NumbersCallbackFactory(CallbackData, prefix='fabnum'):
    action: str
    value: Optional[int] = None

session = AiohttpSession(proxy='http://proxy.server:3128')

logging.basicConfig(level=logging.INFO)
TOKEN = config.bot_token.get_secret_value()

bot = Bot(token=TOKEN, session=session)

dp = Dispatcher()
dp.callback_query.middleware(
    CallbackAnswerMiddleware(
        pre=True, text='Ready', show_alert=False
        )
    )
dp["started_at"] = datetime.now().strftime("%d-%m-%Y %H:%M")

@dp.message(F.text, Command("start"))
async def cmd_start(message: Message):
    #команда старт
    await message.answer("Hello")
    kb = [
        [types.KeyboardButton(text='С пюрешкой'),
        types.KeyboardButton(text='Без пюрешки')]
        ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder='Выберите способ подачи'
        )
    await message.answer("Как подавать котлеты?", reply_markup=keyboard)


@dp.message(F.text, Command("test"))
async def cmd_test(message: Message):
    #тестирование разметки сообщения
    await message.reply(
        "This is command <b>test!</b>",
        parse_mode=ParseMode.HTML
        )
    await message.answer(
        "This is *chat\-bot*\!",
        parse_mode=ParseMode.MARKDOWN_V2
        )

@dp.message(Command("hello"))
async def cmd_hello(message: Message):
    #команда приветствия
    content = Text(
        "Hello, ",
        Bold(message.from_user.full_name)
        )
    await message.answer(
        **content.as_kwargs()
        )

@dp.message(F.text, Command("add"))
async def cmd_add(message: Message, myList: list[int]):
    #команда вызова метода добавления цифры 7
    myList.append(7)
    await message.answer("7 add to list")

@dp.message(F.text, Command('show'))
async def cmd_show(message: Message, myList: list[int]):
    #вывод списка
    await message.answer(f'Your list {myList}')

@dp.message(F.text, Command('info'))
async def cmd_info(message: Message, started_at: str):
    #информация о времени запуска бота
    await message.answer(f'Bot is started {started_at}')

@dp.message(Command('examples'))
async def cmd_examples(message: Message):
    #команда примера вёрстки контента в сообщении
    content = as_list(
        as_marked_section(
            Bold("Success:"),
            'Test 1',
            'Test 2',
            'Test 3',
            marker='✅ ',
            ),
        as_marked_section(
            "Failed:",
            "Test 2",
            marker="❌ ",
            ),
        as_marked_section(
            Bold('Summary:'),
            as_key_value('Total', 2),
            as_key_value('Success', 3),
            as_key_value('Failed', 1),
            marker='  ',
            ),
        HashTag('#test'),
        sep='\n\n',
        )

    await message.answer(**content.as_kwargs())

@dp.message(Command('parser'))
async def cmd_parser(
    message: Message,
    command: CommandObject
):
    #команда парсера из сообщения сайта, почты и кода
    if command.args is None:
        await message.answer('Error: not args')
        return

    data = {
        'url': '<N/A>',
        'email': '<N/A>',
        'code': '<N/A>'
        }
    entities = message.entities or []
    for item in entities:
        if item.type in data.keys():
            data[item.type] = item.extract_from(message.text)

    time_now = datetime.now().strftime('%H:%M')
    added_text = html.underline(f'Created at {time_now}')
    await message.answer(
        'This I`m search:\n'
        f"URL: {html.quote(data['url'])}\n"
        f"E-mail: {html.quote(data['email'])}\n"
        f"Password: {html.quote(data['code'])}"
        f'\n\n{added_text}', parse_mode='HTML'
        )

@dp.message(Command('settimer'))
async def cmd_settimer(message: Message, command: CommandObject):
    #команда установки таймера
    if command.args is None:
        await message.answer('Error: not args')
        return

    try:
        delay_time, text_to_send = command.args.split(" ", maxsplit=1)
    except ValueError:
        await message.answer(
            "Ошибка: неправильный формат команды. Пример:\n"
            "/settimer <time> <message>"
            )
        return
    await message.answer(
        'Timer append!\n'
        f'Time: {delay_time}\n'
        f'Text: {text_to_send}'
        )

@dp.message(Command('help'))
@dp.message(CommandStart(deep_link=True, magic=F.args=='help'))
async def cmd_start_help(message: Message):
    await message.answer('This message for help')

@dp.message(CommandStart(deep_link=True, magic=F.args.regexp(re.compile(r'book_(\d+)'))))
async def cmd_start_book(message: Message, command: CommandObject):
    book_number = command.args.split("_")[1]
    await message.answer(f'Sending book №{book_number}')

@dp.message(Command('images'))
async def cmd_upload_photo(message: Message):
    #file_id отправленных файлов
    file_ids = []

    #отправка из файловой системы
    image_from_pc = FSInputFile('cat_code.jpeg')
    result = await message.answer_photo(
        image_from_pc,
        caption='Image from PC'
        )
    file_ids.append(result.photo[-1].file_id)

    image_from_url = URLInputFile('https://sun1-24.userapi.com/s/v1/if1/honL_lQYnAakiVwPlhn9CU-nW9ntkBw5MU8IQaQM68PH4bapZ1yX-HbTPon0AUUegdvBZNDl.jpg?size=1420x1421&quality=96&crop=103,50,1420,1421&ava=1')
    result = await message.answer_photo(
        image_from_url,
        caption='Image from URL'
        )
    file_ids.append(result.photo[-1].file_id)
    await message.answer('Shipped files: \n' +'\n'.join(file_ids))

@dp.message(Command('hidden_link'))
async def cmd_hidden_link(message: Message):
    await message.answer(
        f"{hide_link('https://telegra.ph/file/562a512448876923e28c3.png')}"
        f"Документация Telegram: *существует*\n"
        f"Пользователи: *не читают документацию*\n"
        f"Груша:",
        disable_web_page_preview=True, parse_mode="HTML"
        )
@dp.message(Command('reply_builder'))
async def cmd_reply_builder(message: Message):
    builder = ReplyKeyboardBuilder()
    for i in range(1, 17):
        builder.add(types.KeyboardButton(text=str(i)))
    builder.adjust(4)
    await message.answer(
        'Choise is number',
        reply_markup=builder.as_markup(resize_keyboard=True)
        )

@dp.message(Command('inline_url'))
async def cmd_inline_url(message: Message, bot: Bot):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text='GitHub', url='https://github.com')
        )
    builder.row(types.InlineKeyboardButton(
        text='Telegram',
        url='tg://resolve?domain=telegram')
        )
    user_id = message.from_user.id
    chat_info = await bot.get_chat(user_id)
    if not chat_info.has_private_forwards:
        builder.row(types.InlineKeyboardButton(
            text='Random user',
            url=f'tg://user?id={user_id}')
            )

        await message.answer(
            'Select URL',
            reply_markup=builder.as_markup(),
            )

@dp.message(Command('random'))
async def cmd_random(message: Message):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text = 'Push me',
        callback_data = 'random_value')
        )
    await message.answer(
        'Push the button and bot send random number from 1 to 10',
        reply_markup=builder.as_markup()
        )

@dp.callback_query(F.data == 'random_value')
async def call_random_value(callback: types.CallbackQuery):
    await callback.message.answer(str(randint(1, 10)))
    await callback.answer(
        text = 'Thanks for using chat-bot',
        show_alert=True
        )

@dp.message(F.photo)
async def download_photo(message: Message, bot: Bot):
    await bot.download(
        message.photo[-1],
        destination=f'/tmp/{message.photo[-1].file_id}.jpg'
        )
    await message.answer('Photo is download for server')

@dp.message(F.text.lower() == 'с пюрешкой')
async def with_puree(message: Message):
    await message.reply('The choice is excellent')

@dp.message(F.text.lower() == 'без пюрешки')
async def without_puree(message: Message):
    await message.reply("It`s so tasteless")

user_data = {}

def get_keyboard():
    buttons = [
        [
            types.InlineKeyboardButton(text='-1', callback_data='num_decr'),
            types.InlineKeyboardButton(text='+1', callback_data='num_incr')
            ],
            [types.InlineKeyboardButton(text='Confirm', callback_data='num_finish')]
        ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

async def update_num_text(message: types.Message, new_value: int):
    with suppress(TelegramBadRequest):
        await message.edit_text(
            f'Select number {new_value}',
            reply_markup=get_keyboard()
            )

@dp.message(Command('numbers'))
async def cmd_numbers(message: Message):
    user_data[message.from_user.id] = 0
    await message.answer('Select number: 0', reply_markup=get_keyboard())

@dp.callback_query(F.data.startswith('num_'))
async def callback_num(callback: types.CallbackQuery):
    user_value = user_data.get(callback.from_user.id, 0)
    action = callback.data.split('_')[1]

    if action == 'incr':
        user_data[callback.from_user.id] = user_value + 1
        await update_num_text(callback.message, user_value+1)
    elif action == 'decr':
        user_data[callback.from_user.id] = user_value - 1
        await update_num_text(callback.message, user_value-1)
    elif action == 'finish':
        await callback.message.edit_text(f'Summary: {user_value}')

    await callback.answer()

def get_keyboard_fab():
    builder = InlineKeyboardBuilder()
    builder.button(
        text='-2', callback_data=NumbersCallbackFactory(action='change', value=-2)
        )
    builder.button(
        text='-1', callback_data=NumbersCallbackFactory(action='change', value=-1)
        )
    builder.button(
        text='+1', callback_data=NumbersCallbackFactory(action='change', value=1)
        )
    builder.button(
        text='+2', callback_data=NumbersCallbackFactory(action='change', value=2)
        )
    builder.button(
        text='Confirm', callback_data=NumbersCallbackFactory(action='finish')
        )
    builder.adjust(4)
    return builder.as_markup()

async def update_num_text_fab(message: Message, new_value: int):
    with suppress(TelegramBadRequest):
        await message.edit_text(
            f'Select number {new_value}',
            reply_markup=get_keyboard_fab()
            )

@dp.message(Command('numbers_fab'))
async def cmd_numbers_fab(message: Message):
    user_data[message.from_user.id] = 0
    await message.answer('Select number: 0', reply_markup=get_keyboard_fab())

@dp.callback_query(NumbersCallbackFactory.filter(F.action == 'change'))
async def callbacks_num_change_fab(
    callback: types.CallbackQuery,
    callback_data: NumbersCallbackFactory
):
    user_value = user_data.get(callback.from_user.id, 0)
    user_data[callback.from_user.id] = user_value + callback_data.value
    await update_num_text_fab(callback.message, user_value + callback_data.value)
    await callback.answer()

@dp.callback_query(NumbersCallbackFactory.filter(F.action == 'finish'))
async def callbacks_num_finish_fab(callback: types.CallbackQuery):
    user_value = user_data.get(callback.from_user.id, 0)
    await callback.message.edit_text(f'Summary: {user_value}')
    await callback.answer()


async def main():
    print(datetime.now())
    while True:
        try:
            await dp.start_polling(bot, myList=[1, 2, 3])
        except Exception as e:
            print('crush', datetime.now().strftime("%d-%m-%Y %H:%M"), e)



if __name__ == "__main__":
    asyncio.run(main())
