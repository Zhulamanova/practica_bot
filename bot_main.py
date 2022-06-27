import asyncio
import logging

from aiogram import Bot, Dispatcher, executor
from aiogram import types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart, Text, CommandHelp
from aiogram.types import Message, CallbackQuery
from aiogram.utils.exceptions import WrongFileIdentifier, InvalidHTTPUrlContent

from database.database_module import Base, engine
from dictionaries import validate_district, district_dict, get_key_by_value
from keyboards.default.find_keyboard import start_find_keyboard, stop_find_keyboard
from keyboards.inline.countinue_keyboard import get_continue_keyboard
from keyboards.inline.district_keyboard import get_district_keyboard
from my_parser.flat_parser import parse, validate_request
from repositories.history_repository import get_last_ten_history_request_by_tg_id, create_history_request
from repositories.user_repository import create_user
from states.find_flat_state import FindFlatState
from utils.set_bot_commands import set_default_commands

API_TOKEN = '5138873379:AAFGsXhV7MuVsyQUdZ7aKJBxn-H9FXMPDg8'

# Configure logging
logging.basicConfig(filename='bot.log', encoding='utf-8', level=logging.ERROR,
                    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


async def on_startup(dispatcher):
    await set_default_commands(dispatcher)
    Base.metadata.create_all(engine)


__params_text = "Для подбора жилья необходимо ввести параметры по которым я буду искать, \n" \
                "Формат: {Кол-во комнат, Стоимость, Этаж}\n" \
                "Пример: 2, от 10000 до 16000, от 5 до 12"


async def start_find(message: Message, state: FSMContext) -> None:
    await FindFlatState.district.set()
    await message.answer("Давай начнем поиск", reply_markup=stop_find_keyboard())
    await message.answer("Выбери район:", reply_markup=get_district_keyboard())


@dp.message_handler(CommandStart(), state='*')
async def bot_start(message: types.Message):
    create_user(telegram_user_id=message.from_user.id,
                full_name=message.from_user.full_name,
                username=message.from_user.username)

    await message.answer(
        f"Здравствуйте, {message.from_user.full_name}, я помогу найти тебе самое подходящее жилье в Челябинске.\n",
        reply_markup=start_find_keyboard())


@dp.message_handler(commands='params', state="*")
async def bot_four_question(message: Message, state: FSMContext) -> None:
    await message.answer(__params_text)


@dp.message_handler(CommandHelp(), state='*')
async def bot_help(message: types.Message):
    text = ("Список команд: ",
            "/start - Начать диалог",
            "/help - Получить справку",
            "/start_find - Начать поиск квартир",
            "/stop_find - Прекратить поиск квартир",
            "/params - Помощник по параметрам",
            "/history - Показывает историю твоих запросов"
            )
    await message.answer("\n".join(text))


@dp.message_handler(commands='history', state='*')
async def bot_four_question(message: Message, state: FSMContext) -> None:
    history = get_last_ten_history_request_by_tg_id(message.from_user.id)
    if history is None or len(history) == 0:
        await message.answer("Извините, но вы ничего не искали)")
    else:
        count_item = 1
        result = ''
        for item in history:
            result = result + f"{count_item}) " + str(item) + "\n\n"
            count_item += 1
        await message.answer(result)


@dp.message_handler(state='*', commands='stop_find')
@dp.message_handler(Text(equals="остановить поиск", ignore_case=True), state='*')
async def cmd_cancel(message: Message, state: FSMContext):
    await message.answer("Поиск прекращен", reply_markup=start_find_keyboard())
    await state.finish()


@dp.message_handler(state='*', commands='start_find')
@dp.message_handler(Text(equals="Начать поиск", ignore_case=True), state='*')
async def start_find_handler(message: Message, state: FSMContext) -> None:
    await start_find(message, state)


@dp.callback_query_handler(Text(equals="continue", ignore_case=True), state='*')
async def start_find_handler(callback: CallbackQuery, state: FSMContext) -> None:
    await start_find(callback.message, state)


@dp.callback_query_handler(Text(contains="district", ignore_case=True), state=FindFlatState.district)
async def district_callback(callback_query: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        value = callback_query.data.replace('district_', '').strip()
        data['district'] = district_dict[value]

    await callback_query.message.answer(__params_text)
    await FindFlatState.next()


@dp.message_handler(state=FindFlatState.district)
async def district_text(message: Message, state: FSMContext) -> None:
    if validate_district(message.text):
        await message.answer(__params_text)
        async with state.proxy() as data:
            data['district'] = district_dict[message.text.strip()]
        await FindFlatState.next()
    else:
        await message.answer("Такого района нет, попробуй повторить попытку или нажми на кнопку снизу",
                             reply_markup=get_district_keyboard())


@dp.message_handler(state=FindFlatState.params)
async def district_text(message: Message, state: FSMContext) -> None:
    validity = await validate_request(message.text)

    if not validity[0]:
        await message.answer("Параметры введены не в том формате, попробуй еще раз")
    else:
        await message.answer("Подожди секунду, уже ищу 🔍")
        async with state.proxy() as data:
            district = data['district']
        user_request_model = validity[1]
        user_request_model.district = district
        flat_list = await parse(user_request_model)
        if flat_list is None or len(flat_list) == 0:
            await message.answer("По вашему запросу ничего не найдено, хотите продолжить поиск?",
                                 reply_markup=get_continue_keyboard())
        else:
            try:
                for flat in flat_list:
                    try:
                        await bot.send_photo(chat_id=message.chat.id, photo=flat.image_url, caption=str(flat))
                    except (WrongFileIdentifier ,InvalidHTTPUrlContent):
                        await bot.send_message(chat_id=message.chat.id, text=str(flat))
                    await asyncio.sleep(0.3)
            except Exception as ex:
                logging.error(ex)
            finally:
                user_request_model.district = get_key_by_value(district_dict, user_request_model.district)
                create_history_request(str(user_request_model), message.from_user.id)
                await FindFlatState.next()
                await message.answer("Хотите продолжить поиск?",
                                     reply_markup=get_continue_keyboard())


@dp.message_handler(state="*")
async def bot_four_question(message: Message, state: FSMContext) -> None:
    await message.answer("Извините, я не понял чего вы хотите. Разобраться со всем Вам может помочь команда /help !")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)