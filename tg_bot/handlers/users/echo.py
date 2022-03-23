from aiogram import types

from loader import dp
from utils.db_api import post_ai_request


@dp.message_handler(state=None)
async def bot_echo(message: types.Message):
    data = {
        "question": message.text,
        "answer": "/",
    }
    answer = (await post_ai_request(data=data))['answer']
    await message.answer(answer)
