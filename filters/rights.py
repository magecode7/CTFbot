from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

import database
import ui


class MinRightsFilter(BoundFilter):
    def __init__(self, min_rights: int = 0):
        self.min_rights = min_rights
    

    async def check(self, message: types.Message) -> bool:
        check = database.get_user_rights(message.from_user.id) >= self.min_rights

        if not check: await message.answer(ui.TEXT_RIGHTS_MISSED)

        return check
