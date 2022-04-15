from aiogram.types import InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

show_questions = CallbackData('show_item', 'item_id')


def get_pages_keyboard(array: list, page: int = 1, offset: int = 0):
    """
        Клавиатура с элементами пагинации.

    array: list - список всех элементов;
    page: int - номер страницы (по умолчанию 1);
    offset: int - смещение при передаче элементов на каждой странице;

    """
    MAX_ITEMS_PER_PAGE = 5

    first_item_index = (page - 1) * MAX_ITEMS_PER_PAGE
    last_item_index = page * MAX_ITEMS_PER_PAGE 

    sliced_array = array[first_item_index:last_item_index]
    item_buttons = []

    for item in sliced_array:
        item_buttons.append(
            InlineKeyboardButton(
                text=...,
                callback_data=...,
            )
        )
