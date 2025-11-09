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
        "Я могу помочь тебе с:\n"
        "• Планированием проекта\n"
        "• Методологиями (Agile, Scrum, DevOps)\n"
        "• Документацией и отчетами\n"
        "• Распределением ролей в команде\n\n"
        "Выбери, чем могу помочь:",
        reply_markup=KeyboardBuilder.start_kb()
    )