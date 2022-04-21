from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

show_question = CallbackData('show_question', 'question_id')
pagination_call = CallbackData("paginator", "key", "page")


def get_pages_keyboard(array: list, page: int = 1):
    """
        Клавиатура с элементами пагинации.

    array: list - список всех элементов;
    page: int - номер страницы (по умолчанию 1);

    """
    KEY = "questions"
    MAX_ITEMS_PER_PAGE = 5

    """ Отображение кнопок с вопросами """

    first_item_index = (page - 1) * MAX_ITEMS_PER_PAGE
    last_item_index = page * MAX_ITEMS_PER_PAGE

    sliced_array = array[first_item_index:last_item_index]
    item_buttons = []

    markup = InlineKeyboardMarkup(row_width=1)
    for question in sliced_array:
        item_buttons.append(
            InlineKeyboardButton(
                text=f'{question["question"]}',
                callback_data=show_question.new(question_id=question['id']),
            )
        )

    """ Отображение кнопок пагинации """

    pages_buttons = []
    first_page = 1
    max_page = len(array) // MAX_ITEMS_PER_PAGE

    first_page_text = "« 1"
    max_page_text = f"» {max_page}"
    pages_buttons.append(
        InlineKeyboardButton(
            text=first_page_text,
            callback_data=pagination_call.new(key=KEY,
                                              page=first_page)
        )
    )

    previous_page = page - 1
    previous_page_text = f"< {previous_page}"

    if previous_page >= first_page:
        pages_buttons.append(
            InlineKeyboardButton(
                text=previous_page_text,
                callback_data=pagination_call.new(key=KEY,
                                                  page=previous_page)
            )
        )
    else:
        pages_buttons.append(
            InlineKeyboardButton(
                text=" . ",
                callback_data=pagination_call.new(key=KEY, page="empty")
            )
        )

    pages_buttons.append(
        InlineKeyboardButton(
            text=f"- {page} -",
            callback_data=pagination_call.new(key=KEY, page="empty")
        )
    )

    next_page = page + 1
    next_page_text = f"{next_page} >"

    if next_page <= max_page:
        pages_buttons.append(
            InlineKeyboardButton(
                text=next_page_text,
                callback_data=pagination_call.new(key=KEY,
                                                  page=next_page
                                                  )
            ))
    else:
        pages_buttons.append(
            InlineKeyboardButton(
                text=f" . ",
                callback_data=pagination_call.new(key=KEY, page="empty")
            )
        )

    pages_buttons.append(
        InlineKeyboardButton(
            text=max_page_text,
            callback_data=pagination_call.new(key=KEY,
                                              page=max_page
                                              )
        ))
    for item in item_buttons:
        markup.add(item)
    markup.row(*pages_buttons)
    return markup
