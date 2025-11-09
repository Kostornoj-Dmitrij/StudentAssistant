from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

class KeyboardBuilder:
    @staticmethod
    def start_kb():
        builder = InlineKeyboardBuilder()
        builder.add(
            InlineKeyboardButton(
                text='💬 Задать вопрос по проекту',
                callback_data='ask_question'
            ),
            InlineKeyboardButton(
                text='📚 Методологии проектов',
                callback_data='project_methodology'
            ),
            InlineKeyboardButton(
                text='🛠 Инструменты и практики',
                callback_data='tools_practices'
            ),
            InlineKeyboardButton(
                text='📋 Шаблоны документов',
                callback_data='templates'
            )
        )
        builder.adjust(1)
        return builder.as_markup()

    @staticmethod
    def back_button_kb():
        builder = InlineKeyboardBuilder()
        builder.add(InlineKeyboardButton(text='⬅️ Назад', callback_data='start'))
        return builder.as_markup()

    @staticmethod
    def methodology_kb():
        builder = InlineKeyboardBuilder()
        builder.add(
            InlineKeyboardButton(text='🔄 Agile', callback_data='method_agile'),
            InlineKeyboardButton(text='🏈 Scrum', callback_data='method_scrum'),
            InlineKeyboardButton(text='📋 Kanban', callback_data='method_kanban'),
            InlineKeyboardButton(text='⚙️ DevOps', callback_data='method_devops'),
            InlineKeyboardButton(text='📅 Планирование', callback_data='method_planning'),
            InlineKeyboardButton(text='📄 Документация', callback_data='method_documentation'),
            InlineKeyboardButton(text='⬅️ Назад', callback_data='start')
        )
        builder.adjust(2)
        return builder.as_markup()

    @staticmethod
    def back_to_methodology_kb():
        builder = InlineKeyboardBuilder()
        builder.add(
            InlineKeyboardButton(text='📚 К методологиям', callback_data='project_methodology'),
            InlineKeyboardButton(text='🏠 В начало', callback_data='start')
        )
        builder.adjust(1)
        return builder.as_markup()

    @staticmethod
    def tools_kb():
        builder = InlineKeyboardBuilder()
        builder.add(
            InlineKeyboardButton(text='📊 Trello', callback_data='tool_trello'),
            InlineKeyboardButton(text='🎯 Jira', callback_data='tool_jira'),
            InlineKeyboardButton(text='📝 Notion', callback_data='tool_notion'),
            InlineKeyboardButton(text='🔗 Git', callback_data='tool_git'),
            InlineKeyboardButton(text='⬅️ Назад', callback_data='start')
        )
        builder.adjust(2)
        return builder.as_markup()

    @staticmethod
    def back_to_tools_kb():
        builder = InlineKeyboardBuilder()
        builder.add(
            InlineKeyboardButton(text='🛠 К инструментам', callback_data='tools_practices'),
            InlineKeyboardButton(text='🏠 В начало', callback_data='start')
        )
        builder.adjust(1)
        return builder.as_markup()