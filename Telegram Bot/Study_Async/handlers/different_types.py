from aiogram import Router, F
from aiogram.types import Message

router = Router()

@router.message(F.text)
async def message_with_text(message: Message):
    await message.answer("This is text message!")

@router.message(F.sticker)
async def message_witn_sticker(message: Message):
    await message.answer("This is sticker!")

@router.message(F.animation)
async def message_with_gif(message: Message):
    await message.answer('This is GIF!')