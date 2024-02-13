from typing import List

from aiogram import Router, F, html
from aiogram.types import Message

from filters.find_usernames import HasUsernamesFilter, LoginParser

router = Router()

@router.message(F.text, HasUsernamesFilter())
async def message_with_usernames(message: Message, usernames: List[str]):
    await message.reply(
        f'Спасибо, обязательно подпишусь на '
        f'{", ".join(usernames)}'
    )

@router.message(F.text, LoginParser())
async def login_parser(message: Message, login: List[str]):
    await message.answer(
        'This I`m search:\n'
        f"URL: {login[0]}\n"
        f"E-mail: {login[1]}\n"
        f"Password: {login[2]}"
    )
            