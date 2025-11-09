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
        "💬 Задайте ваш вопрос по проектному обучению:\n\n"
        "Например:\n"
        "• Как составить техническое задание?\n"
        "• Какие этапы в Scrum?\n"
        "• Как распределить роли в команде?",
        reply_markup=KeyboardBuilder.back_button_kb()
    )
    await state.set_state(QuestionStates.waiting_question)


@router.message(QuestionStates.waiting_question)
async def handle_question(message: types.Message, state: FSMContext):
    question = message.text

    processing_msg = await message.answer("🔍 Ищу информацию в базе знаний...")

    try:
        answer = await RAGClient.get_answer(question, message.from_user.id)

        await processing_msg.delete()
        await message.answer(answer, reply_markup=KeyboardBuilder.back_button_kb())

    except Exception as e:
        await processing_msg.delete()
        await message.answer(
            "❌ Произошла ошибка при обработке запроса. Попробуйте позже.",
            reply_markup=KeyboardBuilder.back_button_kb()
        )

    await state.clear()


@router.callback_query(F.data == 'project_methodology')
async def project_methodology_menu(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "📚 Выберите тему по методологии проектов:",
        reply_markup=KeyboardBuilder.methodology_kb()
    )


@router.callback_query(F.data.startswith('method_'))
async def handle_methodology_topic(callback: types.CallbackQuery, state: FSMContext):
    topic = callback.data.replace('method_', '')

    topic_questions = {
        'scrum': "Расскажи подробно о методологии Scrum: основные принципы, роли, артефакты и церемонии",
        'agile': "Что такое Agile манифест и основные принципы гибкой разработки?",
        'kanban': "Как работает методология Kanban и её отличия от Scrum?",
        'devops': "Что такое DevOps практики в проектной деятельности?",
        'planning': "Как правильно планировать задачи в студенческом проекте?",
        'documentation': "Какая документация должна быть в студенческом проекте и как её вести?"
    }

    question = topic_questions.get(topic, "Расскажи о методологии проектов")

    processing_msg = await callback.message.answer("🔍 Ищу информацию...")

    try:
        answer = await RAGClient.get_answer(question, callback.from_user.id)
        await processing_msg.delete()
        await callback.message.answer(answer, reply_markup=KeyboardBuilder.back_to_methodology_kb())
    except Exception as e:
        await processing_msg.delete()
        await callback.message.answer(
            "❌ Произошла ошибка. Попробуйте позже.",
            reply_markup=KeyboardBuilder.back_to_methodology_kb()
        )