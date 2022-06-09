from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Запустить бота"),
            types.BotCommand("help", "Вывести справку"),
            types.BotCommand("start_find", "Начать поиск квартир"),
            types.BotCommand("stop_find", "Прекратить поиск квартир"),
            types.BotCommand("params", "Помощник по параметрам"),
            types.BotCommand("history", "Показывает историю твоих запросов"),
        ]
    )
