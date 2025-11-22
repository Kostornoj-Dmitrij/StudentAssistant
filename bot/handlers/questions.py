from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from keyboards.builders import KeyboardBuilder
from models.states import QuestionStates
from services.rag_client import RAGClient

router = Router()


@router.callback_query(F.data == 'ask_question')
async def start_question_flow(callback: types.CallbackQuery, state: FSMContext):
    try:
        await callback.message.delete()
    except:
        pass

    await callback.message.answer(
        "💬 Напишите ваш вопрос по проектному обучению:",
        reply_markup=KeyboardBuilder.back_button_kb()
    )
    await state.set_state(QuestionStates.waiting_question)


@router.message(QuestionStates.waiting_question)
async def handle_question(message: types.Message, state: FSMContext):
    question = message.text

    processing_msg = await message.answer("🔍 Получение информации из базы знаний...")

    try:
        answer = await RAGClient.get_answer(question, message.from_user.id)

        await processing_msg.edit_text(
            f"🤖 Ответ на ваш вопрос:\n\n{answer}",
            reply_markup=KeyboardBuilder.back_to_start_kb()
        )

    except Exception as e:
        await processing_msg.edit_text(
            "❌ Произошла ошибка при обработке запроса. Попробуйте позже.",
            reply_markup=KeyboardBuilder.back_to_start_kb()
        )

    await state.clear()


@router.callback_query(F.data == 'examples')
async def show_examples(callback: types.CallbackQuery, state: FSMContext):
    try:
        await callback.message.delete()
    except:
        pass

    examples_text = """
📋 *Примеры вопросов, которые можно задать:*

*Планирование проекта:*
• Как составить план проекта?
• Какие этапы должны быть в студенческом проекте?
• Как оценить время на выполнение задач?

*Методологии:*
• Что такое Scrum и как его применять?
• В чем разница между Agile и Waterfall?
• Как проводить ежедневные стендапы?

*Документация:*
• Как оформить техническое задание?
• Какая документация нужна для проекта?
• Как вести протоколы встреч?

*Командная работа:*
• Как распределить роли в команде?
• Как эффективно проводить командные встречи?
• Как разрешать конфликты в команде?
"""

    await callback.message.answer(
        examples_text,
        reply_markup=KeyboardBuilder.back_button_kb(),
        parse_mode="Markdown"
    )


@router.callback_query(F.data == 'about')
async def show_about(callback: types.CallbackQuery, state: FSMContext):
    try:
        await callback.message.delete()
    except:
        pass

    about_text = """
🤖 *О боте*

Я - ИИ-ассистент для студентов, работающих над проектами. Моя задача - помогать вам с методологическими вопросами проектной деятельности.

*Что я умею:*
• Отвечать на вопросы по управлению проектами
• Консультировать по методологиям (Agile, Scrum, Kanban)
• Помогать с документацией и планированием
• Давать советы по командной работе

*Особенности:*
• Ответы основаны на проверенной базе знаний
• Использую RAG-архитектуру для точности
• Постоянно обучаюсь на новых материалах
"""

    await callback.message.answer(
        about_text,
        reply_markup=KeyboardBuilder.back_button_kb(),
        parse_mode="Markdown"
    )