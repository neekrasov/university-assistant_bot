from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.utils.callback_data import CallbackData

from data.config import get_manager_id
from loader import dp
from utils.db_api import post_ai_request

send_manager_call = CallbackData("send_to_manager", "text", "user")


@dp.message_handler(state=None)
async def bot_echo(message: types.Message):
    data = {
        "question": message.text,
    }
    answer = (await post_ai_request(data=data))['answer']
    if len(answer) == 1:
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="Написать менеджеру.",
                                     callback_data=send_manager_call.new(text=message.text,
                                                                         user=message.from_user.id))
            ]
        ]
        )
        await message.answer(
            text="Я не могу ответить на этот вопрос. Перефразируйте сообщение или отправьте данный вопрос менеджеру.",
            reply_markup=markup)

    else:
        await message.answer(answer)


@dp.callback_query_handler(send_manager_call.filter())
async def send_message_to_manager(call: CallbackQuery, callback_data: dict):
    question = callback_data.get("text")
    user_id = callback_data.get("user")
    manager_id = get_manager_id()
    await call.answer("Ваш вопрос был отправлен менеджеру!")
    user = await dp.bot.get_chat_member(user_id, user_id)
    await dp.bot.send_message(chat_id=int(manager_id[0]),
                              text=f"Вопрос: '{question}'"
                                   f"поступил от пользователя: {user.user.get_mention()}.")

