from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from dictionaries import district_dict


def get_district_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)
    districts = district_dict.keys()
    for district in districts:
        keyboard.add(
            InlineKeyboardButton(
                text=district,
                callback_data='district_' + district))

    return keyboard
