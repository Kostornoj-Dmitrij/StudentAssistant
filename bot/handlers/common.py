from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from keyboards.builders import KeyboardBuilder

router = Router()

@router.callback_query(F.data == 'start')
async def back_to_start(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    try:
        await callback.message.delete()
    except:
        pass
    await callback.message.answer(
        "👋 Привет! Я твой ИИ-ассистент по проектному обучению.",
        reply_markup=KeyboardBuilder.start_kb()
    )