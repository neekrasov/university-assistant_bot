from aiogram import types
from aiogram.dispatcher.filters import Command

from loader import dp
from utils.db_api import retraining_get_request


@dp.message_handler(Command("/retraining"))
async def retraining_core(message: types.Message):
    retraining_status = await retraining_get_request()
    await message.answer(retraining_status)
