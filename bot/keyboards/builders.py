from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

class KeyboardBuilder:
    @staticmethod
    def start_kb():
        builder = InlineKeyboardBuilder()
        builder.add(
            InlineKeyboardButton(
                text='💬 Задать вопрос',
                callback_data='ask_question'
            ),
            InlineKeyboardButton(
                text='📋 Примеры вопросов',
                callback_data='examples'
            ),
            InlineKeyboardButton(
                text='🤖 О боте',
                callback_data='about'
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
    def back_to_start_kb():
        builder = InlineKeyboardBuilder()
        builder.add(InlineKeyboardButton(text='🏠 В начало', callback_data='start'))
        return builder.as_markup()