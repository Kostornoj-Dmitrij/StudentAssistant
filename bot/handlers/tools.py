from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from keyboards.builders import KeyboardBuilder
from services.rag_client import RAGClient

router = Router()


@router.callback_query(F.data == 'tools_practices')
async def tools_practices_menu(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "🛠 *Инструменты и практики проектной деятельности*\n\n"
        "Выберите категорию:",
        reply_markup=KeyboardBuilder.tools_kb(),
        parse_mode="Markdown"
    )


@router.callback_query(F.data.startswith('tool_'))
async def handle_tool_topic(callback: types.CallbackQuery, state: FSMContext):
    topic = callback.data.replace('tool_', '')

    topic_questions = {
        'trello': "Расскажи о Trello для управления проектами",
        'jira': "Что такое Jira и как её использовать в проектах?",
        'notion': "Как использовать Notion для ведения проектной документации?",
        'git': "Как использовать Git в командной работе над проектом?"
    }

    question = topic_questions.get(topic, "Расскажи об инструментах проектной деятельности")

    processing_msg = await callback.message.answer("🔍 Ищу информацию...")

    try:
        answer = await RAGClient.get_answer(question, callback.from_user.id)
        await processing_msg.delete()
        await callback.message.answer(
            answer,
            reply_markup=KeyboardBuilder.back_to_tools_kb(),
            parse_mode="Markdown"
        )
    except Exception as e:
        await processing_msg.delete()
        await callback.message.answer(
            "❌ Произошла ошибка. Попробуйте позже.",
            reply_markup=KeyboardBuilder.back_to_tools_kb()
        )


@router.callback_query(F.data == 'templates')
async def templates_menu(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "📋 *Шаблоны документов для проектов*\n\n"
        "Скоро здесь появятся шаблоны:\n"
        "• Техническое задание (ТЗ)\n"
        "• План проекта\n"
        "• Отчет о проделанной работе\n"
        "• Презентация проекта\n"
        "• Протокол встречи\n\n"
        "Пока вы можете задать вопрос о том, как составить тот или иной документ.",
        reply_markup=KeyboardBuilder.back_button_kb(),
        parse_mode="Markdown"
    )