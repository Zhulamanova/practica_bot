from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_continue_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton(
            text="Да, продолжить",
            callback_data='continue'))

    return keyboard
