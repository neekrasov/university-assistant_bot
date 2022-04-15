from aiogram import types
from aiogram.dispatcher.filters import CommandHelp
from aiogram.dispatcher.filters.builtin import CommandStart

from filters.private import IsPrivate
from loader import dp


@dp.message_handler(IsPrivate(), CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f"Привет, {message.from_user.full_name}!")


@dp.message_handler(IsPrivate(), CommandHelp())
async def bot_help(message: types.Message):
    text = ("Список команд: ",
            "/start - Начать диалог",
            "/help - Получить справку")

    await message.answer("\n".join(text))