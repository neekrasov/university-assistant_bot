from aiogram import types

from data.config import assistant_bot
from loader import dp


@dp.message_handler(state=None)
async def bot_echo(message: types.Message):
    answer = assistant_bot.ask(message.text)
    await message.answer(answer)
