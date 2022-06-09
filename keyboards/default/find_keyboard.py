from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def start_find_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)

    keyboard.add(KeyboardButton(
        text="Начать поиск"))

    return keyboard


def stop_find_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)

    keyboard.add(KeyboardButton(text="Остановить поиск"))

    return keyboard
