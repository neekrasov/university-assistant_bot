from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Command
from aiogram.types import CallbackQuery

from data.config import ADMINS
from filters.private import IsPrivate
from keyboards.inline.admin_answers_keyboard import get_pages_keyboard, pagination_call, show_question
from loader import dp
from utils.db_api import get_all_questions_request, put_question_request, get_question_request
from loguru import logger


@dp.message_handler(IsPrivate(), Command("menu"))
async def answer_questions(message: types.Message):
    if message.from_user.id not in ADMINS:
        await message.answer("Данная функция доступна только администраторам")
    else:
        questions = await get_all_questions_request()
        await message.answer(
            text="Список вопросов",
            reply_markup=get_pages_keyboard(questions)
        )


@dp.callback_query_handler(pagination_call.filter(key="questions"))
async def show_chosen_page(call: CallbackQuery, callback_data: dict):
    current_page = callback_data.get("page")
    if current_page == "empty":
        await call.answer(text="Текущая страница")
    else:
        questions = await get_all_questions_request()
        markup = get_pages_keyboard(questions, page=int(current_page))
        await call.message.edit_reply_markup(markup)


@dp.callback_query_handler(show_question.filter())
async def listen_answer(call: CallbackQuery, callback_data: dict, state: FSMContext):
    question_id = callback_data.get("question_id")
    await state.update_data(
        question_id=question_id,
    )
    await call.answer()
    await call.message.answer("Введите ответ на вопрос")
    await state.set_state("add_answer")


@dp.message_handler(state="add_answer")
async def set_answer(message: types.Message, state: FSMContext):
    data = await state.get_data()
    question_id = int(data.get("question_id"))
    answer = await put_question_request(data={
        "id": int(question_id),
        "answer": message.text,
    })
    question = await get_question_request(question_id)
    logger.debug(question)
    await message.answer(text=f"Ответ на вопрос: <b>'{question['question']}'</b> "
                              f"был добавлен успешно. \nВаш ответ: <b>{message.text}</b>")
    await state.finish()
