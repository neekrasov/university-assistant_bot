from typing import Union

from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from data.config import ADMINS

is_admin = lambda id: id in ADMINS


class IsPrivate(BoundFilter):
    async def check(self, message: Union[types.Message, types.CallbackQuery]) -> bool:
        if isinstance(message, types.Message):
            return message.chat.type == types.ChatType.PRIVATE
        if isinstance(message, types.CallbackQuery):
            return message.message.chat.type == types.ChatType.PRIVATE
