from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from keyboards.builders import KeyboardBuilder

router = Router()

@router.message(CommandStart())
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()

    await message.answer(
        "👋 Привет! Я твой ИИ-ассистент по проектному обучению.\n\n"
        "Выбери действие:",
        reply_markup=KeyboardBuilder.start_kb()
    )