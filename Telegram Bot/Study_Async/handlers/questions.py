from aiogram import Router, F
from aiogram.filters import Command, MagicData, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery

from keyboards.for_questions import get_yes_no_kb

maintenance_router = Router()
maintenance_router.message.filter(MagicData(F.maintenance_mode.is_(True)))
maintenance_router.callback_query.filter(MagicData(F.maintenance_mode.is_(True)))

regular_router = Router()

textTO = 'Бот в режиме обслуживания. Пожалуйста подождите!'

@maintenance_router.message()
async def any_message(message: Message):
    await message.answer(textTO)

@maintenance_router.callback_query()
async def any_callback(callback: CallbackQuery):
    await callback.answer(text=textTO, show_alert=False)

@regular_router.message(Command('start'))
async def cms_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
                'Вы довольны своей работой?',
        reply_markup=get_yes_no_kb()
    )

@regular_router.message(F.text.lower() == 'yes')
async def answer_yes(message: Message):
    await message.answer(
        "This is excellent!"
        "Вы можете заказать: "
        "блюда (/food) или напитки (/drinks).",
        reply_markup=ReplyKeyboardRemove()
    )

@regular_router.message(F.text.lower() == 'no')
async def answer_no(message: Message):
    await message.answer(
        'Sorry...',
        reply_markup=ReplyKeyboardRemove()
    )

@regular_router.message(StateFilter(None), Command(commands=['cancel']))
@regular_router.message(default_state, F.text.lower() == "отмена")
async def cmd_cancel_no_state(message: Message, state: FSMContext):
    await state.set_data({})
    await message.answer(
        text="Нечего отменять",
        reply_markup=ReplyKeyboardRemove()
    )

@regular_router.message(Command('cancel'))
@regular_router.message(F.text.lower() == "отмена")
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Действие отменено",
        reply_markup=ReplyKeyboardRemove()
    )